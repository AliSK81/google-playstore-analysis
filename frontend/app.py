import streamlit as st

from filters import load_filters


def app():
    load_filters()

    pages = [
        st.Page("search_apps.py", title="🔍 Search Apps"),
        st.Page("rating_distribution.py", title="📊 Rating Distribution"),
        st.Page("release_trend.py", title="📈 App Release Trend"),
        st.Page("average_rating.py", title="⭐ Average Rating per Category")
    ]

    page = st.navigation(pages)
    page.run()


if __name__ == "__main__":
    app()
