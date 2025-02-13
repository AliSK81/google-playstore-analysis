import pandas as pd
import requests

api_url = "http://127.0.0.1:8000"


def fetch_data(endpoint, params=None):
    try:
        response = requests.get(f"{api_url}/{endpoint}", params=params)
        return response.json() if response.status_code == 200 else None
    except requests.RequestException as e:
        print(f"Error fetching data from {endpoint}: {e}")
        return None


def fetch_filters():
    filters_data = fetch_data("filters")
    return filters_data if filters_data else {}


def fetch_apps(filters):
    data = fetch_data("apps", filters)
    return pd.DataFrame(data) if data else pd.DataFrame()


def fetch_rating_distribution(filters):
    data = fetch_data("apps/rating_distribution", filters)
    return data if data else []


def fetch_release_trend(category=None):
    params = {"category_name": category} if category else {}
    return fetch_data("apps/release_trend", params)


def fetch_update_trend(category=None):
    params = {"category_name": category} if category else {}
    return fetch_data("apps/release_trend", params)


def fetch_average_rating(category):
    params = {"category_name": category} if category else {}
    return fetch_data("apps/average_rating", params).get("average_rating")
