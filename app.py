import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Page Config
st.set_page_config(page_title="Bayut Studios | Price Calculator", layout="centered")

# 2. Premium Dark Styling
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    h1, h2, h3 { color: #37b36f !important; text-align: center; font-family: sans-serif; }
    .stSelectbox label, .stNumberInput label { color: white !important; }
    div[data-baseweb="select"] { background-color: #111 !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. Logo & Title
st.image("https://i.ibb.co/LzsV9Z6j/f774cc00-9f2e-4130-9644-1bddb2d6ae50.jpg")
st.markdown("### PRICE CALCULATOR")

# 4. Connect to your Google Sheet
url = "https://docs.google.com/spreadsheets/d/1qvBKlYH7q4dXsu7tEh9OLnKSydfONNRzGa-xjUYLB0g/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

# Read the data (Skipping the first row if it's just a title)
df = conn.read(spreadsheet=url, worksheet="Calculator Values", ttl="1m")

# Clean price columns (Removing 'PKR' and commas so math works)
def clean_currency(value):
    if isinstance(value, str):
        return float(value.replace('PKR', '').replace(',', '').strip())
    return value

# 5. User Interface
category = st.selectbox("Product Category", df['Product Category'].unique())
filtered_df = df[df['Product Category'] == category]

product = st.selectbox("Select Product", filtered_df['Product'].unique())
units = st.number_input("Units Required", min_value=1, value=1)

# 6. Logic & Display
selected_row = filtered_df[filtered_df['Product'] == product].iloc[0]
raw_price = clean_currency(selected_row['Total Price (PKR)'])
total_cost = raw_price * units

st.markdown(f"""
    <div style="border: 2px solid #37b36f; padding: 30px; border-radius: 15px; text-align: center; background: rgba(55, 179, 111, 0.05); margin-top: 20px;">
        <p style="color: #aaa; margin-bottom: 5px;">Total Estimated Cost</p>
        <h1 style="font-size: 3.5rem; margin: 0;">PKR {total_cost:,.0f}</h1>
        <p style="color: #37b36f; margin-top: 10px;">Service: {product}</p>
    </div>
    """, unsafe_allow_html=True)
