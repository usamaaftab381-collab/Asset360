import streamlit as st
import sqlite3
import pandas as pd
import qrcode

st.title("📦 Asset360")
st.header("Fixed Asset Management System")

st.header("Add Asset")

name = st.text_input("Asset Name")
category = st.text_input("Category")
