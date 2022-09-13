import json
import os
from os.path import expanduser

home = expanduser("~").replace("\\", "/")


def load_config():
    config_path = os.path.join(home, ".gmcache", "config.json")
    if os.path.exists(config_path):
        with open(os.path.join(home, ".gmcache", "config.json"), mode='r') as f:
            return json.load(f)
    else:
        config_dir = os.path.join(home, ".gmcache")
        if not os.path.exists(config_dir):
            os.makedirs(os.path.join(home, ".gmcache"))
        return {}


def store_config(config: dict):
    with open(os.path.join(home, ".gmcache", "config.json"), 'w', encoding='utf-8') as f:
        json.dump(config, f)
