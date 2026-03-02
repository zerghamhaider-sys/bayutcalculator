import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import numpy as np

# 1. Page Configuration
st.set_page_config(page_title="Bayut Studios | Prime Quotation Engine", layout="centered")

# 2. Premium Design: Enhanced Stars & Bold White Text
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

    /* Enhanced Glistening Stars - Larger & More Abundant */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background-image: 
            radial-gradient(4px 4px at 20px 30px, #ffffff, rgba(0,0,0,0)),
            radial-gradient(6px 6px at 80px 120px, #37b36f, rgba(0,0,0,0)),
            radial-gradient(5px 5px at 150px 200px, #ffffff, rgba(0,0,0,0)),
            radial-gradient(7px 7px at 250px 80px, #37b36f, rgba(0,0,0,0)),
            radial-gradient(4px 4px at 350px 400px, #ffffff, rgba(0,0,0,0)),
            radial-gradient(8px 8px at 450px 150px, #ffffff, rgba(0,0,0,0)),
            radial-gradient(5px 5px at 550px 500px, #37b36f, rgba(0,0,0,0)),
            radial-gradient(6px 6px at 650px 300px, #ffffff, rgba(0,0,0,0)),
            radial-gradient(7px 7px at 750px 450px, #37b36f, rgba(0,0,0,0)),
            radial-gradient(5px 5px at 850px 200px, #ffffff, rgba(0,0,0,0)),
            radial-gradient(9px 9px at 950px 550px, #ffffff, rgba(0,0,0,0)),
            radial-gradient(4px 4px at 1050px 350px, #37b36f, rgba(0,0,0,0)),
            radial-gradient(6px 6px at 150px 650px, #ffffff, rgba(0,0,0,0)),
            radial-gradient(8px 8px at 450px 750px, #37b36f, rgba(0,0,0,0)),
            radial-gradient(5px 5px at 750px 850px, #ffffff, rgba(0,0,0,0)),
            radial-gradient(7px 7px at 950px 950px, #37b36f, rgba(0,0,0,0));
        background-repeat: repeat;
        background-size: 1200px 1200px;
        opacity: 1;
        animation: stars-move 180s linear infinite;
        z-index: -1;
    }

    /* Additional twinkling stars layer */
    .stApp::after {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background-image: 
            radial-gradient(3px 3px at 120px 520px, #ffffff, rgba(0,0,0,0)),
            radial-gradient(5px 5px at 320px 220px, #37b36f, rgba(0,0,0,0)),
            radial-gradient(4px 4px at 520px 720px, #ffffff, rgba(0,0,0,0)),
            radial-gradient(6px 6px at 720px 420px, #37b36f, rgba(0,0,0,0)),
            radial-gradient(4px 4px at 920px 620px, #ffffff, rgba(0,0,0,0));
        background-repeat: repeat;
        background-size: 1000px 1000px;
        opacity: 0.7;
        animation: stars-move 120s linear infinite reverse;
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
        text-shadow: 0 0 30px rgba(55, 179, 111, 0.8);
        font-size: 2.5rem;
    }

    /* Fixed Glassmorphism Expander - Always Green Tint */
    div.stExpander {
        border: 2px solid rgba(55, 179, 111, 0.7) !important;
        background: rgba(0, 0, 0, 0.7) !important;
        backdrop-filter: blur(15px);
        border-radius: 16px !important;
        transition: all 0.3s ease;
    }
    
    /* Keep the green tint even when not hovered */
    div.stExpander > div:first-child {
        background-color: rgba(55, 179, 111, 0.15) !important;
        border-radius: 16px 16px 0 0 !important;
    }
    
    /* Expander header text */
    div.stExpander summary p {
        color: #37b36f !important;
        font-size: 1rem !important;
        font-weight: 900 !important;
    }
    
    /* Content area background */
    div.stExpander > div[data-testid="stExpander"] > div:nth-child(2) {
        background-color: rgba(0, 0, 0, 0.8) !important;
        border-radius: 0 0 16px 16px !important;
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
        box-shadow: 0 10px 30px rgba(55, 179, 111, 0.4);
        transition: all 0.3s ease;
    }
    
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 15px 40px rgba(55, 179, 111, 0.6);
    }
    
    /* Cart items styling */
    .cart-item {
        background: rgba(55, 179, 111, 0.1);
        padding: 10px;
        border-radius: 8px;
        margin: 5px 0;
        border-left: 4px solid #37b36f;
    }
    
    /* Demo mode badge */
    .demo-badge {
        background: rgba(55, 179, 111, 0.2);
        border: 2px solid #37b36f;
        color: #37b36f;
        padding: 10px 20px;
        border-radius: 30px;
        text-align: center;
        font-weight: 900;
        letter-spacing: 2px;
        margin: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Logo & Rich Header
st.image("https://i.ibb.co/LzsV9Z6j/f774cc00-9f2e-4130-9644-1bddb2d6ae50.jpg")
st.markdown("<h1 class='rich-header'>PRIME QUOTATION ENGINE</h1>", unsafe_allow_html=True)

# 4. Global Project Memory
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'use_demo_data' not in st.session_state:
    st.session_state.use_demo_data = False

# Function to consolidate cart items
def consolidate_cart(cart_items):
    consolidated = {}
    for item in cart_items:
        key = item["name"]  # Use product name as key
        if key in consolidated:
            consolidated[key]["units"] += item["units"]
            consolidated[key]["pkr"] += item["pkr"]
            consolidated[key]["sar"] += item["sar"]
            consolidated[key]["aed"] += item["aed"]
        else:
            consolidated[key] = item.copy()
    return list(consolidated.values())

# Function to create demo data if sheet is not accessible
def get_demo_data():
    demo_data = {
        'Product Category': ['Architectural Design', 'Architectural Design', 'Interior Design', 'Interior Design', 
                            'Construction', 'Construction', 'Project Management', 'Project Management'],
        'Product': ['Residential Design', 'Commercial Design', 'Residential Interior', 'Commercial Interior',
                   'Villa Construction', 'Apartment Renovation', 'Design Supervision', 'Construction Management'],
        'Total Price (PKR)': ['PKR 500,000', 'PKR 1,200,000', 'PKR 350,000', 'PKR 800,000',
                             'PKR 5,000,000', 'PKR 2,500,000', 'PKR 450,000', 'PKR 600,000'],
        'Total Price (SAR)': ['SAR 7,500', 'SAR 18,000', 'SAR 5,250', 'SAR 12,000',
                             'SAR 75,000', 'SAR 37,500', 'SAR 6,750', 'SAR 9,000'],
        'Total Price (AED)': ['AED 7,200', 'AED 17,280', 'AED 5,040', 'AED 11,520',
                             'AED 72,000', 'AED 36,000', 'AED 6,480', 'AED 8,640']
    }
    return pd.DataFrame(demo_data)

# 5. Data Hub
url = "https://docs.google.com/spreadsheets/d/1qvBKlYH7q4dXsu7tEh9OLnKSydfONNRzGa-xjUYLB0g/edit?usp=sharing"

try:
    # Try to connect to Google Sheets
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(spreadsheet=url, ttl="1m")
    
    # Check if df is valid and has data
    if df is None or df.empty:
        st.warning("⚠️ Google Sheets connection returned empty data. Using demo data instead.")
        df = get_demo_data()
        st.session_state.use_demo_data = True
    else:
        # Clean column names
        df.columns = [str(c).strip() for c in df.columns]
        
        # Check if required columns exist
        required_cols = ["Product Category", "Product", "Total Price (PKR)", "Total Price (SAR)", "Total Price (AED)"]
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            st.warning(f"⚠️ Missing columns: {missing_cols}. Using demo data instead.")
            df = get_demo_data()
            st.session_state.use_demo_data = True
            
except Exception as e:
    st.warning(f"⚠️ Could not connect to Google Sheets: {str(e)}. Using demo data instead.")
    df = get_demo_data()
    st.session_state.use_demo_data = True

# Show demo mode badge if using demo data
if st.session_state.use_demo_data:
    st.markdown("""
        <div class='demo-badge'>
            ⚡ DEMO MODE - Using Sample Data ⚡
        </div>
    """, unsafe_allow_html=True)

# Column Mapping
cat_col, prod_col, pkr_col, sar_col, aed_col = "Product Category", "Product", "Total Price (PKR)", "Total Price (SAR)", "Total Price (AED)"

def clean_num(val):
    try:
        if pd.isna(val):
            return 0.0
        if isinstance(val, (int, float)):
            return float(val)
        if isinstance(val, str):
            # Remove currency symbols and commas
            cleaned = val.replace('PKR','').replace('SAR','').replace('AED','').replace('dh','').replace(',','').strip()
            return float(cleaned) if cleaned else 0.0
        return 0.0
    except:
        return 0.0

# 6. Service Selector
with st.expander("🚀 CONFIGURE YOUR PROJECT SCOPE", expanded=True):
    # Get unique categories, handling potential NaN values
    categories = df[cat_col].dropna().unique()
    if len(categories) > 0:
        category = st.selectbox("CATEGORY", categories)
        sub_df = df[df[cat_col] == category]
        
        # Get unique products, handling potential NaN values
        products = sub_df[prod_col].dropna().unique()
        if len(products) > 0:
            product = st.selectbox("PRODUCT SERVICE", products)
            units = st.number_input("UNITS REQUIRED", min_value=1, value=1, step=1)
            
            if st.button("➕ ADD TO QUOTATION"):
                # Get the matching row
                row = sub_df[sub_df[prod_col] == product].iloc[0]
                
                # Clean and calculate prices
                pkr_price = clean_num(row[pkr_col]) * units
                sar_price = clean_num(row[sar_col]) * units
                aed_price = clean_num(row[aed_col]) * units
                
                st.session_state.cart.append({
                    "name": product, 
                    "units": units,
                    "pkr": pkr_price,
                    "sar": sar_price,
                    "aed": aed_price
                })
                # Consolidate cart immediately after adding
                st.session_state.cart = consolidate_cart(st.session_state.cart)
                st.rerun()
        else:
            st.error("No products found in this category.")
    else:
        st.error("No categories found in the data.")

# 7. Summary & Total Valuation
if st.session_state.cart:
    # Consolidate cart before displaying (ensures no duplicates)
    st.session_state.cart = consolidate_cart(st.session_state.cart)
    
    totals = {"pkr": 0, "sar": 0, "aed": 0}
    st.markdown("<br><h3 style='letter-spacing:4px; font-weight:200; color: white;'>📋 CURRENT SCOPE</h3>", unsafe_allow_html=True)
    
    for i, item in enumerate(st.session_state.cart):
        totals["pkr"] += item["pkr"]
        totals["sar"] += item["sar"]
        totals["aed"] += item["aed"]
        
        # Enhanced cart item display
        col_1, col_2, col_3, col_4 = st.columns([3, 1, 1.5, 0.5])
        with col_1:
            st.markdown(f"**{item['name']}**")
        with col_2:
            st.markdown(f"x**{item['units']}**")
        with col_3:
            st.markdown(f"PKR **{item['pkr']:,.0f}**")
        with col_4:
            if st.button("🗑️", key=f"del_{i}"):
                st.session_state.cart.pop(i)
                st.rerun()

    # Premium Total Display with enhanced styling
    st.markdown(f"""
        <div style="border: 3px solid #37b36f; padding: 40px; border-radius: 20px; 
                   background: linear-gradient(135deg, rgba(55, 179, 111, 0.15), rgba(0, 0, 0, 0.8));
                   text-align: center; margin-top: 40px; box-shadow: 0 20px 50px rgba(55, 179, 111, 0.3);">
            <p style="letter-spacing: 8px; color: #37b36f; font-size: 0.9rem; font-weight: 700; margin-bottom: 20px;">
                ✦ TOTAL VALUATION ✦
            </p>
            <h1 style="color: white; font-size: 4rem; font-weight: 900; margin: 20px 0; 
                      text-shadow: 0 0 40px rgba(55, 179, 111, 0.5);">
                PKR {totals['pkr']:,.0f}
            </h1>
            <div style="display: flex; justify-content: center; gap: 60px; border-top: 2px solid #37b36f; 
                       padding-top: 30px; margin-top: 30px;">
                <div>
                    <p style="color: #37b36f; font-size: 1rem; font-weight:900; letter-spacing: 3px;">SAR</p>
                    <h2 style="color:white; font-weight:300; font-size: 2rem;">{totals['sar']:,.2f}</h2>
                </div>
                <div>
                    <p style="color: #37b36f; font-size: 1rem; font-weight:900; letter-spacing: 3px;">AED</p>
                    <h2 style="color:white; font-weight:300; font-size: 2rem;">{totals['aed']:,.2f}</h2>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Add a clear all button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🗑️ CLEAR ALL QUOTATION", use_container_width=True):
            st.session_state.cart = []
            st.rerun()

# Add footer
st.markdown("""
    <div style="text-align: center; margin-top: 50px; padding: 20px; border-top: 1px solid #333;">
        <p style="color: #666; font-size: 0.8rem;">✦ BAYUT STUDIOS ✦ PRIME QUOTATION ENGINE ✦</p>
    </div>
""", unsafe_allow_html=True)
