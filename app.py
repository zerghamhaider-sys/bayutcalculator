import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import numpy as np

# 1. Page Configuration
st.set_page_config(page_title="Bayut Studios | Prime Quotation Engine", layout="centered")

# --- FUNCTIONS DEFINED FIRST TO PREVENT NAMEERROR ---

def consolidate_cart(cart_items):
    """Consolidates duplicate items in the cart."""
    consolidated = {}
    for item in cart_items:
        # Ensure item is a dictionary and has the "name" key to prevent TypeErrors
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
    """Cleans currency strings into floats."""
    try:
        if pd.isna(val): return 0.0
        if isinstance(val, (int, float)): return float(val)
        if isinstance(val, str):
            cleaned = val.replace('PKR','').replace('SAR','').replace('AED','').replace('dh','').replace(',','').strip()
            return float(cleaned) if cleaned else 0.0
        return 0.0
    except:
        return 0.0

def get_demo_data():
    """Fallback data if Google Sheets fails."""
    demo_data = {
        'Product Category': ['Architectural Design', 'Interior Design', 'Construction'],
        'Product': ['Residential Design', 'Residential Interior', 'Villa Construction'],
        'Total Price (PKR)': ['PKR 500,000', 'PKR 350,000', 'PKR 5,000,000'],
        'Total Price (SAR)': ['SAR 7,500', 'SAR 5,250', 'SAR 75,000'],
        'Total Price (AED)': ['AED 7,200', 'AED 5,040', 'AED 72,000']
    }
    return pd.DataFrame(demo_data)

# --- 2. PREMIUM DESIGN (STARRY THEME) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@200;700;900&display=swap');
    .stApp { background-color: #000000; color: white !important; font-family: 'Montserrat', sans-serif; }
    
    label, .stMarkdown p, .stExpander p { color: #FFFFFF !important; font-weight: 700 !important; text-transform: uppercase; letter-spacing: 1.5px; }

    /* Big Stars */
    .stApp::before {
        content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background-image: radial-gradient(4px 4px at 20px 30px, #ffffff, rgba(0,0,0,0)), radial-gradient(6px 6px at 80px 120px, #37b36f, rgba(0,0,0,0)), radial-gradient(8px 8px at 450px 150px, #ffffff, rgba(0,0,0,0));
        background-repeat: repeat; background-size: 1200px 1200px; opacity: 1; animation: stars-move 180s linear infinite; z-index: -1;
    }
    @keyframes stars-move { from { background-position: 0 0; } to { background-position: 0 -10000px; } }

    .rich-header { text-align: center; font-weight: 900; letter-spacing: 10px; color: #FFFFFF; text-transform: uppercase; margin: 20px 0; text-shadow: 0 0 30px rgba(55, 179, 111, 0.8); font-size: 2.5rem; }
    div.stExpander { border: 2px solid rgba(55, 179, 111, 0.7) !important; background: rgba(0, 0, 0, 0.7) !important; backdrop-filter: blur(15px); border-radius: 16px !important; }
    div.stButton > button { background: linear-gradient(135deg, #1a6b4a 0%, #37b36f 100%) !important; color: white !important; font-weight: 900 !important; letter-spacing: 3px; padding: 1rem 2rem !important; width: 100%; border-radius: 4px; }
    </style>
    """, unsafe_allow_html=True)

# 3. Logo & Header
st.image("https://i.ibb.co/LzsV9Z6j/f774cc00-9f2e-4130-9644-1bddb2d6ae50.jpg")
st.markdown("<h1 class='rich-header'>PRIME QUOTATION ENGINE</h1>", unsafe_allow_html=True)

# 4. Global Project Memory & Self-Healing
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'use_demo_data' not in st.session_state:
    st.session_state.use_demo_data = False

# 5. Data Connection
url = "https://docs.google.com/spreadsheets/d/1qvBKlYH7q4dXsu7tEh9OLnKSydfONNRzGa-xjUYLB0g/edit?usp=sharing"
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(spreadsheet=url, ttl="1m")
    if df is None or df.empty:
        df = get_demo_data()
        st.session_state.use_demo_data = True
    else:
        df.columns = [str(c).strip() for c in df.columns]
except Exception as e:
    df = get_demo_data()
    st.session_state.use_demo_data = True

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

# 7. Summary & Total Valuation
if st.session_state.cart:
    st.session_state.cart = consolidate_cart(st.session_state.cart)
    totals = {"pkr": 0, "sar": 0, "aed": 0}
    st.markdown("<br><h3 style='letter-spacing:4px; font-weight:200; color: white;'>📋 CURRENT SCOPE</h3>", unsafe_allow_html=True)
    
    for i, item in enumerate(st.session_state.cart):
        totals["pkr"] += item["pkr"]
        totals["sar"] += item["sar"]
        totals["aed"] += item["aed"]
        c1, c2, c3, c4 = st.columns([3, 1, 1.5, 0.5])
        with c1: st.markdown(f"**{item['name']}**")
        with col_2 if 'col_2' in locals() else c2: st.markdown(f"x**{item['units']}**")
        with col_3 if 'col_3' in locals() else c3: st.markdown(f"PKR **{item['pkr']:,.0f}**")
        with c4: 
            if st.button("🗑️", key=f"del_{i}"):
                st.session_state.cart.pop(i); st.rerun()

    st.markdown(f"""
        <div style="border: 3px solid #37b36f; padding: 40px; border-radius: 20px; background: rgba(0, 0, 0, 0.8); text-align: center; margin-top: 40px;">
            <p style="color: #37b36f; font-weight: 700;">✦ TOTAL VALUATION ✦</p>
            <h1 style="color: white; font-size: 3.5rem;">PKR {totals['pkr']:,.0f}</h1>
            <div style="display: flex; justify-content: center; gap: 40px; border-top: 2px solid #37b36f; padding-top: 20px; margin-top: 20px;">
                <div><p style="color: #37b36f;">SAR</p><h3>{totals['sar']:,.2f}</h3></div>
                <div><p style="color: #37b36f;">AED</p><h3>{totals['aed']:,.2f}</h3></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if st.button("🗑️ CLEAR ALL QUOTATION"):
        st.session_state.cart = []; st.rerun()
