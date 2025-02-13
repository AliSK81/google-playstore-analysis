import streamlit as st

from utils import fetch_data


def fetch_filters():
    filters_data = fetch_data("filters")
    return filters_data if filters_data else {}


def load_filters():
    if "filters_data" not in st.session_state:
        st.session_state.filters_data = fetch_filters()


def get_filter_default_values():
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


def get_filters(show_category=False, show_rating=False, show_price=False, show_installs=False,
                show_content_rating=False,
                show_free_only=False, show_ads=False, show_in_app=False, show_editors_choice=False, show_limits=False):
    categories, content_ratings, min_rating, max_rating, min_price, max_price, min_installs, max_installs \
        = get_filter_default_values()

    filters = {}

    if show_category:
        category = st.selectbox("📂 Select Category", ["All"] + categories)
        filters["category"] = None if category == "All" else category

    if show_rating:
        filters["min_rating"], filters["max_rating"] = st.slider(
            "⭐ Rating Range",
            min_value=min_rating,
            max_value=max_rating,
            value=(min_rating, max_rating),
            step=0.1
        )

    if show_price:
        filters["min_price"], filters["max_price"] = st.slider(
            "💰 Price Range ($)",
            min_value=min_price,
            max_value=max_price,
            value=(min_price, max_price),
            step=0.1
        )

    if show_installs:
        filters["min_installs"] = st.number_input("📥 Minimum Installs", min_value=min_installs, value=min_installs,
                                                  step=100)
        filters["max_installs"] = st.number_input("📥 Maximum Installs", min_value=min_installs, value=max_installs,
                                                  step=100)

    if show_content_rating:
        content_rating = st.selectbox("🔞 Content Rating", ["All"] + content_ratings)
        filters["content_rating"] = None if content_rating == "All" else content_rating

    if show_free_only:
        filters["free"] = st.checkbox("🆓 Show Only Free Apps")

    if show_ads:
        filters["ad_supported"] = st.checkbox("📢 Apps with Ads")

    if show_in_app:
        filters["in_app_purchases"] = st.checkbox("💵 Apps with In-App Purchases")

    if show_editors_choice:
        filters["editors_choice"] = st.checkbox("🏆 Editors' Choice")

    if show_limits:
        filters["limit"] = st.number_input("📝 Results Limit", min_value=1, max_value=5000, value=1000, step=100)

    return filters
