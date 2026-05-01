import hashlib
import time
import multiprocessing

def worker(core_id, difficulty, stop_event, result_queue):
    prefix = "0" * difficulty
    nonce = core_id * 1_000_000
    hash_count = 0
    start = time.time()

    data = f"CoreFlux-core-{core_id}"

    while not stop_event.is_set():
        text = f"{data}{nonce}".encode()
        h = hashlib.sha256(text).hexdigest()
        hash_count += 1

        if h.startswith(prefix):
            elapsed = time.time() - start
            hps = hash_count / elapsed

            result_queue.put({
                "core": core_id,
                "hash": h,
                "nonce": nonce,
                "hashrate": hps
            })

            # reset
            hash_count = 0
            start = time.time()

        nonce += 1


class Miner:
    def __init__(self, api_client, miner_name, difficulty=4):
        self.api = api_client
        self.name = miner_name
        self.difficulty = difficulty

    def start(self):
        cores = multiprocessing.cpu_count()

        print(f"⛏️ CoreFlux Miner starting on {cores} CPU cores")

        stop_event = multiprocessing.Event()
        result_queue = multiprocessing.Queue()

        processes = []

        for i in range(cores):
            p = multiprocessing.Process(
                target=worker,
                args=(i, self.difficulty, stop_event, result_queue)
            )
            processes.append(p)
            p.start()

        try:
            while True:
                if not result_queue.empty():
                    result = result_queue.get()
                    print("\n🔥 BLOCK FOUND")
                    print(result)

        except KeyboardInterrupt:
            stop_event.set()
            for p in processes:
                p.terminate()
