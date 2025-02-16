import time

import pandas as pd
import streamlit as st

from client_api import fetch_categories, create_category, update_category, delete_category


def create_category_page():
    st.subheader("Create New Category")
    category_name = st.text_input("Category Name")
    if st.button("Create Category"):
        data = create_category(category_name)
        if data:
            st.success(f"Category '{category_name}' created successfully!")
            time.sleep(1)
            st.rerun()
        else:
            st.error("Failed to create category.")


def list_categories_page():
    st.subheader("Manage Categories")

    categories = fetch_categories()

    if not categories:
        st.warning("No categories found.")
        return

    category_df = pd.DataFrame(categories)

    col1, col2 = st.columns([6, 1])

    with col1:
        st.write("**Existing Categories**")

    with col2:
        st.write("**Actions**")

    for index, row in category_df.iterrows():
        col1, col2, col3 = st.columns([9, 1, 1])

        with col1:
            st.write(f"📂 {row['name']}")

        with col2:
            edit_button = st.button("✏️", key=f"edit_{row['id']}")
        with col3:
            delete_button = st.button("❌", key=f"delete_{row['id']}")

        if edit_button:
            st.session_state['edit_mode'] = True
            st.session_state['edit_id'] = row['id']
            st.session_state['edit_name'] = row['name']
            st.rerun()

        if delete_button:
            delete_category_page(row['id'])


def edit_category_page():
    if "edit_mode" in st.session_state and st.session_state["edit_mode"]:
        st.subheader(f"Edit Category: {st.session_state['edit_name']}")
        new_name = st.text_input("New Category Name", value=st.session_state['edit_name'])
        if st.button("Update Category"):
            data = update_category(st.session_state['edit_id'], new_name)
            if data:
                st.success(f"Category '{st.session_state['edit_name']}' updated successfully!")
                time.sleep(1)
                del st.session_state['edit_mode']
                del st.session_state['edit_id']
                del st.session_state['edit_name']
                st.rerun()
            else:
                st.error("Failed to update category.")


def delete_category_page(category_id):
    if delete_category(category_id):
        st.success("Category deleted successfully!")
        time.sleep(1)
        st.rerun()
    else:
        st.error("Failed to delete category.")


def categories_page():
    st.title("Categories Management")

    tab1, tab2 = st.tabs(["Create Category", "Manage Categories"])

    with tab1:
        create_category_page()

    with tab2:
        if "edit_mode" in st.session_state and st.session_state["edit_mode"]:
            edit_category_page()
        else:
            list_categories_page()


categories_page()
