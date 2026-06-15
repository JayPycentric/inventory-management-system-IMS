import streamlit as st
from client import (
    create_product,
    delete_product,
    get_all_products,
    get_metrics,
    get_products_by_category,
    restock_product,
    search_products,
    update_product,
)

st.set_page_config(
    page_title="Inventory Management System",
    page_icon="📦",
    layout="wide",
)

title_col, spacer_col, logo_col = st.columns([17, 2, 1], vertical_alignment="center")
with title_col:
    st.title("Inventory Management System")

with logo_col:
    st.image(
        "frontend/resources/inventory.png",
        width="stretch",
    )


def display_metrics() -> None:
    st.subheader("Products Metrics")
    try:
        metrics = get_metrics()

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                label=":orange[Total Products]",
                value=metrics["total_products"],
            )

        with col2:
            st.metric(
                label=":orange[Asset Valuation]",
                value=f"R {metrics['total_value']:,.2f}",
            )

        with col3:
            st.metric(
                label=":orange[Out of Stock]",
                value=metrics["out_of_stock_products"],
            )

    except Exception as e:
        st.error(f"Failed to load metrics: {e}")


def display_create_form() -> None:
    st.subheader("Add New Product")

    with st.form(key="create_product_form"):
        name = st.text_input(":orange[Product Name]")
        price = st.number_input(":orange[Price (R)]", min_value=0.01, step=0.01)
        stock = st.number_input(":orange[Stock]", min_value=0, step=1)
        category = st.text_input(":orange[Category]")

        submitted = st.form_submit_button("Add Product", type="primary")

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
                st.toast(f"{name} added successfully.")
                st.rerun()

            except Exception as e:
                st.error(f"Failed to create product: {e}")


def display_edit_form(product: dict) -> None:
    st.subheader(f"Edit {product['name']}")

    with st.form(key=f"edit_form_{product['id']}"):
        name = st.text_input("Name", value=product["name"])
        price = st.number_input(
            "Price (R)",
            value=product["price"],
            min_value=0.01,
            step=0.01,
        )
        stock = st.number_input(
            "Stock",
            value=product["stock"],
            min_value=0,
            step=1,
        )
        category = st.text_input("Category", value=product["category"])

        submitted = st.form_submit_button("Update")

        if submitted:
            try:
                update_product(
                    product["id"],
                    {
                        "name": name,
                        "price": price,
                        "stock": stock,
                        "category": category,
                    },
                )
                st.toast(f"{product['name']} updated.")
                st.rerun()
            except Exception as e:
                st.error(f"Failed to update: {e}")


def display_product_actions(product: dict) -> None:
    btn1, btn2, btn3 = st.columns(3)

    with btn1:
        if st.button(
            "Restock",
            key=f"restock_{product['id']}",
            width="stretch",
            type="primary",
        ):
            try:
                restock_product(product["id"])
                st.toast(f"{product['name']} restocked successfully.")
                st.rerun()
            except Exception as e:
                st.error(f"Failed to restock: {e}")

    with btn2:
        with st.popover("Edit", width="stretch"):
            display_edit_form(product)

    with btn3:
        with st.popover("Delete", width="stretch"):
            st.warning(f"Delete **{product['name']}**?")
            if st.button(
                "Yes, Delete",
                key=f"confirm_delete_{product['id']}",
                type="primary",
            ):
                try:
                    delete_product(product["id"])
                    st.toast(f"{product['name']} deleted.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to delete: {e}")


def display_product_row(product: dict) -> None:
    with st.container(border=True):
        col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 3])

        with col1:
            st.caption(":orange[**Name / SKU**]")
            st.write(f"**{product['name']}**")
            st.caption(f":red[{product['sku']}]")

        with col2:
            st.caption(":orange[**Price**]")
            st.write(f"R {product['price']:,.2f}")

        with col3:
            st.caption(":orange[**Stock**]")
            st.write(f"Stock: {product['stock']}")

        with col4:
            st.caption(":orange[**Category**]")
            st.write(product["category"])

        with col5:
            st.caption(":orange[**Actions**]")
            display_product_actions(product)


def get_categories(products: list[dict]) -> list[str]:
    return sorted({product["category"] for product in products})


def display_search_and_filter(products: list[dict]) -> tuple[str, str]:
    col1, col2 = st.columns(2)

    with col1:
        search_term = st.text_input(
            "Search by Name or SKU",
            placeholder="e.g. Keyboard or ELEC-KBD-9042",
        )

    with col2:
        categories = ["All"] + get_categories(products)
        selected_category = st.selectbox("Filter by Category", options=categories)

    return search_term, selected_category


def display_products(search_term: str = "", category: str = "All") -> None:
    st.subheader("Products")
    try:
        if search_term:
            if "-" in search_term:
                products = search_products(sku=search_term)
            else:
                products = search_products(name=search_term)
        elif category != "All":
            products = get_products_by_category(category)
        else:
            products = get_all_products()

        if not products:
            st.info("No products found.")
            return

        for product in products:
            display_product_row(product)

    except Exception as e:
        st.error(f"Failed to load products: {e}")


if "success_message" in st.session_state:
    st.success(st.session_state["success_message"])
    del st.session_state["success_message"]

display_metrics()
st.divider()

all_products = get_all_products()
search_term, selected_category = display_search_and_filter(all_products)

display_products(search_term=search_term, category=selected_category)
st.divider()
display_create_form()
