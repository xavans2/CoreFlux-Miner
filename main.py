import json
from src.miner import Miner

with open("config/miner_config.json") as f:
    config = json.load(f)

miner = Miner(config)
miner.start()
