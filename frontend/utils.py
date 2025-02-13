import requests

api_url = "http://127.0.0.1:8000"


def fetch_data(endpoint, params=None):
    try:
        response = requests.get(f"{api_url}/{endpoint}", params=params)
        return response.json() if response.status_code == 200 else None
    except requests.RequestException as e:
        print(f"Error fetching data from {endpoint}: {e}")
        return None
