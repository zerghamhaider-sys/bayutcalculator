import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Bayut Studios | Global Estimate Builder", layout="centered")

# 2. THE FIX: Global CSS Injection for Starry Theme & White Labels
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@200;400;700&display=swap');

    /* 1. Bulletproof Dark Starry Background */
    .stApp {
        background: radial-gradient(ellipse at bottom, #000000 0%, #050505 100%);
        background-attachment: fixed;
        color: white !important;
        font-family: 'Inter', sans-serif;
    }

    /* 2. Visible White Headings & Labels */
    .stMarkdown p, .stSelectbox label, .stNumberInput label, .stExpander p {
        color: #FFFFFF !important;
        font-weight: 300 !important;
        letter-spacing: 1px;
        font-size: 1rem !important;
    }

    /* 3. High-Visibility Starfield */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background-image: 
            radial-gradient(2px 2px at 20px 30px, #eee, rgba(0,0,0,0)),
            radial-gradient(2px 2px at 40px 70px, #fff, rgba(0,0,0,0)),
            radial-gradient(3px 3px at 50px 160px, #37b36f, rgba(0,0,0,0)),
            radial-gradient(2px 2px at 90px 40px, #fff, rgba(0,0,0,0)),
            radial-gradient(2px 2px at 130px 80px, #fff, rgba(0,0,0,0));
        background-repeat: repeat;
        background-size: 300px 300px;
        opacity: 0.6;
        animation: stars-move 100s linear infinite;
        z-index: -1;
    }

    @keyframes stars-move {
        from { background-position: 0 0; }
        to { background-position: 0 -10000px; }
    }

    /* 4. Luxury Glassmorphism & Buttons */
    div.stExpander {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(55, 179, 111, 0.3) !important;
        backdrop-filter: blur(15px);
        border-radius: 15px !important;
    }

    div.stButton > button {
        background: linear-gradient(135deg, #1a6b4a 0%, #37b36f 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        letter-spacing: 2px;
        font-weight: 700 !important;
        padding: 0.75rem 2rem !important;
        box-shadow: 0 10px 20px rgba(55, 179, 111, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Branding Section
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("https://i.ibb.co/LzsV9Z6j/f774cc00-9f2e-4130-9644-1bddb2d6ae50.jpg", use_container_width=True)
st.markdown("<h2 style='text-align: center; color: white; letter-spacing: 8px; font-weight: 200;'>ESTIMATE BUILDER</h2>", unsafe_allow_html=True)

# 4. Initialize Project Cart
if 'cart' not in st.session_state:
    st.session_state.cart = []

# 5. Data Connection
url = "https://docs.google.com/spreadsheets/d/1qvBKlYH7q4dXsu7tEh9OLnKSydfONNRzGa-xjUYLB0g/edit?usp=sharing"

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(spreadsheet=url, ttl="1m")

    # Column Mapping
    cat_col, prod_col, pkr_col, sar_col, aed_col = "Product Category", "Product", "Total Price (PKR)", "Total Price (SAR)", "Total Price (AED)"

    def clean_val(val):
        if isinstance(val, str):
            return float(val.replace('PKR', '').replace('SAR', '').replace('dh', '').replace(',', '').strip())
        return float(val)

    # 6. Service Selection
    with st.expander("➕ ADD SERVICES TO PROJECT", expanded=not st.session_state.cart):
        category = st.selectbox("Product Category", df[cat_col].unique())
        product = st.selectbox("Product Name", df[df[cat_col] == category][prod_col].unique())
        units = st.number_input("Total Units Required", min_value=1, value=1, step=1)
        
        if st.button("ADD TO ESTIMATE"):
            selected_row = df[df[prod_col] == product].iloc[0]
            st.session_state.cart.append({
                "name": product, "units": units,
                "pkr": clean_val(selected_row[pkr_col]) * units,
                "sar": clean_val(selected_row[sar_col]) * units,
                "aed": clean_val(selected_row[aed_col]) * units
            })
            st.rerun()

    # 7. Cart & Total Display
    if st.session_state.cart:
        st.markdown("---")
        totals = {"pkr": 0, "sar": 0, "aed": 0}
        
        for i, item in enumerate(st.session_state.cart):
            totals["pkr"] += item["pkr"]; totals["sar"] += item["sar"]; totals["aed"] += item["aed"]
            c1, c2, c3 = st.columns([3, 1, 0.5])
            with c1: st.write(f"**{item['name']}** (x{item['units']})")
            with c2: st.write(f"PKR {item['pkr']:,.0f}")
            with c3: 
                if st.button("🗑️", key=f"del_{i}"):
                    st.session_state.cart.pop(i); st.rerun()

        # 8. Luxury Global Total Card
        st.markdown(f"""
            <div style="border: 1px solid #37b36f; padding: 40px; border-radius: 20px; background: rgba(55, 179, 111, 0.08); text-align: center; margin-top: 30px;">
                <p style="letter-spacing: 4px; color: #FFFFFF; opacity: 0.7; font-size: 0.8rem;">GRAND TOTAL ESTIMATE</p>
                <h1 style="color: white; margin: 15px 0; font-size: 3.5rem;">PKR {totals['pkr']:,.0f}</h1>
                <div style="display: flex; justify-content: center; gap: 40px; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 20px;">
                    <div><p style="color: #37b36f; font-size: 0.7rem;">SAUDI RIYAL</p><h2 style="color:white; font-weight:400;">SAR {totals['sar']:,.0f}</h2></div>
                    <div><p style="color: #37b36f; font-size: 0.7rem;">DUBAI DIRHAM</p><h2 style="color:white; font-weight:400;">AED {totals['aed']:,.0f}</h2></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"Syncing Error: {e}")
