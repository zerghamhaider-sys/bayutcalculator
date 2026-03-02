import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Page Config & Theme
st.set_page_config(page_title="Bayut Studios | Estimate Builder", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    h1, h2, h3 { color: #37b36f !important; text-align: center; }
    .cart-box { border: 1px solid #333; padding: 15px; border-radius: 10px; background: #111; margin-bottom: 10px; }
    .total-box { border: 2px solid #37b36f; padding: 20px; border-radius: 15px; text-align: center; background: rgba(55, 179, 111, 0.1); }
    </style>
    """, unsafe_allow_html=True)

# 2. Header
st.image("https://i.ibb.co/V99SV7v/bayut-logo.png") # Updated to your logo
st.markdown("### PROJECT ESTIMATE BUILDER")

# 3. Initialize Cart (Session State)
if 'cart' not in st.session_state:
    st.session_state.cart = []

# 4. Data Connection
url = "https://docs.google.com/spreadsheets/d/1qvBKlYH7q4dXsu7tEh9OLnKSydfONNRzGa-xjUYLB0g/edit?usp=sharing"
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(spreadsheet=url, ttl="1m")

    # 5. Selection Area
    with st.expander("➕ Add Service to Estimate", expanded=True):
        cat_col = [c for c in df.columns if 'Category' in c][0]
        prod_col = [c for c in df.columns if 'Product' in c and 'Category' not in c][0]
        price_col = [c for c in df.columns if 'Price' in c and 'PKR' in c][0]

        col1, col2 = st.columns(2)
        with col1:
            category = st.selectbox("Category", df[cat_col].unique())
        with col2:
            product = st.selectbox("Service", df[df[cat_col] == category][prod_col].unique())
        
        units = st.number_input("Units/Quantity", min_value=1, value=1)
        
        if st.button("Add to Cart", use_container_width=True):
            # Get price logic
            row = df[df[prod_col] == product].iloc[0]
            price_val = float(str(row[price_col]).replace('PKR', '').replace(',', '').strip())
            
            # Add item to session state
            st.session_state.cart.append({
                "service": product,
                "units": units,
                "price": price_val,
                "total": price_val * units
            })
            st.toast(f"Added {product} to estimate!")

    # 6. Display Cart
    st.markdown("---")
    st.markdown("### 🛒 Your Estimate")

    if not st.session_state.cart:
        st.info("Your cart is empty. Add services above to begin.")
    else:
        grand_total = 0
        # Create a copy to allow deletion while iterating
        for i, item in enumerate(st.session_state.cart):
            with st.container():
                c1, c2, c3 = st.columns([3, 1, 0.5])
                with c1:
                    st.markdown(f"**{item['service']}** \n{item['units']} unit(s) @ PKR {item['price']:,.0f}")
                with c2:
                    st.markdown(f"**PKR {item['total']:,.0f}**")
                with c3:
                    # The "Bin" icon logic
                    if st.button("🗑️", key=f"del_{i}"):
                        st.session_state.cart.pop(i)
                        st.rerun()
                st.markdown("<hr style='margin: 5px 0; border-color: #222;'>", unsafe_allow_html=True)
                grand_total += item['total']

        # 7. Final Grand Total
        st.markdown(f"""
            <div class="total-box">
                <p style="color: #888; margin-bottom: 0;">ESTIMATED TOTAL</p>
                <h1 style="margin: 0;">PKR {grand_total:,.0f}</h1>
            </div>
            """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"Error loading data: {e}")
