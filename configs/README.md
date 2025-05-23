# Configuration Documentation

The configuration file for the experiment is a [YAML format](https://en.wikipedia.org/wiki/YAML) file, which includes the following fields:

## 1. Field `model`

This field defines the configurations for the attacker model (subfield `attacker`), target model (subfield `target`), and evaluator model (subfield `evaluator`).

| Name | Type | Description | Example |
| ---- | ---- | ----------- | ------- |
| model | String | The type of the model | Options: `gpt-3.5-turbo-0125`, `gpt-3.5-turbo-1106`, `gpt-4o-2024-05-13`, `gemini-pro`, `llama-2-7b-chat`, `llama-2-13b-chat`, `llama-3-8b-chat`, `llama-3-8b`|
| temperature | Float | The sampling temperature | Default: `1.0` (attacker model), `0.7` (target model), `0` (evaluator model) |
| top_p | Float | An alternative to sampling with temperature, called nucleus sampling | Default: `1.0` |
| cutoff_len | Int | The maximum length of the data | Default: `1024` |
| model_path | String | (Optional, for open-source model) Path to the Huggingface model | `/root/model/Llama-2-7b-hf` |
| lora_path | String | (Optional, for transfer attack) Path to the trained attacker model | `saves/AdvBench_gpt-3.5-turbo-0125/step_20` |
| dtype | String | (Optional, for open-source model) The data type object to load the model | Options: `float16`, `bfloat16`, `float32` |
| api | `API` | (Optional, for closed-source model) ||

**Type `API`**

| Name | Type | Description | Example |
| ---- | ---- | ----------- | ------- |
| base_url | String | The base URL for the API connector | `https://api.openai.com/v1/chat/completions` |
| key | String | The API key for authentication | `sk-********` |
| max_retry | Int | Maximum number of failure retries | `10` |
| Interval | Int | Failure retry Interval | `1` |

## 2. Field `experiment`

This field defines the settings and hyperparameters of the experiment.

| Name | Type | Description | Example |
| ---- | ---- | ----------- | ------- |
| dataset | String | The dataset of the experiment | Options: `AdvBench`, `CatQA-en`, `DangerousQA`, `HEx-PHI` |
| num_workers | Int | Maximum number of subprocesses | `100` |
| resume | Bool or String | Start from the previous checkpoint | `False` or `results/AdvBench_llama-2-7b-chat_20240605185530` |
| start_from | Int | Initial iteration step | Default: `1` (for direct jailbreak attack), `0` (for transfer attack) |
| max_step | Int | Hyperparameter $n$, the maximum number of iterations | Default: `20` (for direct jailbreak attack), `30` (for transfer attack) |

## 2.1 Subfield `finetune`

This subfield includes SFT-related settings.

| Name | Type | Description | Example |
| ---- | ---- | ----------- | ------- |
| finetune | Bool | Whether to train the attacker model | Default: `True` (for direct jailbreak attack), `False` (for transfer attack)
| gpu | String | The GPUs used for training | `0,1` |
| num_samples | Int | Hyperparameter $p$, the number of attempts of each instance $X_i$ to form the SFT dataset | Default: `5` |
| master_port | Int | The master port for DeepSpeed | `30500` |
| deepspeed | String | Path to DeepSpeed ZeRO optimization configuration | Default: `finetune/ds_z3_config.json` |
| lora_target | String | Target for LoRA | Default: `gate_proj,down_proj,up_proj,q_proj,k_proj,v_proj,o_proj` |
| cutoff_len | Int | The maximum length of the data | Default: `1024` |
| per_device_train_batch_size | Int | The batch size per GPU for training | `16` |
| gradient_accumulation_steps | Int | Number of updates steps to accumulate the gradients for | `1` |
| logging_steps | Int | Number of update steps between two log | `5` |
| warmup_steps | Int | Number of steps used for a linear warmup from 0 to `learning rate` | Default: `10` |
| eval_steps | Int | Number of update steps between two evaluations | `100` |
| learning_rate | Float | The initial learning rate for AdamW | Default: `1e-4` |
| num_train_epochs | Int | Total number of training epochs to perform | Default: `3` (for dataset AdvBench, CatQA-en, and HEx-PHI), `5` (for dataset DangerousQA) |
| fp16 | Bool | Whether to use 16-bit (mixed) precision training | Default: `False`
| bf16 | Bool | Whether to use brain 16-bit (mixed) precision training | Default: `True`

## 2.2 Subfield `evaluator`

This subfield contains settings related to evaluation.

| Name | Type | Description | Example |
| ---- | ---- | ----------- | ------- |
| max_retry | Int | Maximum number of failure retries | `5` |
| threshold_similar | Int | Similarity threshold $\delta$ | Default: `3` |

## 2.3 Subfield `attacker`

This subfield contains settings related to the rewriting stage.

| Name | Type | Description | Example |
| ---- | ---- | ----------- | ------- |
| gpu | String | The GPUs used for rewritting | `0,1,2,3` |
| per_device_workers| Int | The number of workers per GPU | `1` |
| num_samples | Int | Hyperparameter $q$, the number of attempts of each instance $X_i$ for rewriting | Default: `3` |
| num_adds | Int | The number of rewrites for each attempt | Default: `3` |

## 2.4 Subfield `target`

This subfield contains settings related to generating the target response.

| Name | Type | Description | Example |
| ---- | ---- | ----------- | ------- |
| per_device_batch_size | Int | The batch size per worker for inference | `1` |
| gpu | String | (Optional, for open-source model) The GPUs used for inference | `0,1,2,3` |
| per_device_workers | Int | (Optional, for open-source model) The number of workers per GPU | `1` |