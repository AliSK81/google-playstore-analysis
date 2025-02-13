import pandas as pd
import streamlit as st

from filters import get_filter_values
from utils import fetch_data


def fetch_apps(filters):
    data = fetch_data("apps", filters)
    return pd.DataFrame(data) if data else pd.DataFrame()


st.subheader("Search Apps")

(categories, content_ratings, min_rating, max_rating, min_price, max_price, min_installs,
 max_installs) = get_filter_values()

with st.sidebar:
    content_rating = None
    free_only = has_ads = has_in_app_purchases = editors_choice = False
    limit = 1000

    category = st.selectbox("📂 Select Category", ["All"] + categories)

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
if not filtered_df.empty:
    st.dataframe(filtered_df)
else:
    st.warning("No apps found with the current filters.")
