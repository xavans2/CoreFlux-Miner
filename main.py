import json
from src.api_client import APIClient
from src.miner import Miner

with open("config/miner_config.json") as f:
    config = json.load(f)

api = APIClient(config["node_url"])

miner = Miner(
    api,
    config["miner_name"],
    difficulty=4
)

miner.start()
