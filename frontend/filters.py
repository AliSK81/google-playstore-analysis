import streamlit as st

from data_fetcher import fetch_filters


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
        min_rating_input, max_rating_input = st.slider(
            "⭐ Rating Range",
            min_value=min_rating,
            max_value=max_rating,
            value=(min_rating, max_rating),
            step=0.1
        )
        filters["min_rating"] = None if min_rating_input == min_rating else min_rating_input
        filters["max_rating"] = None if max_rating_input == max_rating else max_rating_input

    if show_price:
        min_price_input, max_price_input = st.slider(
            "💰 Price Range ($)",
            min_value=min_price,
            max_value=max_price,
            value=(min_price, max_price),
            step=0.1
        )
        filters["min_price"] = None if min_price_input == min_price else min_price_input
        filters["max_price"] = None if max_price_input == max_price else max_price_input

    if show_installs:
        min_installs_input = st.number_input("📥 Minimum Installs", min_value=min_installs, value=min_installs, step=100)
        max_installs_input = st.number_input("📥 Maximum Installs", min_value=min_installs, value=max_installs, step=100)
        filters["min_installs"] = None if min_installs_input == min_installs else min_installs_input
        filters["max_installs"] = None if max_installs_input == max_installs else max_installs_input

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
        limit_size = 1000
        limit_input = st.number_input("📝 Results Limit", min_value=1, max_value=3000000, value=limit_size, step=100)
        filters["limit"] = None if limit_input == limit_size else limit_input

    return filters
