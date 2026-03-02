import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import numpy as np

# 1. Page Configuration
st.set_page_config(page_title="Bayut Studios | Global Quotation Engine", layout="centered")

# --- FUNCTIONS DEFINED FIRST ---
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

# --- 2. THE DESIGN: RICH NIGHT & MASSIVE STARS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@200;700;900&display=swap');
    
    .stApp { background-color: #000000; color: white !important; font-family: 'Montserrat', sans-serif; }
    
    label, .stMarkdown p, .stExpander p { color: #FFFFFF !important; font-weight: 700 !important; text-transform: uppercase; letter-spacing: 2px; }

    /* LAYER 1: MASSIVE STATIONARY STARS */
    .stApp::before {
        content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background-image: 
            radial-gradient(5px 5px at 10% 15%, #ffffff, rgba(0,0,0,0)),
            radial-gradient(8px 8px at 80% 80%, #37b36f, rgba(0,0,0,0)),
            radial-gradient(6px 6px at 40% 60%, #ffffff, rgba(0,0,0,0)),
            radial-gradient(10px 10px at 20% 90%, #ffffff, rgba(0,0,0,0)),
            radial-gradient(7px 7px at 85% 15%, #37b36f, rgba(0,0,0,0));
        background-repeat: repeat; background-size: 1000px 1000px; opacity: 1; z-index: -1;
    }

    /* LAYER 2: LARGE MOVING STARS */
    .stApp::after {
        content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background-image: 
            radial-gradient(4px 4px at 50% 50%, #ffffff, rgba(0,0,0,0)),
            radial-gradient(9px 9px at 25% 25%, #37b36f, rgba(0,0,0,0)),
            radial-gradient(5px 5px at 75% 75%, #ffffff, rgba(0,0,0,0));
        background-repeat: repeat; background-size: 800px 800px; opacity: 0.8; 
        animation: stars-move 120s linear infinite; z-index: -1;
    }

    @keyframes stars-move { from { background-position: 0 0; } to { background-position: 0 -10000px; } }

    .rich-header { text-align: center; font-weight: 900; letter-spacing: 12px; text-transform: uppercase; margin: 20px 0; text-shadow: 0 0 40px rgba(55, 179, 111, 0.8); font-size: 2.8rem; }
    
    div.stExpander { border: 2px solid rgba(55, 179, 111, 0.7) !important; background: rgba(0, 0, 0, 0.85) !important; backdrop-filter: blur(20px); border-radius: 12px !important; }
    
    div.stButton > button { background: linear-gradient(135deg, #1a6b4a 0%, #37b36f 100%) !important; color: white !important; font-weight: 900 !important; letter-spacing: 3px; border-radius: 4px; border: none; padding: 1rem; width: 100%; }

    /* Item Card Styling */
    .item-card { background: rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid #37b36f; }
    .currency-sub { font-size: 0.8rem; color: #37b36f; margin: 0; }
    </style>
    """, unsafe_allow_html=True)

# 3. Logo & Header
st.image("https://i.ibb.co/LzsV9Z6j/f774cc00-9f2e-4130-9644-1bddb2d6ae50.jpg")
st.markdown("<h1 class='rich-header'>Price Calculator</h1>", unsafe_allow_html=True)

# 4. Session Initialization
if 'cart' not in st.session_state: st.session_state.cart = []

# 5. Data Hub
url = "https://docs.google.com/spreadsheets/d/1qvBKlYH7q4dXsu7tEh9OLnKSydfONNRzGa-xjUYLB0g/edit?usp=sharing"
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(spreadsheet=url, ttl="1m")
    df.columns = [str(c).strip() for c in df.columns]
except Exception as e:
    st.error("Engine Syncing Error. Please check Google Sheet columns.")
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

# 7. Current Scope & Multi-Currency Breakdown
if st.session_state.cart:
    st.markdown("<br><h3>📋 CURRENT SCOPE</h3>", unsafe_allow_html=True)
    totals = {"pkr": 0, "sar": 0, "aed": 0}
    
    for i, item in enumerate(st.session_state.cart):
        totals["pkr"] += item["pkr"]
        totals["sar"] += item["sar"]
        totals["aed"] += item["aed"]
        
        with st.container():
            st.markdown(f"""
            <div class="item-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <b style="font-size: 1.1rem;">{item['name']} (x{item['units']})</b>
                        <p class="currency-sub">SAR {item['sar']:,.2f} | AED {item['aed']:,.2f}</p>
                    </div>
                    <b style="font-size: 1.2rem; color: #FFF;">PKR {item['pkr']:,.0f}</b>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Remove {i}", key=f"del_{i}", help="Remove item"):
                st.session_state.cart.pop(i); st.rerun()

    # 8. Global Valuation Card
    st.markdown(f"""
        <div style="border: 3px solid #37b36f; padding: 40px; border-radius: 20px; background: rgba(55, 179, 111, 0.1); text-align: center; margin-top: 40px;">
            <p style="letter-spacing: 5px; color: #37b36f; font-weight: 700;">✦ TOTAL VALUATION ✦</p>
            <h1 style="color: white; font-size: 3.8rem; font-weight: 900; margin: 0;">PKR {totals['pkr']:,.0f}</h1>
            <div style="display: flex; justify-content: center; gap: 60px; border-top: 2px solid #37b36f; padding-top: 20px; margin-top: 20px;">
                <div><p style="color: #37b36f; font-size: 0.9rem;">SAR</p><h2 style="color:white; font-size: 1.8rem;">{totals['sar']:,.2f}</h2></div>
                <div><p style="color: #37b36f; font-size: 0.9rem;">AED</p><h2 style="color:white; font-size: 1.8rem;">{totals['aed']:,.2f}</h2></div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🗑️ CLEAR ALL QUOTATION"):
        st.session_state.cart = []; st.rerun()
