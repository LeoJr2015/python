import json

configfile = "config_game.json"
loaded = ""

def writeout():
    with open(configfile,"w") as f:
        json.dump(loaded,f)
    
def load():
    global loaded
    with open(configfile) as f:
        loaded = json.load(f)

def get():
    global loaded
    return loaded
    
load()
        
