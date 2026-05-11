import pandas as pd
import streamlit as st

import streamlit.components.v1 as components

import os
import base64

# =========================================================
# 1. CONFIG & IMAGE CONVERSION
# =========================================================
st.set_page_config(page_title="Best Shop | Mixed Portfolio", layout="wide")

def img_to_base64(path):
    try:
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return ""

# =========================================================
# 2. THE "EQUALIZER" CSS (EXACTLY FROM YOUR SNIPPET)
# =========================================================
st.markdown("""
    <style>
    .block-container { padding-top: 3.5rem !important; padding-bottom: 150px !important; }
    
    .logo-container {
        display: flex;
        font-family: "Arial Black", Gadget, sans-serif;
        font-size: 42px;
        font-weight: 900;
        letter-spacing: -2px;
        line-height: 1;
    }
    
    .box-orange { background-color: #333333; color: #f1c40f; padding: 5px 15px; border: 2px solid #333333; display: flex; align-items: center; }
    .box-green { background-color: #f1c40f; color: #333333; padding: 5px 15px; border: 2px solid #f1c40f; display: flex; align-items: center; }
    
    .category-bar {
        background-color: #333333; 
        padding: 10px 0px;
        display: flex;
        justify-content: center;
        gap: 50px;
        margin-top: 10px !important;
        margin-bottom: 20px !important;
        width: 100% !important;
    }
    
    .cat-link { 
        font-weight: bold; 
        color: #F5F5DC; 
        font-size: 16px; 
        text-transform: uppercase; 
        cursor: pointer; 
    }
    .cat-link:hover { color: #ffffff; }

    /* MAIN GRID IMAGES */
    .stImage > img { 
        width: 100% !important;
        height: 300px !important;   
        object-fit: cover !important; 
        border-radius: 8px;
        border: 1px solid #eee;
    }

    /* DETAIL IMAGE */
    .detail-main-img img {
        max-height: 300px !important; 
        width: auto !important;
        object-fit: contain !important;
        margin-bottom: 10px;
    }
    
    .small-img img {
        height: 60px !important;   
        width: auto !important;
        border-radius: 4px;
        border: 1px solid #ddd;
    }

    .rating-text { color: #f39c12; font-weight: bold; font-size: 14px; margin: 0; }
    .price-text { font-size: 18px; font-weight: bold; color: #333; margin: 0; }

    .color-circle {
        height: 22px; width: 22px; border-radius: 50%; display: inline-block; 
        border: 2px solid #ddd; margin-right: 8px;
    }

    /* THE GRAY BOX WRAPPER */
    [data-testid="stVerticalBlock"] > div:has(.rec-container) {
        background-color: #f2f2f2 !important; 
        border-radius: 12px;
        padding-top: 0px !important; 
        margin-top: 10px !important; 
    }

    .rec-container h3 {
        margin-top: -90px !important; 
        padding-top: 0px !important;
        font-size: 22px !important;
        margin-bottom: 5px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# =========================================================
# 3. DATA
# =========================================================
IMAGE_FOLDER, BACK_FOLDER = "./Pictures_New", "./Pictures_Back"

PRODUCT_TITLES = ["Adidas Runfalcon 5", "Reebok Energen Run 4", "XTEP Running Shoes", "Skechers Track Ripkent", "WHITIN Running", "Nike Stellar Ride", "Asics Gel-Excite 11", "New Balance Fresh Foam", "Brooks Adrenaline Gts 25", "Nike Vomero 18", "New Balance 411", "Under Armour Charged Edge", "Nike Wildhorse 10", "On Cloud 6", "HOKA Clifton 10", "New Balance 1080"]
BACK_TITLES = ["Top Rated Choice", "Style Inspired by You", "Performance Pick", "Season's Best", "New Arrival"]
BACK_PRICES = ["$160.00", "$49.99", "$60.00", "$43.99", "$65.00"]
BACK_RATINGS = [4.7, 4.1, 4.3, 4.4, 4.4]
PRODUCT_PRICES = ["$60.00", "$69.99", "$139.99", "$69.95", "$49.99", "$59.99", "$90.00", "$139.99", "$160.00", "$169.99", "$49.99", "$65.00", "$149.99", "$138.85", "$129.99", "$159.99"]
PRODUCT_RATINGS = [4.3, 4.7, 4.3, 4.5, 4.3, 4.4, 4.5, 4.6, 4.7, 4.3, 4.1, 4.4, 4.4, 4.2, 4.6, 4.5]

def get_star_string(rating): return ("★" * int(rating)) + ("☆" * (5 - int(rating)))
def get_images(folder):
    valid = ('.png', '.jpg', '.jpeg', '.webp', '.avif')
    return sorted([os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(valid)]) if os.path.exists(folder) else []

all_images, back_images = get_images(IMAGE_FOLDER), get_images(BACK_FOLDER)

# =========================================================
# 4. STATE & SIDEBAR LOGIC
# =========================================================
if 'user_interest' not in st.session_state: st.session_state.user_interest = None
if 'cart_count' not in st.session_state: st.session_state.cart_count = 0
if 'viewed_history' not in st.session_state: st.session_state.viewed_history = False
if 'liked' not in st.session_state: st.session_state.liked = False

# Sidebar ONLY if on Home Page
if st.session_state.user_interest is None:
    with st.sidebar:
        st.header("Refine Search")
        st.divider()
        st.subheader("Category")
        st.checkbox("Running", value=True); st.checkbox("Training"); st.checkbox("Lifestyle")
        st.subheader("Price Range")
        st.slider("Filter by Price", 0, 300, (40, 200))
        if st.button("Reset All Filters", use_container_width=True): st.rerun()

# =========================================================
# 5. HEADER (WITH ALL LINKS)
# =========================================================
t1, t2, t3 = st.columns([2, 2, 1.2])
with t1: st.markdown('<div class="logo-container"><div class="box-orange">BEST</div><div class="box-green">SHOP</div></div>', unsafe_allow_html=True)
with t2: st.text_input("Search", placeholder="Search brand or style...", label_visibility="collapsed")
with t3: st.markdown(f"<p style='text-align:right; padding-top:20px; font-size:14px; font-weight:bold;'>🛒 Cart ({st.session_state.cart_count})</p>", unsafe_allow_html=True)

st.markdown('''
    <div class="category-bar">
        <span class="cat-link">Home</span>
        <span class="cat-link">Categories</span>
        <span class="cat-link">New Arrivals</span>
        <span class="cat-link">Brands</span>
        <span class="cat-link">Checkout</span>
        <span class="cat-link">Contact</span>
    </div>
''', unsafe_allow_html=True)

# =========================================================
# 6. MAIN CONTENT
# =========================================================
if st.session_state.user_interest is None:
    # --- GRID VIEW ---
    for r in range(4):
        if r == 1 and st.session_state.viewed_history:
            # THIS IS YOUR EXACT GRAY BOX STRUCTURE
            with st.container():
                st.markdown('<div class="rec-container">', unsafe_allow_html=True)
                st.subheader("Similar to what you just viewed")
                rel_cols = st.columns(5)
                for i in range(5):
                    with rel_cols[i]:
                        if i < len(back_images):
                            st.image(back_images[i])
                            st.markdown(f"**{BACK_TITLES[i]}**")
                            st.markdown(f'<p class="rating-text">{get_star_string(BACK_RATINGS[i])} ({BACK_RATINGS[i]})</p>', unsafe_allow_html=True)
                            st.markdown(f'<p class="price-text">{BACK_PRICES[i]}</p>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

        cols = st.columns(4)
        for c in range(4):
            idx = r * 4 + c
            if idx < len(all_images):
                with cols[c]:
                    st.image(all_images[idx])
                    st.markdown(f"**{PRODUCT_TITLES[idx]}**")
                    st.markdown(f'<p class="rating-text">{get_star_string(PRODUCT_RATINGS[idx])} ({PRODUCT_RATINGS[idx]})</p>', unsafe_allow_html=True)
                    st.markdown(f'<p class="price-text">{PRODUCT_PRICES[idx]}</p>', unsafe_allow_html=True)
                    if st.button("View Product", key=f"v_{idx}", use_container_width=True):
                        st.session_state.user_interest = {"idx": idx, "path": all_images[idx], "name": PRODUCT_TITLES[idx], "price": PRODUCT_PRICES[idx], "rating": PRODUCT_RATINGS[idx]}
                        st.session_state.viewed_history = True
                        st.rerun()
else:
    # --- PRODUCT DETAIL VIEW (NO SIDEBAR) ---
    item = st.session_state.user_interest
    if st.button("⬅ Back to Collection"):
        st.session_state.user_interest = None
        st.rerun()
        
    c_left, c_img, c_gap, c_buy, c_right = st.columns([0.6, 1, 0.3, 1, 0.6])
    with c_img:
        st.markdown('<div class="detail-main-img">', unsafe_allow_html=True)
        st.image(item['path'])
        st.markdown('</div>', unsafe_allow_html=True)
        st.write("### Editions")
        sub1, sub2, _ = st.columns([1, 1, 1.5])
        if len(all_images) > 16:
            with sub1:
                st.markdown('<div class="small-img">', unsafe_allow_html=True)
                st.image(all_images[16])
                st.markdown('</div>', unsafe_allow_html=True)
        if len(all_images) > 17:
            with sub2:
                st.markdown('<div class="small-img">', unsafe_allow_html=True)
                st.image(all_images[17])
                st.markdown('</div>', unsafe_allow_html=True)
                
    with c_buy:
        title_col, heart_col = st.columns([5, 1])
        title_col.header(item['name'])
        if heart_col.button("❤️" if st.session_state.liked else "🤍", key="h_btn"):
            st.session_state.liked = not st.session_state.liked
            st.rerun()
            
        st.markdown(f'<p class="rating-text" style="font-size:18px;">{get_star_string(item["rating"])} ({item["rating"]})</p>', unsafe_allow_html=True)
        st.subheader(item['price'])
        st.write("**Colors**")
        st.markdown('<div class="color-circle" style="background-color:gray;"></div><div class="color-circle" style="background-color:white;"></div><div class="color-circle" style="background-color:black;"></div>', unsafe_allow_html=True)
        
        st.write("**Size**")
        s_cols = st.columns(5)
        for i, s in enumerate(["42", "43", "44", "45", "46"]):
            s_cols[i].button(s, key=f"sz_{s}", use_container_width=True)
        
        st.divider()
        b1, b2 = st.columns(2)
        if b1.button("ADD", key="main_add", use_container_width=True, type="primary"):
            st.session_state.cart_count += 1
            st.toast("Added!")
        b2.button("BUY", key="buy_now", use_container_width=True)

    # --- 3S SLIDING DOCK ---
    rel_indices = [11, 10, 3, 14]
    cards_html = "".join([f"""
        <div style="min-width:180px; max-width:200px; background:#f9f9f9; padding:15px; border-radius:12px; text-align:center; border:1px solid #ddd; flex: 0 0 auto;">
            <img src="data:image/png;base64,{img_to_base64(all_images[i])}" style="width:100%; height:110px; object-fit:cover; border-radius:8px; margin-bottom:8px;">
            <div style="font-size:13px; font-weight:bold; color:#333; margin-bottom:4px; height:32px; overflow:hidden;">{PRODUCT_TITLES[i]}</div>
            <div style="color:#f39c12; font-size:12px; margin-bottom:4px;">{get_star_string(PRODUCT_RATINGS[i])}</div>
            <div style="font-size:14px; font-weight:700; color:#222;">{PRODUCT_PRICES[i]}</div>
        </div>""" for i in rel_indices])

    components.html(f"""
    <div id="dock-container" style="position:fixed; bottom:-400px; left:50%; transform:translateX(-50%); width:100%; max-width:1200px; background:white; padding:25px; border-radius:25px 25px 0 0; box-shadow:0 -10px 40px rgba(0,0,0,0.2); transition: bottom 0.8s ease; z-index:9999; font-family: sans-serif;">
        <h3 style="margin-top:0; text-align:center; color:#333; margin-bottom:20px;">Because you viewed this...</h3>
        <div style="display:flex; gap:20px; justify-content:center; overflow-x:auto;">{cards_html}</div>
    </div>
    <script>setTimeout(() => {{ document.getElementById("dock-container").style.bottom = "0px"; }}, 3000);</script>
    """, height=400)
