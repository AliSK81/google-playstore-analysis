import matplotlib.pyplot as plt
import pandas as pd
import requests
import streamlit as st

api_url = "http://127.0.0.1:8000"


def fetch_filters():
    response = requests.get(f"{api_url}/filters")
    if response.status_code == 200:
        return response.json()
    return {}


def fetch_apps(filters):
    response = requests.get(f"{api_url}/apps", params=filters)
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    return pd.DataFrame()


def fetch_free_apps_in_social():
    response = requests.get(f"{api_url}/apps/free/social")
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    return pd.DataFrame()


def fetch_release_trend(category):
    response = requests.get(f"{api_url}/apps/release_trend/{category}")
    if response.status_code == 200:
        return response.json()
    return []


def fetch_average_rating(category):
    response = requests.get(f"{api_url}/apps/average_rating/{category}")
    if response.status_code == 200:
        return response.json()
    return {}


st.set_page_config(page_title="Google Play Store Data Analytics", layout="wide")
st.title("📊 Google Play Store Data Analytics")

filters_data = fetch_filters()

categories = filters_data.get("categories", [])
content_ratings = filters_data.get("content_ratings", [])
min_rating = filters_data.get("min_rating", 0.0)
max_rating = filters_data.get("max_rating", 5.0)
min_price = filters_data.get("min_price", 0.0)
max_price = filters_data.get("max_price", 100.0)
min_installs = filters_data.get("min_installs", 0)
max_installs = filters_data.get("max_installs", 10000000)

col1, col2 = st.columns(2)

with col1:
    category = st.selectbox("📂 Select Category", ["All"] + categories)
    min_rating = st.slider("⭐ Minimum Rating", min_rating, max_rating, min_rating)
    max_rating = st.slider("⭐ Maximum Rating", min_rating, max_rating, max_rating)
    min_price = st.number_input("💰 Minimum Price ($)", min_value=min_price, value=min_price, step=1.0)
    max_price = st.number_input("💰 Maximum Price ($)", min_value=min_price, value=max_price, step=1.0)

with col2:
    min_installs = st.number_input("📥 Minimum Installs", min_value=min_installs, value=min_installs, step=100)
    max_installs = st.number_input("📥 Maximum Installs", min_value=min_installs, value=max_installs, step=100)
    content_rating = st.selectbox("🔞 Content Rating", ["All"] + content_ratings)
    free_only = st.checkbox("🆓 Show Only Free Apps")
    has_ads = st.checkbox("📢 Apps with Ads")
    has_in_app_purchases = st.checkbox("💵 Apps with In-App Purchases")
    editors_choice = st.checkbox("🏆 Editors' Choice")
    limit = st.number_input("📝 Results Limit", min_value=1, max_value=5000, value=1000, step=100)

filters = {
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

filtered_df = fetch_apps(filters)

st.subheader("Filtered Apps")
st.dataframe(filtered_df)

if not filtered_df.empty:
    st.subheader("📊 Data Visualizations")

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("### ⭐ Rating Distribution")
        fig, ax = plt.subplots(figsize=(6, 4))
        filtered_df["rating"].hist(bins=20, ax=ax, color="blue", alpha=0.7)
        ax.set_xlabel("Rating")
        ax.set_ylabel("Count")
        st.pyplot(fig)

    with col4:
        st.markdown("### 📅 App Release Trend")
        category = st.selectbox("Select Category for Release Trend", categories)
        release_trend = fetch_release_trend(category)
        years = [entry["year"] for entry in release_trend]
        counts = [entry["count"] for entry in release_trend]
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(years, counts, marker="o", color="green")
        ax.set_xlabel("Year")
        ax.set_ylabel("Number of Apps Released")
        st.pyplot(fig)

    st.markdown("### 📊 Average Rating per Category")
    category = st.selectbox("Select Category for Average Rating", categories)
    average_rating = fetch_average_rating(category)
    st.write(f"Average Rating for {category}: {average_rating.get('average_rating', 'Not available')}")
