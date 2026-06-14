import streamlit as st
from client import get_metrics

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


display_metrics()
st.divider()
