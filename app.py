import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Bayut Studios | Estimate Builder", layout="centered")
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Bayut Studios | Estimate Builder", layout="centered")

# 2. Rich Midnight Starfield CSS
st.markdown("""
    <style>
    /* Rich Deep Navy Background */
    .stApp {
        background: radial-gradient(ellipse at bottom, #1B2735 0%, #090A0F 100%);
        color: white;
        overflow: hidden;
    }

    /* Star Layer 1: Tiny & Many */
    .stars-small {
        position: fixed;
        top: 0; left: 0; width: 2px; height: 2px;
        background: transparent;
        box-shadow: 454px 105px #FFF, 207px 1012px #FFF, 1200px 200px #FFF, 800px 900px #FFF, 300px 400px #FFF, 1500px 600px #FFF, 50px 800px #FFF, 950px 150px #FFF;
        animation: animStar 50s linear infinite;
    }

    /* Star Layer 2: Medium & Glistening */
    .stars-medium {
        position: fixed;
        top: 0; left: 0; width: 4px; height: 4px;
        background: transparent;
        box-shadow: 100px 300px #FFF, 700px 400px #FFF, 1400px 700px #37b36f, 500px 100px #FFF, 1100px 900px #FFF;
        animation: animStar 100s linear infinite, twinkle 3s ease-in-out infinite;
        border-radius: 50%;
    }

    /* Animations */
    @keyframes animStar {
        from { transform: translateY(0px); }
        to { transform: translateY(-2000px); }
    }
    @keyframes twinkle {
        0%, 100% { opacity: 0.4; transform: scale(1); }
        50% { opacity: 1; transform: scale(1.4); filter: blur(1px); }
    }

    /* Premium UI Styling */
    div.stExpander {
        border: 1px solid rgba(55, 179, 111, 0.3);
        background: rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(20px);
        border-radius: 15px;
    }
    div.stButton > button {
        background-color: #1a6b4a !important;
        border: 1px solid #37b36f !important;
        box-shadow: 0 0 15px rgba(55, 179, 111, 0.4);
        border-radius: 10px;
        padding: 15px;
    }
    .total-card {
        border: 2px solid #37b36f;
        padding: 30px;
        border-radius: 15px;
        background: rgba(0, 0, 0, 0.6);
        box-shadow: 0 10px 40px rgba(55, 179, 111, 0.2);
    }
    </style>
    
    <div class="stars-small"></div>
    <div class="stars-medium"></div>
    """, unsafe_allow_html=True)

# 3. Logo & Brand
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("https://i.ibb.co/LzsV9Z6j/f774cc00-9f2e-4130-9644-1bddb2d6ae50.jpg")
st.markdown("<h3 style='text-align: center; color: white; letter-spacing: 5px; opacity: 0.9;'>ESTIMATE BUILDER</h3>", unsafe_allow_html=True)

# --- REST OF YOUR LOGIC (Session State, Connection, Cart) REMAINS THE SAME ---
# 4. Initialize Session State
if 'cart' not in st.session_state:
    st.session_state.cart = []

# 5. Data Connection
url = "https://docs.google.com/spreadsheets/d/1qvBKlYH7q4dXsu7tEh9OLnKSydfONNRzGa-xjUYLB0g/edit?usp=sharing"
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(spreadsheet=url, ttl="1m")

    cat_col = [c for c in df.columns if 'Category' in c][0]
    prod_col = [c for c in df.columns if 'Product' in c and 'Category' not in c][0]
    price_col = [c for c in df.columns if 'Price' in c and 'PKR' in c][0]

    # 6. Selection Interface
    with st.expander("➕ Add Service to Estimate", expanded=not st.session_state.cart):
        col1, col2 = st.columns(2)
        with col1:
            category = st.selectbox("Category", df[cat_col].unique())
            filtered_df = df[df[cat_col] == category]
        with col2:
            product = st.selectbox("Service", filtered_df[prod_col].unique())
        
        units = st.number_input("Units/Quantity", min_value=1, value=1, step=1)
        
        if st.button("Add to Cart"):
            price_data = filtered_df[filtered_df[prod_col] == product].iloc[0]
            price_val = float(str(price_data[price_col]).replace('PKR', '').replace(',', '').strip())
            
            st.session_state.cart.append({
                "service": product,
                "units": units,
                "price": price_val,
                "total": price_val * units
            })
            st.rerun()

    # 7. Cart Display
    if st.session_state.cart:
        st.markdown("---")
        st.markdown("### Your Selection")
        grand_total = 0
        
        for i, item in enumerate(st.session_state.cart):
            grand_total += item['total']
            with st.container():
                c1, c2, c3 = st.columns([3, 1, 0.5])
                with c1:
                    st.markdown(f"**{item['service']}**")
                    st.markdown(f"<p style='color: #bbb; font-size: 0.9rem; margin-top:0;'>{item['units']} unit(s) @ PKR {item['price']:,.0f}</p>", unsafe_allow_html=True)
                with c2:
                    st.markdown(f"<p style='margin-top: 10px; font-weight: bold;'>PKR {item['total']:,.0f}</p>", unsafe_allow_html=True)
                with c3:
                    if st.button("🗑️", key=f"del_{i}"):
                        st.session_state.cart.pop(i)
                        st.rerun()
                st.markdown("<hr style='margin: 5px 0; border-color: #333;'>", unsafe_allow_html=True)

        # 8. Grand Total
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
            <div class="total-card">
                <p style="color: #bbb; text-transform: uppercase; letter-spacing: 2px; font-size: 0.8rem;">Project Estimated Total</p>
                <h1 style="margin: 0; color: #37b36f;">PKR {grand_total:,.0f}</h1>
            </div>
            """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"Error loading data: {e}")
