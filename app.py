import streamlit as st
import sqlite3
import pandas as pd
import qrcode
from io import BytesIO

st.set_page_config(
    page_title="Asset360",
    page_icon="📦"
)

# Fresh database
conn = sqlite3.connect(":memory:", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE assets(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    category TEXT,
    location TEXT,
    qr TEXT
)
""")

conn.commit()


def create_qr(data):
    qr = qrcode.make(data)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    return buffer.getvalue()


st.title("📦 Asset360")
st.header("Fixed Asset Management System")


menu = st.sidebar.selectbox(
    "Menu",
    [
        "Dashboard",
        "Add Asset",
        "Search Asset"
    ]
)


# Dashboard
if menu == "Dashboard":

    st.subheader("📊 Dashboard")

    df = pd.read_sql(
        "SELECT * FROM assets",
        conn
    )

    st.metric(
        "Total Assets",
        len(df)
    )

    if len(df) > 0:
        st.dataframe(df)


# Add Asset
elif menu == "Add Asset":

    st.subheader("➕ Add Asset")

    asset_name = st.text_input(
        "Asset Name"
    )

    category = st.text_input(
        "Category"
    )

    location = st.text_input(
        "Location"
    )


    if st.button("Save Asset"):

        qr_data = (
            asset_name
            + " | "
            + category
            + " | "
            + location
        )

        c.execute(
            """
            INSERT INTO assets
            (name, category, location, qr)
            VALUES (?, ?, ?, ?)
            """,
            (
                asset_name,
                category,
                location,
                qr_data
            )
        )

        conn.commit()

        st.success(
            "Asset Saved Successfully"
        )


        qr_image = create_qr(
            qr_data
        )

        st.image(
            qr_image,
            caption="Asset QR Code"
        )


# Search
elif menu == "Search Asset":

    st.subheader("🔍 Search Asset")

    search = st.text_input(
        "Search by Asset Name"
    )


    if search:

        df = pd.read_sql(
            """
            SELECT * FROM assets
            WHERE name LIKE ?
            """,
            conn,
            params=(
                "%" + search + "%",
            )
        )

        st.dataframe(df)
