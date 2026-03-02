import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Bayut Studios | Estimate Builder", layout="centered")
# 2. Premium Design Layer (High Visibility Starfield & Custom Styles)
st.markdown("""
    <style>
    /* Main Background & Text */
    .stApp {
        background-color: #010101; /* Even deeper black for contrast */
        color: white;
        font-family: 'Segoe UI', Roboto, sans-serif;
    }

    /* Input Section - Glassmorphism Effect */
    div.stExpander {
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 12px;
        background: rgba(255,255,255,0.07);
        backdrop-filter: blur(15px);
    }
    
    /* Sexy Green Buttons */
    div.stButton > button {
        background-color: #1a6b4a;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 2px;
        box-shadow: 0 4px 15px rgba(26, 107, 74, 0.6); /* Glow on button */
        width: 100%;
    }

    /* Final Total Card */
    .total-card {
        border: 2px solid #37b36f;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        background: rgba(55, 179, 111, 0.12);
        box-shadow: 0 0 50px rgba(55, 179, 111, 0.2); /* Outer glow */
        backdrop-filter: blur(5px);
    }
    </style>

    <div style="position:fixed; top:0; left:0; width:100%; height:100%; z-index:-1;" id="particles-js"></div>
    <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
    <script>
        particlesJS("particles-js", {
            "particles": {
                "number": { "value": 180, "density": { "enable": true, "value_area": 800 } },
                "color": { "value": "#ffffff" },
                "shape": { "type": "circle" },
                "opacity": { 
                    "value": 1.0,  /* Full opacity base */
                    "random": true, 
                    "anim": { "enable": true, "speed": 1.5, "opacity_min": 0.4, "sync": false } 
                },
                "size": { 
                    "value": 4.5, /* Bigger, crisp stars */
                    "random": true, 
                    "anim": { "enable": true, "speed": 3, "size_min": 1.5, "sync": false } 
                },
                "line_linked": { "enable": false },
                "move": { 
                    "enable": true, 
                    "speed": 0.6, 
                    "direction": "none", 
                    "random": true, 
                    "straight": false, 
                    "out_mode": "out", 
                    "bounce": false 
                }
            },
            "interactivity": { "detect_on": "canvas", "events": { "onhover": { "enable": false }, "onclick": { "enable": false }, "resize": true } },
            "retina_detect": true
        });
    </script>
    """, unsafe_allow_html=True)

# 3. Header & Logo
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("https://i.ibb.co/LzsV9Z6j/f774cc00-9f2e-4130-9644-1bddb2d6ae50.jpg")
st.markdown("<h3 style='text-align: center; color: white; letter-spacing: 5px; opacity: 0.9;'>ESTIMATE BUILDER</h3>", unsafe_allow_html=True)
st.markdown("---")

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
