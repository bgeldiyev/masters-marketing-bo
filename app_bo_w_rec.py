import os

import streamlit as st

# --- 1. CONFIG ---
st.set_page_config(page_title="Best Shop | Mixed Portfolio", layout="wide")

# --- 2. THE CSS (Updated with 60% Gray Sliding Panel) ---
st.markdown("""
    <style>
    .block-container { padding-top: 3.5rem !important; }
    
    .logo-container {
        display: flex;
        font-family: "Arial Black", Gadget, sans-serif;
        font-size: 42px; font-weight: 900;
        letter-spacing: -2px; line-height: 1;
    }
    
    .box-orange { background-color: #333333; color: #f1c40f; padding: 5px 15px; border: 2px solid #333333; display: flex; align-items: center; }
    .box-green { background-color: #f1c40f; color: #333333; padding: 5px 15px; border: 2px solid #f1c40f; display: flex; align-items: center; }
    
    .category-bar {
        background-color: #333333; 
        padding: 10px 0px;
        display: flex; justify-content: center; gap: 50px;
        margin-top: 10px !important; margin-bottom: 20px !important;
        width: 100% !important;
        border-radius: 0px;
    }
    
    .cat-link { 
        font-weight: bold; color: #F5F5DC; font-size: 16px; 
        text-transform: uppercase; cursor: pointer; 
    }
    .cat-link:hover { color: #ffffff; }

    .stImage > img { 
        width: 100% !important; height: 300px !important;   
        object-fit: cover !important; border-radius: 8px; border: 1px solid #eee;
    }

    .detail-main-img img {
        max-height: 300px !important; width: auto !important;
        object-fit: contain !important; margin-bottom: 10px;
    }
    
    .small-img img {
        height: 60px !important; width: auto !important;
        border-radius: 4px; border: 1px solid #ddd;
    }

    .rating-text { color: #f39c12; font-weight: bold; font-size: 14px; margin: 0; }
    .price-text { font-size: 18px; font-weight: bold; color: #333; margin: 0; }

    .color-circle {
        height: 22px; width: 22px; border-radius: 50%; display: inline-block; 
        border: 2px solid #ddd; margin-right: 8px;
    }

    /* --- FIXED BOTTOM PANEL --- */
    @keyframes slideUp {
        from { transform: translateY(100%); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }

    div[data-testid="stVerticalBlock"]:has(#popup-marker) {
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        right: 0 !important;
        width: 100% !important;
        background-color: #999999 !important; /* 60% GRAY */
        padding: 15px 60px !important;
        border-top: 3px solid #f1c40f !important;
        box-shadow: 0px -10px 30px rgba(0,0,0,0.2) !important;
        z-index: 999999 !important;
        animation: slideUp 0.6s ease-out 3s both; /* 3s DELAY */
    }

    div[data-testid="stVerticalBlock"]:has(#popup-marker) * {
        color: white !important;
    }
    
    div[data-testid="stVerticalBlock"]:has(#popup-marker) img {
        background-color: white !important;
        height: 90px !important;
        object-fit: contain !important;
        border-radius: 4px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATA ---
IMAGE_FOLDER = "./Pictures_New" 
BACK_FOLDER = "./Pictures_Back" 

PRODUCT_TITLES = ["Adidas Runfalcon 5 (Men)", "Reebok Energen Run 4 (Women)", "XTEP Running Shoes (Men)", "Skechers Track Ripkent Sneaker (Men)", "WHITIN Running Shoes (Unisex)", "Nike Stellar Ride (Kids)", "Asics Gel-Excite 11 Sneaker (Men)", "New Balance Fresh Foam", "Brooks Adrenaline Gts 25 (Men)", "Nike Vomero 18 GORE-TEX (Men)", "New Balance 411 Sneaker (Men)", "Under Armour Charged Edge (Men)", "Nike Wildhorse 10 (Men)", "On Cloud 6 Sneaker (Men)", "HOKA Clifton 10 (Women)", "New Balance 1080"]
PRODUCT_PRICES = ["$60.00", "$69.99", "$139.99", "$69.95", "$49.99", "$59.99", "$90.00", "$139.99", "$160.00", "$169.99", "$49.99", "$65.00", "$149.99", "$138.85", "$129.99", "$159.99"]
PRODUCT_RATINGS = [4.3, 4.7, 4.3, 4.5, 4.3, 4.4, 4.5, 4.6, 4.7, 4.3, 4.1, 4.4, 4.4, 4.2, 4.6, 4.5]

BACK_TITLES = ["Top Rated", "Style Pick", "Performance", "Season Best", "New Arrival"]
BACK_PRICES = ["$160.00", "$49.99", "$60.00", "$43.99", "$65.00"]

def get_star_string(rating): return ("★" * int(rating)) + ("☆" * (5 - int(rating)))

# --- 4. STATE ---
if 'user_interest' not in st.session_state: st.session_state.user_interest = None
if 'cart_count' not in st.session_state: st.session_state.cart_count = 0
if 'liked' not in st.session_state: st.session_state.liked = False
if 'viewed_history' not in st.session_state: st.session_state.viewed_history = False 
if 'popup_closed' not in st.session_state: st.session_state.popup_closed = False

def get_images(folder):
    valid = ('.png', '.jpg', '.jpeg', '.webp', '.avif')
    return sorted([os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(valid)]) if os.path.exists(folder) else []

all_images = get_images(IMAGE_FOLDER)
back_images = get_images(BACK_FOLDER)

# --- 5. THE DELAYED "BECAUSE" PANEL ---
if st.session_state.viewed_history and not st.session_state.popup_closed:
    with st.container():
        st.markdown('<div id="popup-marker"></div>', unsafe_allow_html=True)
        p1, p2, p3 = st.columns([2, 5, 0.5])
        with p1:
            st.markdown("### Because you viewed this:")
        with p2:
            pcols = st.columns(5)
            for i in range(min(len(back_images), 5)):
                with pcols[i]:
                    st.image(back_images[i])
                    st.markdown(f"**{BACK_PRICES[i]}**")
        with p3:
            if st.button("✖", key="close_p"):
                st.session_state.popup_closed = True
                st.rerun()

# --- 6. HEADER ---
t1, t2, t3 = st.columns([2, 2, 1.2])
with t1: st.markdown('<div class="logo-container"><div class="box-orange">BEST</div><div class="box-green">SHOP</div></div>', unsafe_allow_html=True)
with t2: st.text_input("Search", placeholder="Search...", label_visibility="collapsed")
with t3: st.markdown(f"<p style='text-align:right; padding-top:20px; font-weight:bold;'>🛒 Cart ({st.session_state.cart_count})</p>", unsafe_allow_html=True)

st.markdown('<div class="category-bar"><span class="cat-link">Home</span><span class="cat-link">Categories</span><span class="cat-link">Brands</span></div>', unsafe_allow_html=True)

# --- 7. MAIN CONTENT ---
if not all_images:
    st.info("Add images.")
else:
    if st.session_state.user_interest is None:
        # GRID VIEW
        for r in range(4): 
            cols = st.columns(4)
            for c in range(4):
                idx = r * 4 + c
                if idx < len(all_images):
                    with cols[c]:
                        st.image(all_images[idx])
                        st.markdown(f"**{PRODUCT_TITLES[idx]}**")
                        st.markdown(f'<p class="price-text">{PRODUCT_PRICES[idx]}</p>', unsafe_allow_html=True)
                        if st.button("View Product", key=f"btn_{idx}", use_container_width=True):
                            st.session_state.viewed_history = True
                            st.session_state.user_interest = {"idx": idx, "path": all_images[idx], "name": PRODUCT_TITLES[idx], "price": PRODUCT_PRICES[idx], "rating": PRODUCT_RATINGS[idx]}
                            st.session_state.popup_closed = False
                            st.rerun()
    else:
        # PRODUCT DETAIL VIEW (Clean)
        item = st.session_state.user_interest
        if st.button("⬅ Back"):
            st.session_state.user_interest = None
            st.rerun()
            
        c_l, c_img, c_g, c_buy, c_r = st.columns([0.6, 1, 0.3, 1, 0.6])
        with c_img:
            st.markdown('<div class="detail-main-img">', unsafe_allow_html=True)
            st.image(item['path'])
            st.markdown('</div>', unsafe_allow_html=True)
            st.write("### Editions")
            sub1, sub2, _ = st.columns([1, 1, 1.5]) 
            if len(all_images) > 16:
                with sub1: st.image(all_images[16])
            if len(all_images) > 17:
                with sub2: st.image(all_images[17])
                
        with c_buy:
            st.header(item['name'])
            st.markdown(f'<p class="rating-text" style="font-size:18px;">{get_star_string(item["rating"])} ({item["rating"]})</p>', unsafe_allow_html=True)
            st.subheader(item['price'])
            st.write("**Size**")
            s_cols = st.columns(5)
            for i, s in enumerate(["42", "43", "44", "45", "46"]):
                s_cols[i].button(s, key=f"sz_{s}", use_container_width=True)
            st.divider()
            if st.button("ADD TO CART", use_container_width=True, type="primary"):
                st.session_state.cart_count += 1
                st.toast("Added!")
