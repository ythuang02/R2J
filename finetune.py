import os
import json
import logging
import subprocess

from config import cfg
from chat import Chat
from process import run_multiprocess
from prompt import chat_template, rewrite

logger = logging.getLogger("main")

def before_finetune(step):
    data = json.load(open(cfg["data_path"]))
    dataset = []

    for sample in data:
        attempts = sorted(sample["attempts"].items(), key = lambda x: (x[1]["harmful"] + x[1]["similar"], x[1]["similar"], -x[1]["step"]), reverse = True)

        for index in range(min(len(attempts), cfg["experiment"]["finetune"]["num_samples"])):
            dataset.append({
                "instruction": rewrite(sample["instruction"]),
                "input": "",
                "output": attempts[index][0]
            })    
    
    save_dir = os.path.join(cfg["workspace"], "finetune")
    os.makedirs(save_dir, exist_ok = True)

    with open(os.path.join(save_dir, "step_%d.json" % (step)), "w", encoding = "utf-8") as writer:
        json.dump(dataset, writer, indent = 2, ensure_ascii = False)

    logger.info("Created fine-tuning dataset %s" % (os.path.join(save_dir, "step_%d.json" % (step))))

    dataset_info_path = os.path.join(save_dir, "dataset_info.json")
    if os.path.exists(dataset_info_path):
        dataset_info = json.load(open(dataset_info_path))
    else:
        dataset_info = {}
    
    dataset_info["step_%d" % (step)] = {
        "file_name": "step_%d.json" % (step)
    }

    with open(dataset_info_path, "w", encoding = "utf-8") as writer:
        json.dump(dataset_info, writer, indent = 2, ensure_ascii = False)

def start_finetune(step):
    finetune_args = cfg["experiment"]["finetune"]
    finetune_script = [
        'bash',
        'finetune/finetune.sh',
        finetune_args["gpu"],
        finetune_args["master_port"],
        finetune_args["deepspeed"],
        cfg["model"]["attacker"]["model_path"],
        "step_%d" % (step),
        os.path.join(cfg["workspace"], "finetune"),
        finetune_args["lora_target"],
        os.path.join(cfg["workspace"], "finetune", "step_%d" % (step)),
        finetune_args["cutoff_len"],
        cfg["experiment"]["num_workers"],
        finetune_args["per_device_train_batch_size"],
        finetune_args["gradient_accumulation_steps"],
        finetune_args["logging_steps"],
        finetune_args["warmup_steps"],
        finetune_args["eval_steps"],
        finetune_args["learning_rate"],
        finetune_args["num_train_epochs"]
    ]

    if finetune_args["bf16"]:
        finetune_script.append("bf16")
    elif finetune_args["fp16"]:
        finetune_script.append("fp16")
    else:
        finetune_script.append("fp32")

    for args in range(len(finetune_script)):
        finetune_script[args] = str(finetune_script[args])

    os.makedirs(finetune_script[9], exist_ok = True)

    logger.info("Ready for fine-tuning, running scripts: " + " ".join(finetune_script))
    logger.info("Log save to %s" % os.path.join(finetune_script[9], "finetune.log"))

    subprocess.run(
        finetune_script, 
        env = dict(os.environ) | {
            "MKL_SERVICE_FORCE_INTEL": "1"
        }
    )

def after_finetune(step):
    def Loader(tasks, args):
        data = json.load(open(cfg["data_path"]))

        for sample in data:
            tasks.put(sample) 
    
    def Saver(results, args):
        running = True
        data = json.load(open(cfg["data_path"]))

        while running:
            results.put(-2)

            while True:
                sample = results.get()

                if isinstance(sample, int) and sample == -1:
                    running = False
                    break

                if isinstance(sample, int) and sample == -2:
                    break

                data[sample["id"]] = sample

        with open(cfg["data_path"], "w", encoding = "utf-8") as writer:
            json.dump(data, writer, indent = 2, ensure_ascii = False)

    def Worker(tasks, results, args, index):
        import os
        os.environ['CUDA_VISIBLE_DEVICES'] = str(index)

        model = cfg["model"]["attacker"]
        if "lora_path" not in model:
            model["lora_path"] = os.path.join(cfg["workspace"], "finetune", "step_%d" % (step))
        attacker = Chat(model)

        while True:
            task = tasks.get()

            if isinstance(task, int) and task == -1:
                break

            attempts = sorted(task["attempts"].items(), key = lambda x: (x[1]["harmful"] + x[1]["similar"], x[1]["similar"], -x[1]["step"]), reverse = True)[:cfg["experiment"]["attacker"]["num_samples"]]

            for attempt in attempts:
                instruction = attempt[0]

                for _ in range(cfg["experiment"]["attacker"]["num_adds"]):
                    instruction_rewrite = attacker.query(chat_template(rewrite(instruction), add_system_prompt=False)).strip()

                    if len(instruction_rewrite) > 0:
                        if instruction_rewrite not in task["attempts"]:
                            task["attempts"][instruction_rewrite] = {
                                "harmful": -1,
                                "similar": -1,
                                "step": step
                            }

                        logger.debug("Rewrite instruction %s to %s" % (instruction, instruction_rewrite))
                        instruction = instruction_rewrite
            
            results.put(task)
    
    attacker = Chat(cfg["model"]["attacker"], load = False)
    
    if attacker.model_type == "api":
        run_multiprocess(Saver, (), Worker, (), range(cfg["experiment"]["num_workers"]), Loader, ())
    else:
        run_multiprocess(Saver, (), Worker, (), cfg["experiment"]["attacker"]["gpu"].split(",") * cfg["experiment"]["attacker"]["per_device_workers"], Loader, ())

def finetune(step):
    if cfg["experiment"]["finetune"]["finetune"] == True:
        before_finetune(step)
        start_finetune(step)
    after_finetune(step)