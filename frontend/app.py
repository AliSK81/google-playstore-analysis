import streamlit as st

from filters import load_filters


def app():
    load_filters()

    pages = [
        st.Page("manage_categories_page.py", title="📂 Categories Management"),
        st.Page("manage_developers_page.py", title="👨‍💻 Developers Management"),
        st.Page("manage_apps_page.py", title="📱 Apps Management"),
        st.Page("search_apps_page.py", title="🔍 Search Apps"),
        st.Page("rating_distribution_page.py", title="📊 Rating Distribution"),
        st.Page("release_trend_page.py", title="📈 App Release Trend"),
        st.Page("update_trend_page.py", title="🆕 App Update Trend"),
        st.Page("average_rating_page.py", title="⭐ Average Rating per Category")
    ]

    page = st.navigation(pages)
    page.run()


if __name__ == "__main__":
    app()
