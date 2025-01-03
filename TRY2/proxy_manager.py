import requests
import random

class ProxyManager:
    def __init__(self, proxy_mesh_url):
        self.proxy_mesh_url = proxy_mesh_url
    
    def get_proxy(self):
        try:
            response = requests.get(self.proxy_mesh_url)
            proxies = response.text.strip().split('\n')
            return random.choice(proxies)
        except Exception as e:
            print(f"Error fetching proxy: {e}")
            return None

