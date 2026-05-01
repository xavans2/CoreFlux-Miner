
import requests

class APIClient:
    def __init__(self, node_url):
        self.node_url = node_url

    def get_chain(self):
        return requests.get(f"{self.node_url}/chain").json()

    def mine_block(self, data):
        return requests.post(
            f"{self.node_url}/mine",
            params={"data": data}
        ).json()
