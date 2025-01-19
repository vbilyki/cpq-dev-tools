import requests


def make_request(method, url, api_key, **kwargs):
    headers = kwargs.pop("headers", {})
    headers.update({"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"})
    response = requests.request(method, url, headers=headers, **kwargs)
    response.raise_for_status()
    return response.json() if response.content else {}
