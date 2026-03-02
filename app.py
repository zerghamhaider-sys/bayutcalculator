import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Bayut Studios | Price Calculator", layout="centered")

# 2. Premium Design: Ultra-Visible Stars & Bold White Text
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@200;700;900&display=swap');

    /* Pitch Black Deep Background */
    .stApp {
        background-color: #000000;
        color: white !important;
        font-family: 'Montserrat', sans-serif;
    }

    /* FORCED WHITE LABELS - High Visibility */
    label, .stMarkdown p, .stExpander p, .stSelectbox p {
        color: #FFFFFF !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-size: 0.85rem !important;
    }

    /* Bulletproof Glistening Stars */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background-image: 
            radial-gradient(2px 2px at 50px 100px, #ffffff, rgba(0,0,0,0)),
            radial-gradient(3px 3px at 150px 350px, #37b36f, rgba(0,0,0,0)),
            radial-gradient(2px 2px at 250px 200px, #ffffff, rgba(0,0,0,0)),
            radial-gradient(4px 4px at 400px 500px, #37b36f, rgba(0,0,0,0)),
            radial-gradient(2px 2px at 550px 150px, #ffffff, rgba(0,0,0,0)),
            radial-gradient(3px 3px at 700px 600px, #ffffff, rgba(0,0,0,0));
        background-repeat: repeat;
        background-size: 800px 800px;
        opacity: 0.9;
        animation: stars-move 120s linear infinite;
        z-index: -1;
    }

    @keyframes stars-move {
        from { background-position: 0 0; }
        to { background-position: 0 -10000px; }
    }

    /* Bold Premium Header */
    .rich-header {
        text-align: center;
        font-weight: 900;
        letter-spacing: 10px;
        color: #FFFFFF;
        text-transform: uppercase;
        margin: 20px 0;
        text-shadow: 0 0 20px rgba(55, 179, 111, 0.6);
    }

    /* Glassmorphism Expander */
    div.stExpander {
        border: 1px solid rgba(55, 179, 111, 0.5) !important;
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(20px);
        border-radius: 12px !important;
    }

    /* Premium Green Buttons */
    div.stButton > button {
        background: linear-gradient(135deg, #1a6b4a 0%, #37b36f 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 4px !important;
        font-weight: 900 !important;
        letter-spacing: 3px;
        padding: 1rem 2rem !important;
        width: 100%;
        box-shadow: 0 10px 30px rgba(55, 179, 111, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Logo & Rich Header
st.image("https://i.ibb.co/LzsV9Z6j/f774cc00-9f2e-4130-9644-1bddb2d6ae50.jpg")
st.markdown("<h1 class='rich-header'>PRIME QUOTATION ENGINE</h1>", unsafe_allow_html=True)

# 4. Global Project Memory
if 'cart' not in st.session_state:
    st.session_state.cart = []

# 5. Data Hub
url = "https://docs.google.com/spreadsheets/d/1qvBKlYH7q4dXsu7tEh9OLnKSydfONNRzGa-xjUYLB0g/edit?usp=sharing"

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(spreadsheet=url, ttl="1m")
    df.columns = [c.strip() for c in df.columns] # Syncing fix

    # Column Mapping
    cat_col, prod_col, pkr_col, sar_col, aed_col = "Product Category", "Product", "Total Price (PKR)", "Total Price (SAR)", "Total Price (AED)"

    def clean_num(val):
        if isinstance(val, str):
            return float(val.replace('PKR','').replace('SAR','').replace('dh','').replace(',','').strip())
        return float(val)

    # 6. Service Selector
    with st.expander("CONFIGURE YOUR PROJECT SCOPE", expanded=True):
        category = st.selectbox("CATEGORY", df[cat_col].unique())
        sub_df = df[df[cat_col] == category]
        
        product = st.selectbox("PRODUCT SERVICE", sub_df[prod_col].unique())
        units = st.number_input("UNITS REQUIRED", min_value=1, value=1)
        
        if st.button("ADD TO QUOTATION"):
            row = sub_df[sub_df[prod_col] == product].iloc[0]
            st.session_state.cart.append({
                "name": product, "units": units,
                "pkr": clean_num(row[pkr_col]) * units,
                "sar": clean_num(row[sar_col]) * units,
                "aed": clean_num(row[aed_col]) * units
            })
            st.rerun()

    # 7. Summary & Total Valuation
    if st.session_state.cart:
        totals = {"pkr": 0, "sar": 0, "aed": 0}
        st.markdown("<br><h3 style='letter-spacing:4px; font-weight:200;'>CURRENT SCOPE</h3>", unsafe_allow_html=True)
        
        for i, item in enumerate(st.session_state.cart):
            totals["pkr"] += item["pkr"]; totals["sar"] += item["sar"]; totals["aed"] += item["aed"]
            col_1, col_2, col_3 = st.columns([3, 1.5, 0.5])
            with col_1: st.write(f"**{item['name']}** (x{item['units']})")
            with col_2: st.write(f"PKR {item['pkr']:,.0f}")
            with col_3:
                if st.button("🗑️", key=f"del_{i}"):
                    st.session_state.cart.pop(i); st.rerun()

        # Premium Total Display
        st.markdown(f"""
            <div style="border: 2px solid #37b36f; padding: 40px; border-radius: 4px; background: rgba(55, 179, 111, 0.1); text-align: center; margin-top: 40px;">
                <p style="letter-spacing: 5px; color: #AAA; font-size: 0.7rem;">TOTAL VALUATION</p>
                <h1 style="color: white; font-size: 4rem; font-weight: 900; margin: 10px 0;">PKR {totals['pkr']:,.0f}</h1>
                <div style="display: flex; justify-content: center; gap: 60px; border-top: 1px solid #333; padding-top: 25px; margin-top: 20px;">
                    <div><p style="color: #37b36f; font-size: 0.8rem; font-weight:700;">SAR</p><h2 style="color:white; font-weight:200;">{totals['sar']:,.2f}</h2></div>
                    <div><p style="color: #37b36f; font-size: 0.8rem; font-weight:700;">AED</p><h2 style="color:white; font-weight:200;">{totals['aed']:,.2f}</h2></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"ENGINE OFFLINE: {e}")
