import hashlib
import time
import multiprocessing
import requests
import json


def worker(core_id, difficulty, stop_event, result_queue):
    prefix = "0" * difficulty
    nonce = core_id * 1_000_000

    data = f"CoreFlux-{core_id}"
    start = time.time()
    hashes = 0

    while not stop_event.is_set():
        h = hashlib.sha256(f"{data}{nonce}".encode()).hexdigest()
        hashes += 1

        if h.startswith(prefix):
            elapsed = time.time() - start
            hps = hashes / elapsed if elapsed > 0 else 0

            result_queue.put({
                "hash": h,
                "nonce": nonce,
                "hashrate": hps
            })

            hashes = 0
            start = time.time()

        nonce += 1


class Miner:
    def __init__(self, config):
        self.node_url = config["node_url"]
        self.wallet = config["wallet"]
        self.difficulty = config["difficulty"]

    def submit(self, block):
        return requests.post(
            f"{self.node_url}/mine",
            json={
                "hash": block["hash"],
                "nonce": block["nonce"],
                "wallet": self.wallet
            }
        ).json()

    def start(self):
        cores = multiprocessing.cpu_count()
        use = max(1, cores // 2)

        print(f"⛏️ Mining on {use}/{cores} cores")

        stop_event = multiprocessing.Event()
        queue = multiprocessing.Queue()

        procs = []

        for i in range(use):
            p = multiprocessing.Process(
                target=worker,
                args=(i, self.difficulty, stop_event, queue)
            )
            p.start()
            procs.append(p)

        try:
            while True:
                if not queue.empty():
                    block = queue.get()
                    res = self.submit(block)

                    print("\n🔥 BLOCK ACCEPTED")
                    print(res)

        except KeyboardInterrupt:
            stop_event.set()
            for p in procs:
                p.terminate()
