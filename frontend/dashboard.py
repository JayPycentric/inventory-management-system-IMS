from time import sleep

import streamlit as st
from client import create_product, get_metrics

st.set_page_config(
    page_title="Inventory Management System",
    page_icon="📦",
    layout="wide",
)

st.title("Inventory Management System")
st.divider()


def display_metrics() -> None:
    try:
        metrics = get_metrics()

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                label="Total Products",
                value=metrics["total_products"],
            )

        with col2:
            st.metric(
                label="Asset Valuation",
                value=f"R {metrics['total_value']:,.2f}",
            )

        with col3:
            st.metric(
                label="Out of Stock",
                value=metrics["out_of_stock_products"],
            )

    except Exception as e:
        st.error(f"Failed to load metrics: {e}")


def display_create_form() -> None:
    st.subheader("Add New Product")

    with st.form(key="create_product_form"):
        name = st.text_input("Product Name")
        price = st.number_input("Price (R)", min_value=0.01, step=0.01)
        stock = st.number_input("Stock", min_value=0, step=1)
        category = st.text_input("Category")

        submitted = st.form_submit_button("Add Product")

        if submitted:
            if not name or not category:
                st.error("Name and category are required.")
                return

            try:
                create_product(
                    {
                        "name": name,
                        "price": price,
                        "stock": stock,
                        "category": category,
                    }
                )
                st.success(f"{name} added successfully.")
                sleep(2)
                st.rerun()

            except Exception as e:
                st.error(f"Failed to create product: {e}")


display_metrics()
st.divider()
display_create_form()
