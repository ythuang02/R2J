import yaml

cfg = {}

def load_config(file_str: str) -> None:
    global cfg
    
    with open(file_str) as f:
        cfg.update(yaml.safe_load(f))