import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import numpy as np

# 1. Page Configuration
st.set_page_config(page_title="Bayut Studios | Global Quotation Engine", layout="centered")

# --- FUNCTIONS ---
def consolidate_cart(cart_items):
    consolidated = {}
    for item in cart_items:
        if isinstance(item, dict) and "name" in item:
            key = item["name"]
            if key in consolidated:
                consolidated[key]["units"] += item["units"]
                consolidated[key]["pkr"] += item["pkr"]
                consolidated[key]["sar"] += item["sar"]
                consolidated[key]["aed"] += item["aed"]
            else:
                consolidated[key] = item.copy()
    return list(consolidated.values())

def clean_num(val):
    try:
        if pd.isna(val): return 0.0
        if isinstance(val, (int, float)): return float(val)
        if isinstance(val, str):
            cleaned = val.replace('PKR','').replace('SAR','').replace('AED','').replace('dh','').replace(',','').strip()
            return float(cleaned) if cleaned else 0.0
        return 0.0
    except: return 0.0

## 2. THE DESIGN: ULTRA-STARRY & FIXED BUTTONS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@200;400;700;900&family=Inter:wght@700;900&display=swap');
    
    .stApp { background-color: #000000; color: white !important; font-family: 'Montserrat', sans-serif; }
    
    /* Global Label Visibility */
    label, .stMarkdown p, .stExpander p { 
        color: #FFFFFF !important; 
        font-weight: 700 !important; 
        text-transform: uppercase; 
        letter-spacing: 2px;
    }

    /* MASSIVE STAR ENGINE */
    .stApp::before {
        content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background-image: 
            radial-gradient(4px 4px at 5% 5%, #ffffff, rgba(0,0,0,0)),
            radial-gradient(12px 12px at 15% 45%, #37b36f, rgba(0,0,0,0)),
            radial-gradient(6px 6px at 45% 85%, #ffffff, rgba(0,0,0,0)),
            radial-gradient(14px 14px at 85% 15%, #ffffff, rgba(0,0,0,0)),
            radial-gradient(10px 10px at 70% 60%, #37b36f, rgba(0,0,0,0));
        background-repeat: repeat; background-size: 1100px 1100px; opacity: 1; 
        animation: stars-move 180s linear infinite; z-index: -1;
    }
    @keyframes stars-move { from { background-position: 0 0; } to { background-position: 0 -10000px; } }

    /* FIX: Input Boxes Dark Mode */
    div[data-baseweb="select"] > div, div[data-baseweb="popover"] > div, .stSelectbox div, .stNumberInput input {
        background-color: #0a0a0a !important;
        color: white !important;
        border: 1px solid rgba(55, 179, 111, 0.4) !important;
    }

    /* FIX: ALL BUTTONS - Prevent White-out on Click/Hover */
    button {
        color: white !important;
    }
    
    /* Main Action Buttons (Add to Quotation / Clear All) */
    div.stButton > button:not([key^="del_"]) {
        background: linear-gradient(135deg, #1a6b4a 0%, #37b36f 100%) !important;
        border: none !important;
        font-weight: 900 !important;
        letter-spacing: 3px;
        padding: 1rem !important;
        width: 100%;
        border-radius: 8px !important;
        box-shadow: 0 10px 20px rgba(0,0,0,0.5) !important;
    }
    
    div.stButton > button:not([key^="del_"]):hover, 
    div.stButton > button:not([key^="del_"]):active,
    div.stButton > button:not([key^="del_"]):focus {
        background: #37b36f !important; /* Solid green on hover */
        color: white !important;
        transform: translateY(-2px);
    }

    /* Bin Icon Fix (No White-out) */
    div[key^="del_"] button {
        background-color: transparent !important;
        color: #ff4b4b !important;
        border: none !important;
        font-size: 1.8rem !important;
    }
    
    div[key^="del_"] button:hover, div[key^="del_"] button:focus {
        color: #ff3333 !important;
        background-color: transparent !important;
        transform: scale(1.2);
    }

    /* Item Card & Text Styling */
    .item-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(12px);
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 12px;
        border-left: 6px solid #37b36f;
    }
    .bold-currency { font-family: 'Inter', sans-serif; font-weight: 900; color: #37b36f; letter-spacing: 1px; }
    .rich-header { text-align: center; font-weight: 900; letter-spacing: 14px; text-transform: uppercase; margin: 25px 0; text-shadow: 0 0 35px rgba(55, 179, 111, 0.7); font-size: 2.5rem; }
    .grand-total-text { font-family: 'Inter', sans-serif; font-weight: 900; font-size: 4.2rem; margin: 0; color: white; }
    </style>
    """, unsafe_allow_html=True)
# 3. Logo & Brand
st.image("https://i.ibb.co/LzsV9Z6j/f774cc00-9f2e-4130-9644-1bddb2d6ae50.jpg")
st.markdown("<h1 class='rich-header'>Price Calculator</h1>", unsafe_allow_html=True)

# 4. Initialization
if 'cart' not in st.session_state: st.session_state.cart = []

# 5. Data Core
url = "https://docs.google.com/spreadsheets/d/1qvBKlYH7q4dXsu7tEh9OLnKSydfONNRzGa-xjUYLB0g/edit?usp=sharing"
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(spreadsheet=url, ttl="1m")
    df.columns = [str(c).strip() for c in df.columns]
except:
    st.error("Engine Syncing Error.")
    st.stop()

# 6. Service Selector
with st.expander("🚀 CONFIGURE YOUR PROJECT SCOPE", expanded=True):
    cat_col, prod_col, pkr_col, sar_col, aed_col = "Product Category", "Product", "Total Price (PKR)", "Total Price (SAR)", "Total Price (AED)"
    category = st.selectbox("CATEGORY", df[cat_col].dropna().unique())
    sub_df = df[df[cat_col] == category]
    product = st.selectbox("PRODUCT SERVICE", sub_df[prod_col].dropna().unique())
    units = st.number_input("UNITS REQUIRED", min_value=1, value=1, step=1)
    
    if st.button("➕ ADD TO QUOTATION"):
        row = sub_df[sub_df[prod_col] == product].iloc[0]
        st.session_state.cart.append({
            "name": product, "units": units,
            "pkr": clean_num(row[pkr_col]) * units,
            "sar": clean_num(row[sar_col]) * units,
            "aed": clean_num(row[aed_col]) * units
        })
        st.session_state.cart = consolidate_cart(st.session_state.cart)
        st.rerun()

# 7. Sleek List Display
if st.session_state.cart:
    st.markdown("<br><h3>📋 PROJECT LIST</h3>", unsafe_allow_html=True)
    totals = {"pkr": 0, "sar": 0, "aed": 0}
    
    for i, item in enumerate(st.session_state.cart):
        totals["pkr"] += item["pkr"]
        totals["sar"] += item["sar"]
        totals["aed"] += item["aed"]
        
        # Sleek Glassmorphism Card
        col_text, col_bin = st.columns([4, 1])
        with col_text:
            st.markdown(f"""
            <div class="item-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <span style="font-size: 1.3rem; font-weight: 700; color: #FFF;">{item['name']}</span>
                    <span style="font-size: 1.2rem; font-weight: 900; color: #FFF;">PKR {item['pkr']:,.0f}</span>
                </div>
                <div style="display: flex; gap: 15px; align-items: center;">
                    <span style="color: #888; font-weight: 700;">QTY: {item['units']}</span>
                    <span style="color: #444;">|</span>
                    <span class="bold-currency">SAR {item['sar']:,.2f}</span>
                    <span style="color: #444;">|</span>
                    <span class="bold-currency">AED {item['aed']:,.2f}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col_bin:
            # Fixed Bin Icon Button
            if st.button("🗑️", key=f"del_{i}", help="Delete item"):
                st.session_state.cart.pop(i); st.rerun()

    # 8. Global Valuation Card
    st.markdown(f"""
        <div style="border: 2px solid #37b36f; padding: 45px; border-radius: 20px; background: rgba(55, 179, 111, 0.08); text-align: center; margin-top: 40px; backdrop-filter: blur(10px);">
            <p style="letter-spacing: 6px; color: #37b36f; font-weight: 700; font-size: 0.9rem;">✦ TOTAL VALUATION ✦</p>
            <h1 class="grand-total-text">PKR {totals['pkr']:,.0f}</h1>
            <div style="display: flex; justify-content: center; gap: 60px; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 30px; margin-top: 30px;">
                <div>
                    <p style="color: #37b36f; font-size: 1rem; font-weight: 900; letter-spacing: 2px;">SAR (SAUDI)</p>
                    <h2 style="color:white; font-size: 2.2rem; font-weight: 900; font-family: 'Inter';">{totals['sar']:,.2f}</h2>
                </div>
                <div>
                    <p style="color: #37b36f; font-size: 1rem; font-weight: 900; letter-spacing: 2px;">AED (DUBAI)</p>
                    <h2 style="color:white; font-size: 2.2rem; font-weight: 900; font-family: 'Inter';">{totals['aed']:,.2f}</h2>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🗑️ CLEAR ENTIRE QUOTATION", use_container_width=True):
        st.session_state.cart = []; st.rerun()
