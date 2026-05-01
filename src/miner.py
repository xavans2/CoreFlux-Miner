import time
import hashlib
import threading

class Miner:
    def __init__(self, api_client, miner_name, difficulty=4):
        self.api = api_client
        self.name = miner_name
        self.difficulty = difficulty
        self.running = True

        self.hash_count = 0
        self.start_time = time.time()

    def hash_block(self, data, nonce):
        text = f"{data}{nonce}".encode()
        return hashlib.sha256(text).hexdigest()

    def start(self):
        print("⛏️ CoreFlux miner started (PoW mode)")

        prefix = "0" * self.difficulty
        nonce = 0

        data = f"{self.name}-block"

        while self.running:
            hash_result = self.hash_block(data, nonce)
            self.hash_count += 1

            if hash_result.startswith(prefix):
                elapsed = time.time() - self.start_time
                hashrate = self.hash_count / elapsed if elapsed > 0 else 0

                print("\n🔥 BLOCK FOUND")
                print("Hash:", hash_result)
                print("Nonce:", nonce)
                print(f"Hashrate: {hashrate:.2f} H/s\n")

                # reset voor volgende block
                nonce = 0
                self.hash_count = 0
                self.start_time = time.time()

            nonce += 1
