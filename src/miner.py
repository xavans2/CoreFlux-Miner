
import time
import random

class Miner:
    def __init__(self, api_client, miner_name):
        self.api = api_client
        self.name = miner_name
        self.running = True

    def generate_data(self):
        return f"{self.name}-{random.randint(0,999999)}"

    def start(self):
        print("Miner started...")

        while self.running:
            data = self.generate_data()
            result = self.api.mine_block(data)

            print("Mined block:")
            print(result)

            time.sleep(2)
