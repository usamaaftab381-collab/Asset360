import streamlit as st
import sqlite3
import pandas as pd
import qrcode
from io import BytesIO

# Database
conn = sqlite3.connect("assets.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS assets(
id INTEGER PRIMARY KEY,
asset_name TEXT,
category TEXT,
location TEXT,
status TEXT
)
""")
conn.commit()

st.set_page_config(page_title="Asset360", layout="wide")

st.title("📦 Asset360")
st.subheader("Fixed Asset Management System")

menu = st.sidebar.selectbox(
    "Menu",
    ["Dashboard", "Add Asset", "Asset Register", "QR Generator"]
)

# Add Asset
if menu == "Add Asset":

    st.header("Add New Asset")

    name = st.text_input("Asset Name")
    category = st.text_input("Category")
    location = st.text_input("Location")
    status = st.selectbox(
        "Status",
        ["Active","Missing","Damaged","Disposed"]
    )

    if st.button("Save Asset"):

        c.execute(
        "INSERT INTO assets(asset_name,category,location,status) VALUES(?,?,?,?)",
        (name,category,location,status)
        )

        conn.commit()
        st.success("Asset Added Successfully")


# Register
elif menu == "Asset Register":

    st.header("Asset Register")

    df = pd.read_sql(
        "SELECT * FROM assets",
        conn
    )

    st.dataframe(df)


# Dashboard
elif menu == "Dashboard":

    st.header("Dashboard")

    total = c.execute(
        "SELECT COUNT(*) FROM assets"
    ).fetchone()[0]

    st.metric(
        "Total Assets",
        total
    )


# QR Generator
elif menu == "QR Generator":

    st.header("Generate Asset QR")

    asset_id = st.text_input("Enter Asset ID")

    if st.button("Create QR"):

        qr = qrcode.make(
            f"Asset360 Asset ID: {asset_id}"
        )

        buffer = BytesIO()
        qr.save(buffer)

        st.image(buffer.getvalue())
