from time import sleep

import streamlit as st
from client import create_product, get_all_products, get_metrics

st.set_page_config(
    page_title="Inventory Management System",
    page_icon="📦",
    layout="wide",
)

st.title("Inventory Management System")
st.divider()


def display_metrics() -> None:
    st.subheader("Products Metrics")
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


def display_products() -> None:
    st.subheader("Products")
    try:
        products = get_all_products()
        if not products:
            st.info("No products found.")
            return

        header1, header2, header3, header4 = st.columns([3, 2, 2, 2])
        with header1:
            st.markdown(":orange[**Name / SKU**]")
        with header2:
            st.markdown(":orange[**Price**]")
        with header3:
            st.markdown(":orange[**Stock**]")
        with header4:
            st.markdown(":orange[**Category**]")

        for product in products:
            with st.container(border=True):
                col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
                with col1:
                    st.write(f"**{product['name']}**")
                    st.caption(f":red[{product['sku']}]")
                with col2:
                    st.write(f"R {product['price']:,.2f}")
                with col3:
                    st.write(f"Stock: {product['stock']}")
                with col4:
                    st.write(product["category"])

    except Exception as e:
        st.error(f"Failed to load products: {e}")


display_metrics()
st.divider()
display_products()
st.divider()
display_create_form()
