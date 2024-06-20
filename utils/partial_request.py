import requests
from functools import partial

session = requests.Session()
get_req = partial(
    requests.get,
    timeout=15
)