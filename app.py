import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Bayut Studios | Price Calculator", layout="centered")

# 2. DESIGN FIX: Ultra-Starry Night & Dropdown Visibility
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@200;700;900&display=swap');

    /* Pitch Black Base */
    .stApp {
        background-color: #000000;
        color: white !important;
        font-family: 'Montserrat', sans-serif;
    }

    /* FIX: Force dropdowns to stay black and text to stay white on hover/focus */
    div[data-baseweb="select"] > div, 
    div[data-baseweb="popover"] > div,
    .stSelectbox div, .stNumberInput input {
        background-color: #000000 !important;
        color: white !important;
        border: 1px solid #37b36f !important;
    }
    
    /* Ensure Expander Header stays black/visible */
    .stExpander {
        background-color: #000000 !important;
        border: 1px solid rgba(55, 179, 111, 0.5) !important;
    }

    /* FORCED WHITE LABELS */
    label, .stMarkdown p, .stExpander p, h3 {
        color: #FFFFFF !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    /* ULTRA-STARRY CSS ENGINE */
    /* This creates a dense field of glistening dots exactly like your picture */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background-image: 
            radial-gradient(1.5px 1.5px at 10% 10%, #fff, transparent),
            radial-gradient(2px 2px at 20% 50%, #37b36f, transparent),
            radial-gradient(1.5px 1.5px at 40% 30%, #fff, transparent),
            radial-gradient(2.5px 2.5px at 60% 80%, #fff, transparent),
            radial-gradient(2px 2px at 80% 20%, #37b36f, transparent),
            radial-gradient(1.5px 1.5px at 90% 70%, #fff, transparent),
            radial-gradient(2px 2px at 30% 90%, #fff, transparent),
            radial-gradient(1.5px 1.5px at 70% 40%, #fff, transparent);
        background-size: 350px 350px;
        opacity: 0.9;
        animation: stars-move 100s linear infinite;
        z-index: -1;
    }

    @keyframes stars-move {
        from { background-position: 0 0; }
        to { background-position: 0 -10000px; }
    }

    /* BOLD PRICE CALCULATOR HEADER */
    .rich-header {
        text-align: center;
        font-weight: 900;
        letter-spacing: 15px;
        color: #FFFFFF;
        text-transform: uppercase;
        margin: 30px 0;
        text-shadow: 0 0 20px rgba(55, 179, 111, 0.8);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Branding Section
st.image("https://i.ibb.co/LzsV9Z6j/f774cc00-9f2e-4130-9644-1bddb2d6ae50.jpg")
st.markdown("<h1 class='rich-header'>Price Calculator</h1>", unsafe_allow_html=True)

# 4. Initialize Cart as a DICTIONARY (Fixes the 'items' error)
if 'cart' not in st.session_state or isinstance(st.session_state.cart, list):
    st.session_state.cart = {}

# 5. Data Hub
url = "https://docs.google.com/spreadsheets/d/1qvBKlYH7q4dXsu7tEh9OLnKSydfONNRzGa-xjUYLB0g/edit?usp=sharing"

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(spreadsheet=url, ttl="1m")
    df.columns = [c.strip() for c in df.columns]

    cat_col, prod_col, pkr_col, sar_col, aed_col = "Product Category", "Product", "Total Price (PKR)", "Total Price (SAR)", "Total Price (AED)"

    def clean_num(val):
        if isinstance(val, str):
            return float(val.replace('PKR','').replace('SAR','').replace('dh','').replace(',','').strip())
        return float(val)

    # 6. Service Selection
    with st.expander("CONFIGURE YOUR PROJECT SCOPE", expanded=True):
        category = st.selectbox("CATEGORY", df[cat_col].unique())
        sub_df = df[df[cat_col] == category]
        
        product = st.selectbox("PRODUCT SERVICE", sub_df[prod_col].unique())
        units = st.number_input("UNITS REQUIRED", min_value=1, value=1)
        
        if st.button("ADD TO QUOTATION", use_container_width=True):
            row = sub_df[sub_df[prod_col] == product].iloc[0]
            
            # Smart Merge Logic: If item exists, add units. If not, create it.
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

    # 7. Quotation List
    if st.session_state.cart:
        total_pkr = 0; total_sar = 0; total_aed = 0
        st.markdown("<br><h3>Current Selection</h3>", unsafe_allow_html=True)
        
        for name, data in list(st.session_state.cart.items()):
            total_pkr += data['pkr']; total_sar += data['sar']; total_aed += data['aed']
            c1, c2, c3 = st.columns([3, 1.5, 0.5])
            with c1: st.write(f"**{name}** (x{data['units']})")
            with c2: st.write(f"PKR {data['pkr']:,.0f}")
            with c3:
                if st.button("🗑️", key=f"del_{name}"):
                    del st.session_state.cart[name]; st.rerun()

        # Premium Total Valuation Card
        st.markdown(f"""
            <div style="border: 2px solid #37b36f; padding: 40px; border-radius: 4px; background: rgba(55, 179, 111, 0.1); text-align: center; margin-top: 40px;">
                <p style="letter-spacing: 5px; color: #AAA; font-size: 0.7rem;">TOTAL VALUATION</p>
                <h1 style="color: white; font-size: 4rem; font-weight: 900; margin: 0;">PKR {total_pkr:,.0f}</h1>
                <div style="display: flex; justify-content: center; gap: 50px; border-top: 1px solid #333; padding-top: 25px; margin-top: 20px;">
                    <div><p style="color: #37b36f; font-size: 0.8rem;">SAR</p><h2 style="color:white; font-weight:400;">{total_sar:,.2f}</h2></div>
                    <div><p style="color: #37b36f; font-size: 0.8rem;">AED</p><h2 style="color:white; font-weight:400;">{total_aed:,.2f}</h2></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"ENGINE OFFLINE: {e}")
