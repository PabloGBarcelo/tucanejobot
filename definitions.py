import os, json, platform

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
SLASH = "/" if platform.system() == "Linux" else "\\"

f = open("./assets/options.json", encoding="utf-8")
options = json.load(f)