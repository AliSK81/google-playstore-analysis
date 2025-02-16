import requests

api_url = "http://127.0.0.1:8000"


def fetch_data(endpoint, params=None):
    try:
        response = requests.get(f"{api_url}/{endpoint}", params=params)
        return response.json() if response.status_code == 200 else None
    except requests.RequestException as e:
        print(f"Error fetching data from {endpoint}: {e}")
        return None


def post_data(endpoint, data):
    try:
        response = requests.post(f"{api_url}/{endpoint}", json=data)
        return response.json() if response.status_code == 200 else None
    except requests.RequestException as e:
        print(f"Error posting data to {endpoint}: {e}")
        return None


def put_data(endpoint, data):
    try:
        response = requests.put(f"{api_url}/{endpoint}", json=data)
        return response.json() if response.status_code == 200 else None
    except requests.RequestException as e:
        print(f"Error updating data at {endpoint}: {e}")
        return None


def delete_data(endpoint):
    try:
        response = requests.delete(f"{api_url}/{endpoint}")
        return response.status_code == 200
    except requests.RequestException as e:
        print(f"Error deleting data at {endpoint}: {e}")
        return False


def fetch_categories():
    return fetch_data("categories")


def create_category(name):
    return post_data("categories", {"name": name})


def update_category(category_id, name):
    return put_data(f"categories/{category_id}", {"name": name})


def delete_category(category_id):
    return delete_data(f"categories/{category_id}")


def fetch_developers(filters):
    return fetch_data("developers", filters)


def create_developer(name, email):
    return post_data("developers", {"name": name, "email": email})


def update_developer(developer_id, name, email):
    return put_data(f"developers/{developer_id}", {"name": name, "email": email})


def delete_developer(developer_id):
    return delete_data(f"developers/{developer_id}")


def fetch_apps(filters=None):
    return fetch_data("apps", filters)


def create_app(app_id, app_name, category_id, developer_id, rating, free):
    return post_data("apps", {
        "app_id": app_id, "app_name": app_name,
        "category_id": category_id, "developer_id": developer_id,
        "rating": rating, "free": free
    })


def update_app(app_id, app_name, app_id_new):
    return put_data(f"apps/{app_id}", {"app_name": app_name, "app_id": app_id_new})


def delete_app(app_id):
    return delete_data(f"apps/{app_id}")


def fetch_filters():
    filters_data = fetch_data("filters")
    return filters_data if filters_data else {}


def fetch_rating_distribution(filters):
    data = fetch_data("statistics/rating_distribution", filters)
    return data if data else []


def fetch_release_trend(category=None):
    params = {"category_name": category} if category else {}
    return fetch_data("statistics/release_trend", params)


def fetch_update_trend(category=None):
    params = {"category_name": category} if category else {}
    return fetch_data("statistics/update_trend", params)


def fetch_average_rating(category):
    params = {"category_name": category} if category else {}
    return fetch_data("statistics/average_rating", params).get("average_rating")
