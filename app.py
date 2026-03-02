import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Bayut Studios | Price Calculator", layout="centered")

# 2. Advanced Design: Starry Depth & UI Fixes
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@200;700;900&display=swap');

    /* Deep Black Background */
    .stApp {
        background-color: #000000;
        color: white !important;
        font-family: 'Montserrat', sans-serif;
    }

    /* FIX: Keep input boxes dark even on focus/hover */
    div[data-baseweb="select"] > div, div[data-baseweb="popover"] > div {
        background-color: #111111 !important;
        color: white !important;
    }
    
    /* White Labels for High Visibility */
    label, .stMarkdown p, .stExpander p {
        color: #FFFFFF !important;
        font-weight: 700 !important;
        letter-spacing: 1.5px;
    }

    /* Ultra-Starry CSS Engine */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background-image: 
            radial-gradient(1px 1px at 25px 35px, #fff, rgba(0,0,0,0)),
            radial-gradient(2px 2px at 50px 120px, #37b36f, rgba(0,0,0,0)),
            radial-gradient(1px 1px at 100px 250px, #fff, rgba(0,0,0,0)),
            radial-gradient(2px 2px at 200px 450px, #fff, rgba(0,0,0,0)),
            radial-gradient(3px 3px at 350px 100px, #37b36f, rgba(0,0,0,0)),
            radial-gradient(1px 1px at 450px 300px, #fff, rgba(0,0,0,0));
        background-size: 400px 400px;
        opacity: 1;
        animation: stars-move 150s linear infinite;
        z-index: -1;
    }

    @keyframes stars-move {
        from { background-position: 0 0; }
        to { background-position: 0 -10000px; }
    }

    /* Bold Price Calculator Header */
    .rich-header {
        text-align: center;
        font-weight: 900;
        letter-spacing: 12px;
        color: #FFFFFF;
        text-transform: uppercase;
        margin: 25px 0;
        text-shadow: 0 0 15px rgba(55, 179, 111, 0.5);
    }

    /* Green Premium Buttons */
    div.stButton > button {
        background: linear-gradient(135deg, #1a6b4a 0%, #37b36f 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 4px !important;
        font-weight: 700 !important;
        letter-spacing: 2px;
        padding: 0.8rem !important;
        width: 100%;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Branding
st.image("https://i.ibb.co/LzsV9Z6j/f774cc00-9f2e-4130-9644-1bddb2d6ae50.jpg")
st.markdown("<h1 class='rich-header'>Price Calculator</h1>", unsafe_allow_html=True)

# 4. Smart Project Memory
if 'cart' not in st.session_state:
    st.session_state.cart = {}

# 5. Data Core
url = "https://docs.google.com/spreadsheets/d/1qvBKlYH7q4dXsu7tEh9OLnKSydfONNRzGa-xjUYLB0g/edit?usp=sharing"

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(spreadsheet=url, ttl="1m")
    df.columns = [c.strip() for c in df.columns] # Clean headers

    cat_col, prod_col, pkr_col, sar_col, aed_col = "Product Category", "Product", "Total Price (PKR)", "Total Price (SAR)", "Total Price (AED)"

    def clean_num(val):
        if isinstance(val, str):
            return float(val.replace('PKR','').replace('SAR','').replace('dh','').replace(',','').strip())
        return float(val)

    # 6. Selection Interface
    with st.expander("CONFIGURE YOUR PROJECT SCOPE", expanded=True):
        category = st.selectbox("CATEGORY", df[cat_col].unique())
        sub_df = df[df[cat_col] == category]
        product = st.selectbox("PRODUCT SERVICE", sub_df[prod_col].unique())
        units = st.number_input("UNITS REQUIRED", min_value=1, value=1)
        
        if st.button("ADD TO QUOTATION"):
            row = sub_df[sub_df[prod_col] == product].iloc[0]
            
            # Logic to merge duplicate products
            if product in st.session_state.cart:
                st.session_state.cart[product]['units'] += units
                st.session_state.cart[product]['pkr'] += clean_num(row[pkr_col]) * units
                st.session_state.cart[product]['sar'] += clean_num(row[sar_col]) * units
                st.session_state.cart[product]['aed'] += clean_num(row[aed_col]) * units
            else:
                st.session_state.cart[product] = {
                    "units": units,
                    "pkr": clean_num(row[pkr_col]) * units,
                    "sar": clean_num(row[sar_col]) * units,
                    "aed": clean_num(row[aed_col]) * units
                }
            st.rerun()

    # 7. Quotation Summary
    if st.session_state.cart:
        total_pkr = 0; total_sar = 0; total_aed = 0
        st.markdown("<br>### CURRENT SELECTION")
        
        # Displaying dict items for the merge logic
        for name, data in list(st.session_state.cart.items()):
            total_pkr += data['pkr']; total_sar += data['sar']; total_aed += data['aed']
            c1, c2, c3 = st.columns([3, 1.5, 0.5])
            with c1: st.write(f"**{name}** (x{data['units']})")
            with c2: st.write(f"PKR {data['pkr']:,.0f}")
            with c3:
                if st.button("🗑️", key=f"del_{name}"):
                    del st.session_state.cart[name]; st.rerun()

        # Premium Total Card
        st.markdown(f"""
            <div style="border: 1px solid #37b36f; padding: 40px; border-radius: 4px; background: rgba(55,179,111,0.08); text-align: center; margin-top: 40px;">
                <p style="letter-spacing: 5px; color: #AAA; font-size: 0.7rem;">TOTAL VALUATION</p>
                <h1 style="color: white; font-size: 3.5rem; font-weight: 900; margin: 0;">PKR {total_pkr:,.0f}</h1>
                <div style="display: flex; justify-content: center; gap: 50px; margin-top: 25px; border-top: 1px solid #222; padding-top: 20px;">
                    <div><p style="color: #37b36f; font-size: 0.7rem;">SAR (SAUDI)</p><h2 style="color:white; font-weight:400;">{total_sar:,.2f}</h2></div>
                    <div><p style="color: #37b36f; font-size: 0.7rem;">AED (DUBAI)</p><h2 style="color:white; font-weight:400;">{total_aed:,.2f}</h2></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"Syncing Error: {e}")
