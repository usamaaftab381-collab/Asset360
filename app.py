import streamlit as st
import sqlite3
import qrcode
from io import BytesIO
from PIL import Image
import pandas as pd

# Database
conn = sqlite3.connect("assets.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS assets(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tag_number TEXT,
    asset_name TEXT,
    category TEXT,
    location TEXT,
    status TEXT
)
""")
conn.commit()


st.set_page_config(page_title="Asset360", page_icon="📦")

st.title("📦 Asset360")
st.subheader("Fixed Asset Management System")


menu = st.sidebar.selectbox(
    "Menu",
    ["Dashboard", "Add Asset", "Asset Register"]
)


# Dashboard
if menu == "Dashboard":

    total = c.execute(
        "SELECT COUNT(*) FROM assets"
    ).fetchone()[0]

    st.header("Dashboard")
    st.metric("Total Assets", total)


# Add Asset
elif menu == "Add Asset":

    st.header("➕ Add New Asset")

    tag = st.text_input("Asset Tag Number")
    name = st.text_input("Asset Name")
    category = st.text_input("Category")
    location = st.text_input("Location")
    status = st.selectbox(
        "Status",
        ["Active","Missing","Damaged","Disposed"]
    )


    if st.button("Save Asset"):

        c.execute("""
        INSERT INTO assets
        (tag_number,asset_name,category,location,status)
        VALUES(?,?,?,?,?)
        """,
        (tag,name,category,location,status))

        conn.commit()

        st.success("Asset Saved Successfully")


        # QR Generation
        qr = qrcode.make(
            f"Asset360:{tag}"
        )

        buffer = BytesIO()
        qr.save(buffer)

        st.image(
            buffer.getvalue(),
            caption="Asset QR Code"
        )

        st.download_button(
            "Download QR",
            buffer.getvalue(),
            file_name=f"{tag}.png"
        )


# Register
elif menu == "Asset Register":

    st.header("📋 Asset Register")

    data = pd.read_sql_query(
        "SELECT * FROM assets",
        conn
    )

    st.dataframe(data)

    csv = data.to_csv(index=False)

    st.download_button(
        "Export Excel CSV",
        csv,
        "asset_register.csv"
    )    name = st.text_input("Asset Name")
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
