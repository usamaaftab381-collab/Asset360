import streamlit as st
import sqlite3
import pandas as pd
import qrcode
from io import BytesIO

st.set_page_config(
    page_title="Asset360",
    page_icon="📦",
    layout="wide"
)

# Database
conn = sqlite3.connect("assets.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS assets(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
category TEXT,
location TEXT,
qr TEXT
)
""")

conn.commit()


def generate_qr(data):
    img = qrcode.make(data)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()


st.title("📦 Asset360")
st.subheader("Fixed Asset Management System")


menu = st.sidebar.selectbox(
    "Menu",
    ["Dashboard", "Add Asset", "Search Asset"]
)


# Dashboard
if menu == "Dashboard":

    st.header("📊 Dashboard")

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

    st.header("➕ Add Asset")

    name = st.text_input("Asset Name")

    category = st.text_input(
        "Category"
    )

    location = st.text_input(
        "Location"
    )


    if st.button("Save Asset"):

        qr_text = f"{name}-{category}-{location}"

        c.execute(
            """
            INSERT INTO assets
            (name,category,location,qr)
            VALUES (?,?,?,?)
            """,
            (
                name,
                category,
                location,
                qr_text
            )
        )

        conn.commit()

        st.success(
            "Asset Added Successfully"
        )


        qr_image = generate_qr(qr_text)

        st.image(
            qr_image,
            caption="Asset QR Code"
        )


# Search
elif menu == "Search Asset":

    st.header("🔍 Search Asset")

    search = st.text_input(
        "Enter Asset Name"
    )

    if search:

        df = pd.read_sql(
            f"""
            SELECT * FROM assets
            WHERE name LIKE '%{search}%'
            """,
            conn
        )

        st.dataframe(df)
