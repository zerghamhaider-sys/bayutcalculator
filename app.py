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
