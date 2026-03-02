import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Bayut Studios | Price Calculator", layout="centered")

# Header & Logo
st.image("https://i.ibb.co/LzsV9Z6j/f774cc00-9f2e-4130-9644-1bddb2d6ae50.jpg")
st.markdown("### PRICE CALCULATOR")

url = "https://docs.google.com/spreadsheets/d/1qvBKlYH7q4dXsu7tEh9OLnKSydfONNRzGa-xjUYLB0g/edit?usp=sharing"

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    # Read the data
    df = conn.read(spreadsheet=url, ttl="1m")
    
    # DEBUG: This line helps us see what the code actually "sees" in your sheet
    # st.write("Columns found:", df.columns.tolist()) 

    # We use a flexible way to find your columns
    # This looks for any column that contains the word 'Category'
    cat_col = [c for c in df.columns if 'Category' in c][0]
    prod_col = [c for c in df.columns if 'Product' in c and 'Category' not in c][0]
    price_col = [c for c in df.columns if 'Price' in c and 'PKR' in c][0]

    # User Selection
    category = st.selectbox("Select Category", df[cat_col].unique())
    filtered_df = df[df[cat_col] == category]

    product = st.selectbox("Select Product", filtered_df[prod_col].unique())
    units = st.number_input("Units Required", min_value=1, value=1)

    # Calculation
    selected_row = filtered_df[filtered_df[prod_col] == product].iloc[0]
    
    # Clean the price string
    raw_price = str(selected_row[price_col])
    clean_price = float(raw_price.replace('PKR', '').replace(',', '').strip())
    total_cost = clean_price * units

    st.markdown(f"""
        <div style="border: 2px solid #37b36f; padding: 20px; border-radius: 10px; text-align: center; background: rgba(55, 179, 111, 0.1);">
            <h2 style="margin:0; color: white;">Total Estimated Cost</h2>
            <h1 style="font-size: 3rem; color: #37b36f;">PKR {total_cost:,.0f}</h1>
        </div>
        """, unsafe_allow_html=True)

except Exception as e:
    st.error("We couldn't read your sheet correctly.")
    st.info(f"The error is: {e}")
    st.write("Please check that your Google Sheet has headers in the first row.")
