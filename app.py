import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Bayut Studios | Estimate Builder", layout="centered")

# 2. Ultra-Rich Starfield & Luxury UI
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&display=swap');

    /* Pure Black Background with Deep Space Depth */
    .stApp {
        background: radial-gradient(circle at center, #0a0a0a 0%, #000000 100%);
        color: white;
        font-family: 'Inter', sans-serif;
    }

    /* Multi-Layered CSS Stars */
    .star-layer {
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        pointer-events: none;
        z-index: -1;
    }

    /* Small distant stars */
    .stars1 {
        background: transparent;
        box-shadow: 100px 100px #fff, 400px 300px #fff, 800px 500px #fff, 1200px 100px #fff, 1500px 800px #fff, 200px 900px #fff, 600px 200px #fff, 1000px 700px #fff, 1400px 400px #fff, 300px 600px #fff;
        width: 1px; height: 1px;
        animation: moveStars 120s linear infinite;
    }

    /* Medium glistening stars */
    .stars2 {
        background: transparent;
        box-shadow: 250px 150px #37b36f, 750px 350px #fff, 1150px 650px #37b36f, 150px 850px #fff, 950px 450px #fff, 1350px 250px #37b36f;
        width: 3px; height: 3px;
        border-radius: 50%;
        animation: moveStars 80s linear infinite, twinkle 4s ease-in-out infinite;
    }

    @keyframes moveStars {
        from { transform: translateY(0); }
        to { transform: translateY(-1000px); }
    }

    @keyframes twinkle {
        0%, 100% { opacity: 0.3; transform: scale(1); }
        50% { opacity: 1; transform: scale(1.5); filter: blur(1px); }
    }

    /* Better Text & Headings */
    h3 {
        letter-spacing: 6px !important;
        font-weight: 300 !important;
        text-transform: uppercase;
        color: #ffffff !important;
    }

    /* Luxury Glassmorphism Container */
    div.stExpander {
        border: 1px solid rgba(55, 179, 111, 0.2) !important;
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(25px) !important;
        border-radius: 20px !important;
        box-shadow: 0 10px 40px rgba(0,0,0,0.5);
    }

    /* Dark Green Brand Buttons */
    div.stButton > button {
        background-color: #1a6b4a !important;
        border: 1px solid rgba(55, 179, 111, 0.5) !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 20px !important;
        font-weight: 700 !important;
        letter-spacing: 2px;
        transition: 0.4s;
    }

    div.stButton > button:hover {
        background-color: #37b36f !important;
        box-shadow: 0 0 25px rgba(55, 179, 111, 0.4);
    }
    </style>
    
    <div class="star-layer stars1"></div>
    <div class="star-layer stars2"></div>
    """, unsafe_allow_html=True)

# 3. Logo & Title Section
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    # Ensuring logo is sharp and centered
    st.image("https://i.ibb.co/LzsV9Z6j/f774cc00-9f2e-4130-9644-1bddb2d6ae50.jpg", use_container_width=True)
st.markdown("<h3>ESTIMATE BUILDER</h3>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# --- YOUR EXISTING LOGIC CONTINUES HERE ---

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
