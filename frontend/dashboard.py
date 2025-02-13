import matplotlib.pyplot as plt
import pandas as pd
import requests
import streamlit as st

api_url = "http://127.0.0.1:8000"


def fetch_filters():
    response = requests.get(f"{api_url}/filters")
    return response.json() if response.status_code == 200 else {}


def fetch_apps(filters):
    response = requests.get(f"{api_url}/apps", params=filters)
    return pd.DataFrame(response.json()) if response.status_code == 200 else pd.DataFrame()


def fetch_release_trend(category: str | None = None):
    params = {"category_name": category} if category else {}
    response = requests.get(f"{api_url}/apps/release_trend", params=params)
    return response.json() if response.status_code == 200 else []


def fetch_average_rating(category):
    params = {"category_name": category} if category else {}
    response = requests.get(f"{api_url}/apps/average_rating/", params=params)
    return response.json().get("average_rating") if response.status_code == 200 else None


def configure_page():
    st.set_page_config(page_title="Google Play Store Data Analytics", layout="wide")
    st.title("📊 Google Play Store Data Analytics")


def load_filters():
    if "filters_data" not in st.session_state:
        st.session_state.filters_data = fetch_filters()


def get_filter_values():
    filters_data = st.session_state.filters_data
    categories = filters_data.get("categories", [])
    content_ratings = filters_data.get("content_ratings", [])
    min_rating = filters_data.get("min_rating", 0.0)
    max_rating = filters_data.get("max_rating", 5.0)
    min_price = filters_data.get("min_price", 0.0)
    max_price = filters_data.get("max_price", 100.0)
    min_installs = filters_data.get("min_installs", 0)
    max_installs = filters_data.get("max_installs", 10000000)
    return categories, content_ratings, min_rating, max_rating, min_price, max_price, min_installs, max_installs


def get_filter_input(tab, categories, content_ratings, min_rating, max_rating, min_price, max_price, min_installs,
                     max_installs):
    with st.sidebar:
        content_rating = None
        free_only = has_ads = has_in_app_purchases = editors_choice = False
        limit = 1000

        category = st.selectbox("📂 Select Category", ["All"] + categories)

        if tab in ["Filtered Apps", "Rating Distribution"]:
            min_rating, max_rating = st.slider(
                "⭐ Rating Range",
                min_value=min_rating,
                max_value=max_rating,
                value=(min_rating, max_rating),
                step=0.1
            )
            min_price, max_price = st.slider(
                "💰 Price Range ($)",
                min_value=min_price,
                max_value=max_price,
                value=(min_price, max_price),
                step=0.1
            )
            min_installs = st.number_input("📥 Minimum Installs", min_value=min_installs, value=min_installs, step=100)
            max_installs = st.number_input("📥 Maximum Installs", min_value=min_installs, value=max_installs, step=100)
            content_rating = st.selectbox("🔞 Content Rating", ["All"] + content_ratings)
            free_only = st.checkbox("🆓 Show Only Free Apps")
            has_ads = st.checkbox("📢 Apps with Ads")
            has_in_app_purchases = st.checkbox("💵 Apps with In-App Purchases")
            editors_choice = st.checkbox("🏆 Editors' Choice")

        if tab == "Filtered Apps":
            limit = st.number_input("📝 Results Limit", min_value=1, max_value=5000, value=1000, step=100)

    return {
        "category": None if category == "All" else category,
        "min_rating": min_rating,
        "max_rating": max_rating,
        "min_price": min_price,
        "max_price": max_price,
        "min_installs": min_installs,
        "max_installs": max_installs,
        "content_rating": None if content_rating == "All" else content_rating,
        "free": None if not free_only else True,
        "ad_supported": None if not has_ads else True,
        "in_app_purchases": None if not has_in_app_purchases else True,
        "editors_choice": None if not editors_choice else True,
        "limit": limit
    }


def display_filtered_apps(filters):
    st.subheader("Filtered Apps")
    filtered_df = fetch_apps(filters)
    if filtered_df.empty:
        st.warning("No apps found with the current filters.")
    else:
        st.dataframe(filtered_df)


def plot_rating_distribution(filters):
    st.subheader("📊 Rating Distribution")

    filtered_df = fetch_apps(filters)
    if filtered_df.empty:
        st.warning("No data available for rating distribution.")
    else:
        fig, ax = plt.subplots(figsize=(8, 3))
        filtered_df["rating"].hist(bins=20, ax=ax, color="blue", alpha=0.7)
        ax.set_xlabel("Rating")
        ax.set_ylabel("Count")
        st.pyplot(fig)


def plot_release_trend(category):
    st.subheader("📅 App Release Trend")
    release_trend = fetch_release_trend(category)
    if release_trend:
        years = [entry["year"] for entry in release_trend]
        counts = [entry["count"] for entry in release_trend]
        fig, ax = plt.subplots(figsize=(8, 3))
        ax.plot(years, counts, marker="o", color="green")
        ax.set_xlabel("Year")
        ax.set_ylabel("Number of Apps Released")
        st.pyplot(fig)
    else:
        st.warning(f"No release trend data available for {category}.")


def display_average_rating(category):
    st.subheader("📊 Average Rating per Category")
    avg_rating = fetch_average_rating(category)
    rounded_rating = round(avg_rating, 1)
    st.markdown(f"### 🌟 **{rounded_rating}** / 5")


def main():
    configure_page()
    load_filters()

    (categories, content_ratings,
     min_rating, max_rating,
     min_price, max_price,
     min_installs, max_installs) = get_filter_values()

    tab = st.sidebar.radio("Choose a tab",
                           ["Filtered Apps", "Rating Distribution", "App Release Trend", "Average Rating per Category"])

    filters = get_filter_input(tab, categories, content_ratings, min_rating, max_rating, min_price, max_price,
                               min_installs,
                               max_installs)

    selected_category = filters.get("category", categories[0])

    if tab == "Filtered Apps":
        display_filtered_apps(filters)
    elif tab == "Rating Distribution":
        plot_rating_distribution(filters)
    elif tab == "App Release Trend":
        plot_release_trend(selected_category)
    elif tab == "Average Rating per Category":
        display_average_rating(selected_category)


if __name__ == "__main__":
    main()
