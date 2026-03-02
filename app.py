import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Bayut Studios | Price Calculator", layout="centered")

# 2. Premium Design: Pitch Black, Moving Stars, & White Labels
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@200;400;700&display=swap');

    /* Pitch Black Background */
    .stApp {
        background-color: #000000;
        color: white !important;
        font-family: 'Montserrat', sans-serif;
    }

    /* Forced White Labels for Dropdowns */
    label, .stMarkdown p, .stExpander p {
        color: #FFFFFF !important;
        font-weight: 400 !important;
        letter-spacing: 1px;
    }

    /* Sexy Glistening Moving Stars */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background-image: 
            radial-gradient(2px 2px at 20px 30px, #ffffff, rgba(0,0,0,0)),
            radial-gradient(2px 2px at 150px 150px, #37b36f, rgba(0,0,0,0)),
            radial-gradient(2px 2px at 300px 100px, #ffffff, rgba(0,0,0,0)),
            radial-gradient(3px 3px at 450px 400px, #37b36f, rgba(0,0,0,0)),
            radial-gradient(2px 2px at 600px 250px, #ffffff, rgba(0,0,0,0));
        background-repeat: repeat;
        background-size: 600px 600px;
        opacity: 0.8;
        animation: stars-move 80s linear infinite;
        z-index: -1;
    }

    @keyframes stars-move {
        from { background-position: 0 0; }
        to { background-position: 0 -10000px; }
    }

    /* Add To Estimate Button Style */
    div.stButton > button {
        background: linear-gradient(135deg, #1a6b4a 0%, #37b36f 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        font-weight: 700 !important;
        padding: 0.8rem 2rem !important;
        box-shadow: 0 10px 25px rgba(55, 179, 111, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Logo & Premium Heading
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("https://i.ibb.co/LzsV9Z6j/f774cc00-9f2e-4130-9644-1bddb2d6ae50.jpg", use_container_width=True)
st.markdown("<h2 style='text-align: center; color: white; letter-spacing: 8px; font-weight: 200;'>Price Calculator</h2>", unsafe_allow_html=True)

# 4. Cart Logic
if 'cart' not in st.session_state:
    st.session_state.cart = []

# 5. Data Connection
url = "https://docs.google.com/spreadsheets/d/1qvBKlYH7q4dXsu7tEh9OLnKSydfONNRzGa-xjUYLB0g/edit?usp=sharing"

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(spreadsheet=url, ttl="1m")

    # CLEANING COLUMN NAMES (Resolves the Syncing Error)
    # We strip spaces to ensure a perfect match
    df.columns = [c.strip() for c in df.columns]

    cat_col = "Product Category"
    prod_col = "Product"
    pkr_col = "Total Price (PKR)"
    sar_col = "Total Price (SAR)"
    aed_col = "Total Price (AED)"

    def clean_num(val):
        if isinstance(val, str):
            return float(val.replace('PKR','').replace('SAR','').replace('dh','').replace(',','').strip())
        return float(val)

    # 6. User Selection UI
    with st.expander("➕ ADD SERVICES TO PROJECT", expanded=True):
        category = st.selectbox("Select Product Category", df[cat_col].unique())
        sub_df = df[df[cat_col] == category]
        
        product = st.selectbox("Select Product Name", sub_df[prod_col].unique())
        units = st.number_input("Total Units Required", min_value=1, value=1)
        
        if st.button("ADD TO ESTIMATE"):
            row = sub_df[sub_df[prod_col] == product].iloc[0]
            st.session_state.cart.append({
                "name": product, "units": units,
                "pkr": clean_num(row[pkr_col]) * units,
                "sar": clean_num(row[sar_col]) * units,
                "aed": clean_num(row[aed_col]) * units
            })
            st.rerun()

    # 7. Final Results
    if st.session_state.cart:
        totals = {"pkr": 0, "sar": 0, "aed": 0}
        st.markdown("---")
        for i, item in enumerate(st.session_state.cart):
            totals["pkr"] += item["pkr"]
            totals["sar"] += item["sar"]
            totals["aed"] += item["aed"]
            st.write(f"**{item['name']}** (x{item['units']}) — PKR {item['pkr']:,.0f}")

        # Luxury Result Card
        st.markdown(f"""
            <div style="border: 2px solid #37b36f; padding: 40px; border-radius: 20px; background: rgba(55, 179, 111, 0.1); text-align: center; margin-top: 30px;">
                <p style="letter-spacing: 4px; color: white; opacity: 0.7;">GRAND TOTAL ESTIMATE</p>
                <h1 style="color: white; font-size: 3.5rem;">PKR {totals['pkr']:,.0f}</h1>
                <div style="display: flex; justify-content: center; gap: 40px; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 20px;">
                    <div><p style="color: #37b36f; font-size: 0.8rem;">SAR (SAUDI)</p><h2 style="color:white;">{totals['sar']:,.2f}</h2></div>
                    <div><p style="color: #37b36f; font-size: 0.8rem;">AED (DUBAI)</p><h2 style="color:white;">{totals['aed']:,.2f}</h2></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"Syncing Error: {e}")
