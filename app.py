import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Bayut Studios | Price Calculator", layout="centered")

# 2. Premium Dark Styling
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    h1, h2, h3 { color: #37b36f !important; text-align: center; }
    .stSelectbox label, .stNumberInput label { color: white !important; }
    /* Style the dropdown boxes */
    div[data-baseweb="select"] > div { background-color: #111 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. Logo & Title
st.image("https://i.ibb.co/LzsV9Z6j/f774cc00-9f2e-4130-9644-1bddb2d6ae50.jpg")
st.markdown("### PRICE CALCULATOR")

# 4. Connect to Google Sheets (CLEANED URL)
# The .strip() at the end removes any accidental hidden spaces
raw_url = "https://docs.google.com/spreadsheets/d/1qvBKlYH7q4dXsu7tEh9OLnKSydfONNRzGa-xjUYLB0g/edit?usp=sharing"
url = raw_url.strip() 

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    # We load the data. Note: worksheet name must match your sheet tab exactly!
    df = conn.read(spreadsheet=url, ttl="1m")

    # 5. User Interface
    # Using 'Product Category' because that is the column name in your sheet
    category = st.selectbox("Product Category", df['Product Category'].unique())
    filtered_df = df[df['Product Category'] == category]

    product = st.selectbox("Select Product", filtered_df['Product'].unique())
    units = st.number_input("Units Required", min_value=1, value=1)

    # 6. Calculation Logic
    selected_row = filtered_df[filtered_df['Product'] == product].iloc[0]
    
    # Cleaning the price string (PKR 172,023 -> 172023)
    raw_price = str(selected_row['Total Price (PKR)'])
    clean_price = float(raw_price.replace('PKR', '').replace(',', '').strip())
    
    total_cost = clean_price * units

    # 7. Display Result
    st.markdown(f"""
        <div style="border: 2px solid #37b36f; padding: 30px; border-radius: 15px; text-align: center; background: rgba(55, 179, 111, 0.05); margin-top: 20px;">
            <p style="color: #aaa; margin-bottom: 5px;">Total Estimated Cost</p>
            <h1 style="font-size: 3.5rem; margin: 0; color: #37b36f;">PKR {total_cost:,.0f}</h1>
        </div>
        """, unsafe_allow_html=True)

except Exception as e:
    st.error("Connection Error: Please ensure the Google Sheet is set to 'Anyone with the link can view'.")
    st.info(f"Technical details: {e}")
