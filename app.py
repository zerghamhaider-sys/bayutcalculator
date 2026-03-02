import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Page Setup
st.set_page_config(page_title="Bayut Studios | Global Estimate Builder", layout="centered")

# 2. Luxury Starfield & Glass UI
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@200;400;700&display=swap');

    .stApp {
        background-color: #000000;
        color: #E0E0E0;
        font-family: 'Montserrat', sans-serif;
    }

    /* Ultra-Dense Glistening Starfield */
    .star-bg {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        z-index: -1; background: transparent;
        box-shadow: 10vw 10vh #fff, 25vw 40vh #fff, 45vw 15vh #37b36f, 70vw 80vh #fff, 85vw 30vh #fff, 15vw 90vh #37b36f, 60vw 50vh #fff, 95vw 10vh #fff, 35vw 75vh #fff, 55vw 20vh #37b36f, 5vw 55vh #fff, 80vw 65vh #fff;
        animation: twinkle 4s infinite ease-in-out;
    }

    @keyframes twinkle {
        0%, 100% { opacity: 0.3; transform: scale(1); }
        50% { opacity: 0.9; transform: scale(1.1); filter: blur(1px); }
    }

    /* Premium Headings */
    .main-heading {
        letter-spacing: 12px;
        font-weight: 200;
        color: #F8F8F8;
        text-align: center;
        text-transform: uppercase;
        margin-top: 20px;
    }

    /* Glassmorphism Cards */
    div.stExpander {
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(20px) !important;
        border-radius: 20px !important;
    }

    /* Bayut Green Buttons */
    div.stButton > button {
        background: linear-gradient(135deg, #1a6b4a 0%, #37b36f 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 15px 40px !important;
        font-weight: 600 !important;
        letter-spacing: 2px;
        box-shadow: 0 10px 20px rgba(55, 179, 111, 0.2);
    }
    </style>
    <div class="star-bg"></div>
    """, unsafe_allow_html=True)

# 3. Branding
st.image("https://i.ibb.co/LzsV9Z6j/f774cc00-9f2e-4130-9644-1bddb2d6ae50.jpg")
st.markdown("<h1 class='main-heading'>Estimate Builder</h1>", unsafe_allow_html=True)

# 4. Currency Constants (Update these as needed)
SAR_RATE = 0.013  # 1 PKR to SAR
AED_RATE = 0.013  # 1 PKR to AED

# 5. Data Connection
if 'cart' not in st.session_state:
    st.session_state.cart = []

url = "https://docs.google.com/spreadsheets/d/1qvBKlYH7q4dXsu7tEh9OLnKSydfONNRzGa-xjUYLB0g/edit?usp=sharing"
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(spreadsheet=url, ttl="1m")

    # Selection Logic
    with st.expander("➕ SELECT SERVICES"):
        cat = st.selectbox("Category", df['Product Category'].unique())
        prod = st.selectbox("Product", df[df['Product Category'] == cat]['Product'].unique())
        qty = st.number_input("Units", min_value=1, value=1)
        
        if st.button("ADD TO PROJECT"):
            row = df[df['Product'] == prod].iloc[0]
            # Cleaning the price string to float
            price_pkr = float(str(row['Total Price (PKR)']).replace('PKR', '').replace(',', '').strip())
            
            st.session_state.cart.append({
                "item": prod,
                "qty": qty,
                "pkr": price_pkr * qty
            })
            st.rerun()

    # 6. The Cart Display
    if st.session_state.cart:
        st.markdown("---")
        total_pkr = 0
        for i, item in enumerate(st.session_state.cart):
            total_pkr += item['pkr']
            c1, c2, c3 = st.columns([3, 1, 0.5])
            with c1:
                st.markdown(f"<span style='color:#37b36f;'>●</span> {item['item']} (x{item['qty']})", unsafe_allow_html=True)
            with c2:
                st.markdown(f"PKR {item['pkr']:,.0f}")
            with c3:
                if st.button("🗑️", key=f"del_{i}"):
                    st.session_state.cart.pop(i)
                    st.rerun()

        # 7. Final Global Totals
        total_sar = total_pkr * SAR_RATE
        total_aed = total_pkr * AED_RATE

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
            <div style="background: rgba(255,255,255,0.05); padding: 40px; border-radius: 20px; border: 1px solid #37b36f; text-align: center;">
                <p style="letter-spacing: 3px; color: #888;">TOTAL ESTIMATE</p>
                <h1 style="color: white; margin: 10px 0;">PKR {total_pkr:,.0f}</h1>
                <div style="display: flex; justify-content: center; gap: 40px; border-top: 1px solid #333; pt-20px; margin-top: 20px;">
                    <div><p style="color:#888; font-size: 0.8rem;">SAR</p><h3 style="color:#37b36f;">{total_sar:,.2f}</h3></div>
                    <div><p style="color:#888; font-size: 0.8rem;">AED (DUBAI)</p><h3 style="color:#37b36f;">{total_aed:,.2f}</h3></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"Waiting for Sheet Connection... ({e})")
