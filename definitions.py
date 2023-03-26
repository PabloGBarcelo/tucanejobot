import os, json

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

f = open("./assets/options.json", encoding="utf-8")
options = json.load(f)