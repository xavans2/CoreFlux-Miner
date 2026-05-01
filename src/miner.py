import hashlib
import time
import multiprocessing


def worker(core_id, difficulty, stop_event, result_queue):
    prefix = "0" * difficulty

    # unieke start per core
    nonce = core_id * 1_000_000

    hash_count = 0
    start_time = time.time()

    data = f"CoreFlux-core-{core_id}"

    while not stop_event.is_set():
        text = f"{data}{nonce}".encode()
        h = hashlib.sha256(text).hexdigest()
        hash_count += 1

        # check proof-of-work
        if h.startswith(prefix):
            elapsed = time.time() - start_time
            hashrate = hash_count / elapsed if elapsed > 0 else 0

            result_queue.put({
                "core": core_id,
                "hash": h,
                "nonce": nonce,
                "hashrate": round(hashrate, 2)
            })

            # reset stats
            hash_count = 0
            start_time = time.time()

        nonce += 1


class Miner:
    def __init__(self, api_client, miner_name, difficulty=4):
        self.api = api_client
        self.name = miner_name
        self.difficulty = difficulty

    def start(self):
        total_cores = multiprocessing.cpu_count()
        used_cores = max(1, total_cores // 2)

        print("⛏️ CoreFlux Miner starting")
        print(f"🧠 Total cores: {total_cores}")
        print(f"⚙️ Using cores: {used_cores} (50%)")

        stop_event = multiprocessing.Event()
        result_queue = multiprocessing.Queue()

        processes = []

        for i in range(used_cores):
            p = multiprocessing.Process(
                target=worker,
                args=(i, self.difficulty, stop_event, result_queue)
            )
            p.start()
            processes.append(p)

        try:
            while True:
                if not result_queue.empty():
                    result = result_queue.get()

                    print("\n🔥 BLOCK FOUND")
                    print(f"Core: {result['core']}")
                    print(f"Hash: {result['hash']}")
                    print(f"Nonce: {result['nonce']}")
                    print(f"Hashrate: {result['hashrate']} H/s")

        except KeyboardInterrupt:
            print("\n🛑 Stopping miner...")
            stop_event.set()

            for p in processes:
                p.terminate()
                p.join()
