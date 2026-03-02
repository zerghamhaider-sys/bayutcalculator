import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Bayut Studios | Global Estimate Builder", layout="centered")

# 2. Luxury Design Layer (Rich Night, Glistening Stars & Premium UI)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@200;400;700&display=swap');

    /* Deep Space Background */
    .stApp {
        background-color: #000000;
        color: #F8F8F8;
        font-family: 'Montserrat', sans-serif;
    }

    /* High-Density Glistening Stars */
    .star-bg {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        z-index: -1; background: transparent;
        box-shadow: 
            10vw 20vh 1px #FFF, 30vw 10vh 2px #FFF, 50vw 40vh 1px #37b36f, 
            70vw 30vh 2px #FFF, 90vw 50vh 1px #FFF, 20vw 80vh 2px #37b36f,
            40vw 90vh 1px #FFF, 60vw 70vh 2px #FFF, 80vw 10vh 1px #FFF,
            15vw 15vh 1px #FFF, 85vw 85vh 2px #37b36f, 55vw 55vh 1px #FFF;
        animation: twinkle 4s infinite ease-in-out;
    }

    @keyframes twinkle {
        0%, 100% { opacity: 0.4; transform: scale(1); }
        50% { opacity: 1; transform: scale(1.2); filter: blur(1px); }
    }

    /* Premium Typography */
    .main-heading {
        letter-spacing: 12px;
        font-weight: 200;
        color: #FFFFFF;
        text-align: center;
        text-transform: uppercase;
        margin-top: 20px;
        opacity: 0.9;
    }

    /* Glassmorphism Input Cards */
    div.stExpander {
        border: 1px solid rgba(55, 179, 111, 0.3) !important;
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(20px) !important;
        border-radius: 20px !important;
    }

    /* Bayut Brand Buttons */
    div.stButton > button {
        background: linear-gradient(135deg, #1a6b4a 0%, #37b36f 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 15px 40px !important;
        font-weight: 600 !important;
        letter-spacing: 2px;
        box-shadow: 0 10px 20px rgba(55, 179, 111, 0.2);
        transition: 0.3s;
    }
    
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 15px 30px rgba(55, 179, 111, 0.4);
    }

    /* Bin Icon Styling */
    div[key^="del_"] > button {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        color: #ff4b4b !important;
        font-size: 1.5rem !important;
    }
    </style>
    <div class="star-bg"></div>
    """, unsafe_allow_html=True)

# 3. Branding Section
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("https://i.ibb.co/LzsV9Z6j/f774cc00-9f2e-4130-9644-1bddb2d6ae50.jpg", use_container_width=True)
st.markdown("<h1 class='main-heading'>Estimate Builder</h1>", unsafe_allow_html=True)

# 4. Initialize Project Cart
if 'cart' not in st.session_state:
    st.session_state.cart = []

# 5. Data Connection
url = "https://docs.google.com/spreadsheets/d/1qvBKlYH7q4dXsu7tEh9OLnKSydfONNRzGa-xjUYLB0g/edit?usp=sharing"

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(spreadsheet=url, ttl="1m")

    # Mapping your exact column names
    cat_col = "Product Category"
    prod_col = "Product"
    pkr_col = "Total Price (PKR)"
    sar_col = "Total Price (SAR)"
    aed_col = "Total Price (AED)"

    # Helper function to clean numeric strings from PKR, SAR, AED
    def clean_val(val):
        if isinstance(val, str):
            return float(val.replace('PKR', '').replace('SAR', '').replace('dh', '').replace(',', '').strip())
        return float(val)

    # 6. Service Selection (Glass Container)
    with st.expander("➕ ADD SERVICES TO PROJECT", expanded=not st.session_state.cart):
        c1, c2 = st.columns(2)
        with c1:
            category = st.selectbox("Category", df[cat_col].unique())
            filtered_df = df[df[cat_col] == category]
        with c2:
            product = st.selectbox("Product", filtered_df[prod_col].unique())
        
        units = st.number_input("Units Required", min_value=1, value=1, step=1)
        
        if st.button("ADD TO ESTIMATE"):
            selected_row = filtered_df[filtered_df[prod_col] == product].iloc[0]
            
            st.session_state.cart.append({
                "name": product,
                "units": units,
                "pkr": clean_val(selected_row[pkr_col]) * units,
                "sar": clean_val(selected_row[sar_col]) * units,
                "aed": clean_val(selected_row[aed_col]) * units
            })
            st.rerun()

    # 7. Your Selection Display
    if st.session_state.cart:
        st.markdown("---")
        st.markdown("<h3 style='font-weight:200; letter-spacing:3px;'>PROJECT SCOPE</h3>", unsafe_allow_html=True)
        
        totals = {"pkr": 0, "sar": 0, "aed": 0}
        
        for i, item in enumerate(st.session_state.cart):
            totals["pkr"] += item["pkr"]
            totals["sar"] += item["sar"]
            totals["aed"] += item["aed"]
            
            with st.container():
                col_a, col_b, col_c = st.columns([3, 1, 0.5])
                with col_a:
                    st.markdown(f"**{item['name']}**")
                    st.markdown(f"<p style='color: #888; font-size: 0.8rem;'>Quantity: {item['units']}</p>", unsafe_allow_html=True)
                with col_b:
                    st.markdown(f"PKR {item['pkr']:,.0f}")
                with col_c:
                    if st.button("🗑️", key=f"del_{i}"):
                        st.session_state.cart.pop(i)
                        st.rerun()
            st.markdown("<hr style='border-color: #222; margin: 10px 0;'>", unsafe_allow_html=True)

        # 8. Luxury Global Total Card
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
            <div style="border: 1px solid #37b36f; padding: 40px; border-radius: 20px; background: rgba(55, 179, 111, 0.05); text-align: center; backdrop-filter: blur(10px);">
                <p style="letter-spacing: 4px; color: #888; font-size: 0.8rem; text-transform: uppercase;">Estimated Project Total</p>
                <h1 style="color: white; margin: 15px 0; font-size: 3rem;">PKR {totals['pkr']:,.0f}</h1>
                <div style="display: flex; justify-content: center; gap: 50px; margin-top: 25px; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 20px;">
                    <div>
                        <p style="color: #37b36f; font-size: 0.7rem; margin-bottom: 5px;">SAUDI ARABIA</p>
                        <h2 style="font-weight: 400; margin: 0;">SAR {totals['sar']:,.0f}</h2>
                    </div>
                    <div>
                        <p style="color: #37b36f; font-size: 0.7rem; margin-bottom: 5px;">UNITED ARAB EMIRATES</p>
                        <h2 style="font-weight: 400; margin: 0;">AED {totals['aed']:,.0f}</h2>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"Syncing with Bayut Database... Please ensure columns match. Error: {e}")
