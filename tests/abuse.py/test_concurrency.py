from asyncio import threads
import pytest
import requests
import threading

def test_concureeny(base_url):

    before = requests.get(f"{base_url}/state").json()["counter"]
    def hit_state():
        response = requests.post(f"{base_url}/state")
       

    threads =[
       threading.Thread(target=hit_state)
       for _ in range(5)
   ]
  
    for t in threads:
       t.start()

    for t in threads:
       t.join()   

    after = requests.get(f"{base_url}/state").json()["counter"]   

    assert after in (before + 4, before + 5), (
    f"Concurrency bug detected. Before={before}, After={after}"
)

       