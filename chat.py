import time
import logging
import requests
import json

from config import cfg

logger = logging.getLogger("main")

class OpenAI:
    company = "OpenAI"
    policy = '''1. Comply with applicable laws - for example, don't compromise the privacy of others,  engage in regulated activity without complying with applicable regulations, or promote or engage in any illegal activity, including the exploitation or harm of children and the development or distribution of illegal substances, goods, or services.
2. Don't use our service to harm yourself or others - for example, don't use our services to promote suicide or self-harm, develop or use weapons, injure others or destroy property, or engage in unauthorized activities that violate the security of any service or system. 
3. Don't repurpose or distribute output from our services to harm others - for example, don't share output from our services to defraud, scam, spam, mislead, bully, harass, defame, discriminate based on protected attributes, sexualize children, or promote violence, hatred or the suffering of others.
4. Respect our safeguards - don't circumvent safeguards or safety mitigations in our services unless supported by OpenAI (e.g., domain experts in our Red Teaming Network) or related to research conducted in accordance with our Sharing & Publication Policy.'''
    
    def __init__(self, model: str, temperature: float, top_p: float, api: dict):
        self.model = model
        self.temperature = temperature
        self.top_p = top_p
        self.api = api
    
    def query(self, conversation_list: list):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.3",
            "Content-Type": "application/json",
            "Authorization": "Bearer %s" % (self.api["key"])
        }
        data = {
            "model": self.model,
            "messages": conversation_list,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "stream": False,
        }

        for _ in range(self.api["max_retry"]):
            time.sleep(self.api["interval"])

            try:
                response = requests.post(self.api["base_url"], headers = headers, json = data)
                response = json.loads(response.text)
                return response["choices"][0]["message"]["content"]
            except Exception as e:
                logger.debug(e)

        return ""
    
    def batch_query(self, batch_conversation_list: list[list]):
        return [self.query(c) for c in batch_conversation_list]

class Google:
    company = "Google"
    policy = '''1. Perform or facilitate dangerous, illegal, or malicious activities, including
a. Facilitation or promotion of illegal activities or violations of law, such as
i. Promoting or generating content related to child sexual abuse or exploitation
ii. Promoting or facilitating sale of, or providing instructions for synthesizing or accessing, illegal substances, goods, or services
iii. Facilitating or encouraging users to commit any type of crimes
iv. Promoting or generating violent extremism or terrorist content
b. Abuse, harm, interference, or disruption of services (or enable others to do the same), such as
i. Promoting or facilitating the generation or distribution of spam
ii. Generating content for deceptive or fraudulent activities, scams, phishing, or malware.
c. Attempts to override or circumvent safety filters or intentionally drive the model to act in a manner that contravenes our policies
d. Generation of content that may harm or promote the harm of individuals or a group, such as
i. Generating content that promotes or encourages hatred
ii. Facilitating methods of harassment or bullying to intimidate, abuse, or insult others
iii. Generating content that facilitates, promotes, or incites violence
iv. Generating content that facilitates, promotes, or encourages self harm
v. Generating personally identifying information for distribution or other harms
vi. Tracking or monitoring people without their consent
vii. Generating content that may have unfair or adverse impacts on people, particularly impacts related to sensitive or protected characteristics
2. Generate and distribute content intended to misinform, misrepresent or mislead, including
a. Misrepresentation of the provenance of generated content by claiming content was created by a human, or represent generated content as original works, in order to deceive
b. Generation of content that impersonates an individual (living or dead) without explicit disclosure, in order to deceive
c. Misleading claims of expertise or capability made particularly in sensitive areas (e.g. health, finance, government services, or legal)
d. Making automated decisions in domains that affect material or individual rights or well-being (e.g., finance, legal, employment, healthcare, housing, insurance, and social welfare)
3. Generate sexually explicit content, including content created for the purposes of pornography or sexual gratification (e.g. sexual chatbots). Note that this does not include content created for scientific, educational, documentary, or artistic purposes.'''
    
    def __init__(self, model: str, temperature: float, top_p: float, api: dict):
        self.model = model
        self.temperature = temperature
        self.top_p = top_p
        self.api = api
    
    def query(self, conversation_list: list):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.3",
            "Content-Type": "application/json",
            "Authorization": "Bearer %s" % (self.api["key"])
        }
        data = {
            "model": self.model,
            "messages": conversation_list,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "stream": False,
        }

        for _ in range(self.api["max_retry"]):
            time.sleep(self.api["interval"])

            try:
                response = requests.post(self.api["base_url"], headers = headers, json = data)
                response = json.loads(response.text)
                return response["choices"][0]["message"]["content"]
            except Exception as e:
                logger.debug(e)

        return ""
    
    def batch_query(self, batch_conversation_list: list[list]):
        return [self.query(c) for c in batch_conversation_list]

class Anthropic:
    company = "Anthropic"
    policy = '''1. Do Not Compromise Children's Safety
2. Do Not Compromise Critical Infrastructure
3. Do Not Incite Violence or Hateful Behavior
4. Do Not Compromise Someone's Privacy or Identity
5. Do Not Create or Facilitate the Exchange of Illegal or Highly Regulated Weapons or Goods
6. Do Not Create Psychologically or Emotionally Harmful Content
7. Do Not Spread Misinformation
8. Do Not Create Political Campaigns or Interfere in Elections
9. Do Not Use for Criminal Justice, Law Enforcement, Censorship or Surveillance Purposes
10. Do Not Engage in Fraudulent, Abusive, or Predatory Practices
11. Do Not Abuse our Platform
12. Do Not Generate Sexually Explicit Content'''
    
    def __init__(self, model: str, temperature: float, top_p: float, api: dict):
        self.model = model
        self.temperature = temperature
        self.top_p = top_p
        self.api = api
    
    def query(self, conversation_list: list):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.3",
            "Content-Type": "application/json",
            "Authorization": "Bearer %s" % (self.api["key"])
        }
        data = {
            "model": self.model,
            "messages": conversation_list,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "stream": False,
        }

        for _ in range(self.api["max_retry"]):
            time.sleep(self.api["interval"])

            try:
                response = requests.post(self.api["base_url"], headers = headers, json = data)
                response = json.loads(response.text)
                return response["choices"][0]["message"]["content"]
            except Exception as e:
                logger.debug(e)

        return ""
    
    def batch_query(self, batch_conversation_list: list[list]):
        return [self.query(c) for c in batch_conversation_list]
    
class Meta:
    company = "Meta"
    policy = '''1. Violate the law or others' rights, including to:
a. Engage in, promote, generate, contribute to, encourage, plan, incite, or further illegal or unlawful activity or content, such as:
i. Violence or terrorism
ii. Exploitation or harm to children, including the solicitation, creation, acquisition, or dissemination of child exploitative content or failure to report Child Sexual Abuse Material
b. Human trafficking, exploitation, and sexual violence
iii. The illegal distribution of information or materials to minors, including obscene materials, or failure to employ legally required age-gating in connection with such information or materials.
iv. Sexual solicitation
vi. Any other criminal activity
c. Engage in, promote, incite, or facilitate the harassment, abuse, threatening, or bullying of individuals or groups of individuals
d. Engage in, promote, incite, or facilitate discrimination or other unlawful or harmful conduct in the provision of employment, employment benefits, credit, housing, other economic benefits, or other essential goods and services
e. Engage in the unauthorized or unlicensed practice of any profession including, but not limited to, financial, legal, medical/health, or related professional practices
f. Collect, process, disclose, generate, or infer health, demographic, or other sensitive personal or private information about individuals without rights and consents required by applicable laws
g. Engage in or facilitate any action or generate any content that infringes, misappropriates, or otherwise violates any third-party rights, including the outputs or results of any products or services using the Llama 2 Materials
h. Create, generate, or facilitate the creation of malicious code, malware, computer viruses or do anything else that could disable, overburden, interfere with or impair the proper working, integrity, operation or appearance of a website or computer system
2. Engage in, promote, incite, facilitate, or assist in the planning or development of activities that present a risk of death or bodily harm to individuals, including use of Llama 2 related to the following:
a. Military, warfare, nuclear industries or applications, espionage, use for materials or activities that are subject to the International Traffic Arms Regulations (ITAR) maintained by the United States Department of State
b. Guns and illegal weapons (including weapon development)
c. Illegal drugs and regulated/controlled substances
d. Operation of critical infrastructure, transportation technologies, or heavy machinery
e. Self-harm or harm to others, including suicide, cutting, and eating disorders
f. Any content intended to incite or promote violence, abuse, or any infliction of bodily harm to an individual
3. Intentionally deceive or mislead others, including use of Llama 2 related to the following:
a. Generating, promoting, or furthering fraud or the creation or promotion of disinformation
b. Generating, promoting, or furthering defamatory content, including the creation of defamatory statements, images, or other content
c. Generating, promoting, or further distributing spam
d. Impersonating another individual without consent, authorization, or legal right
e. Representing that the use of Llama 2 or outputs are human-generated
f. Generating or facilitating false online engagement, including fake reviews and other means of fake online engagement
4. Fail to appropriately disclose to end users any known dangers of your AI system'''

    def __init__(self, model: str, model_path: str, temperature: float, top_p: float, cutoff_len: int, dtype: str):
        self.model = model
        self.model_path = model_path
        self.temperature = temperature
        self.top_p = top_p
        self.cutoff_len = cutoff_len
        self.dtype = dtype
    
    def load(self):
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
        from factory.src.llmtuner.data.template import templates

        if self.model in ["llama-2-7b-chat", "llama-2-13b-chat"]:
            self.template = templates["llama2"]
        elif self.model in ["llama-3-8b-chat"]:
            self.template = templates["llama3"]
        else:
            self.template = templates["default"]

        if self.dtype == "float16":
            self.torch_dtype = torch.float16
        elif self.dtype == "bfloat16":
            self.torch_dtype = torch.bfloat16
        else:
            self.torch_dtype = torch.float32

        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.tokenizer.padding_side = "left"

        self.model = AutoModelForCausalLM.from_pretrained(self.model_path, torch_dtype=self.torch_dtype, device_map='cuda')

    def load_lora(self, lora: str):
        from peft import PeftModel
        
        self.model = PeftModel.from_pretrained(self.model, lora, torch_dtype=self.torch_dtype, device_map='cuda')
    
    def compile(self):
        import torch
        self.model = torch.compile(self.model)

    def batch_query(self, batch_conversation_list: list):
        import torch

        def padding(batch: list[list], tokenizer):
            padded = torch.zeros(len(batch), max([len(s) for s in batch]), dtype=torch.long)
            
            for index in range(len(batch)):
                if tokenizer.padding_side == "left":
                    start, end = 0, padded.size(1) - len(batch[index])
                    padded[index, end:] = torch.LongTensor(batch[index])
                else:
                    start, end = len(batch[index]), padded.size(1)
                    padded[index, :start] = torch.LongTensor(batch[index])
                
                padded[index, start: end] = tokenizer.pad_token_id
            return padded
        
        batch = []
        for conversation_list in batch_conversation_list:
            inputs = [{"bos_token"}]

            for message in conversation_list:
                if message["role"] == "system":
                    inputs += self.template.format_system.apply(content=(message["content"]))
                elif message["role"] == "user":
                    inputs += self.template.format_user.apply(content=message["content"])        
            
            input_ids = self.template._convert_elements_to_ids(self.tokenizer, inputs)[:self.cutoff_len - 1]
            batch.append(input_ids)
        
        input_ids = padding(batch, self.tokenizer)
        output_ids = self.model.generate(
            input_ids = input_ids.cuda(),
            temperature = self.temperature,
            top_p = self.top_p,
            max_length = self.cutoff_len
        )


        return self.tokenizer.batch_decode(output_ids[:, len(input_ids[0]):].detach().cpu().numpy(), skip_special_tokens=True)

class Chat:
    def __init__(self, config: dict, load: bool = True):
        if config["model"] in ["gpt-3.5-turbo-0125", "gpt-3.5-turbo-1106", "gpt-3.5-turbo-instruct", "gpt-3.5-turbo-0613"]:
            self.model = OpenAI(config["model"], config["temperature"], config["top_p"], config["api"])
            self.model_type = "api"
        
        elif config["model"] in ["gpt-4-turbo-2024-04-09", "gpt-4-0125-preview", "gpt-4-1106-preview", "gpt-4-0613"]:
            self.model = OpenAI(config["model"], config["temperature"], config["top_p"], config["api"])
            self.model_type = "api"
        
        elif config["model"] in ["gpt-4o-2024-05-13", "gpt-4o"]:
            self.model = OpenAI(config["model"], config["temperature"], config["top_p"], config["api"])
            self.model_type = "api"
        
        elif config["model"] in ["gemini-pro", "gemini-1.5-pro"]:
            self.model = Google(config["model"], config["temperature"], config["top_p"], config["api"])
            self.model_type = "api"  

        elif config["model"] in ["claude-3-haiku-20240307"]:
            self.model = Anthropic(config["model"], config["temperature"], config["top_p"], config["api"])
            self.model_type = "api"    
        
        elif config["model"] in ["llama-2-7b", "llama-3-8b", "llama-2-7b-chat", "llama-2-13b-chat", "llama-3-8b-chat"]:
            self.model_type = "gpu"
            self.model = Meta(config["model"], config["model_path"], config["temperature"], config["top_p"], config["cutoff_len"], config["dtype"])

            if load:
                self.model.load()
                if "lora_path" in config:
                    self.model.load_lora(config["lora_path"])
                self.model.compile()
        
    def query(self, conversation_list: list):
        return self.model.batch_query([conversation_list])[0]
    
    def batch_query(self, batch_conversation_list: list):
        return self.model.batch_query(batch_conversation_list)