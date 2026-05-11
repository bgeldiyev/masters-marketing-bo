import os

import streamlit as st

# --- 1. CONFIG ---
st.set_page_config(page_title="Best Shop | Mixed Portfolio", layout="wide")

# --- 2. THE "EQUALIZER" CSS + SLIDING PANEL CSS ---
st.markdown("""
    <style>
    .block-container { padding-top: 3.5rem !important; background-color: white !important; }
    
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
    }
    
    .cat-link { 
        font-weight: bold; color: #F5F5DC; font-size: 16px; 
        text-transform: uppercase; cursor: pointer; 
    }
    .cat-link:hover { color: #ffffff; }

    /* MAIN GRID IMAGES */
    .stImage > img { 
        width: 100% !important;
        height: 300px !important;   
        object-fit: cover !important; 
        border-radius: 8px; border: 1px solid #eee;
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
        border-radius: 4px; border: 1px solid #ddd;
    }

    .rating-text { color: #f39c12; font-weight: bold; font-size: 14px; margin: 0; }
    .price-text { font-size: 18px; font-weight: bold; color: #333; margin: 0; }

    /* --- ANIMATION & DOCKED PANEL (60% GRAY) --- */
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
        padding: 20px 60px !important;
        border-top: 4px solid #f1c40f !important;
        box-shadow: 0px -10px 30px rgba(0,0,0,0.3) !important;
        z-index: 999999 !important;
        animation: slideUp 0.6s ease-out 3s both; /* 3 SECOND DELAY */
    }

    /* Force text inside the gray bar to be white */
    div[data-testid="stVerticalBlock"]:has(#popup-marker) h3,
    div[data-testid="stVerticalBlock"]:has(#popup-marker) p,
    div[data-testid="stVerticalBlock"]:has(#popup-marker) b,
    div[data-testid="stVerticalBlock"]:has(#popup-marker) span {
        color: white !important;
    }

    div[data-testid="stVerticalBlock"]:has(#popup-marker) img { 
        background-color: white !important; 
        padding: 4px; border-radius: 5px; height: 110px !important; object-fit: contain !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATA ---
IMAGE_FOLDER, BACK_FOLDER = "./Pictures_New", "./Pictures_Back"

PRODUCT_TITLES = [
    "Adidas Runfalcon 5 (Men)", "Reebok Energen Run 4 (Women)", "XTEP Running Shoes (Men)", "Skechers Track Ripkent Sneaker (Men)", "WHITIN Running Shoes (Unisex)", "Nike Stellar Ride (Kids)",
    "Asics Gel-Excite 11 Sneaker (Men)", "New Balance Fresh Foam", "Brooks Adrenaline Gts 25 (Men)", "Nike Vomero 18 GORE-TEX (Men)",
    "New Balance 411 Sneaker (Men)", "Under Armour Charged Edge (Men)", "Nike Wildhorse 10 (Men)", "On Cloud 6 Sneaker (Men)", "HOKA Clifton 10 (Women)", "New Balance 1080"
]
PRODUCT_PRICES = ["$60.00", "$69.99", "$139.99", "$69.95", "$49.99", "$59.99", "$90.00", "$139.99", "$160.00", "$169.99", "$49.99", "$65.00", "$149.99", "$138.85", "$129.99", "$159.99"]
PRODUCT_RATINGS = [4.3, 4.7, 4.3, 4.5, 4.3, 4.4, 4.5, 4.6, 4.7, 4.3, 4.1, 4.4, 4.4, 4.2, 4.6, 4.5]

BACK_TITLES = ["Top Choice", "Style Pick", "Performance", "Season's Best", "New Arrival"]
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

# --- 5. THE SLIDING "BECAUSE" PANEL ---
if st.session_state.viewed_history and not st.session_state.popup_closed:
    with st.container():
        st.markdown('<div id="popup-marker"></div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns([2, 5, 0.5])
        with c1:
            st.markdown("### Because you viewed this style:")
        with c2:
            rec_cols = st.columns(5)
            for i in range(min(len(back_images), 5)):
                with rec_cols[i]:
                    st.image(back_images[i])
                    st.markdown(f"**{BACK_PRICES[i]}**")
        with c3:
            if st.button("✖", key="close_dock"):
                st.session_state.popup_closed = True
                st.rerun()

# --- 6. SIDEBAR ---
if st.session_state.user_interest is None:
    with st.sidebar:
        st.header("Refine Search")
        st.divider()
        st.checkbox("Running", value=True)
        st.slider("Filter by Price", 0, 300, (40, 200))
        if st.button("Reset All Filters", use_container_width=True): st.rerun()

# --- 7. HEADER ---
t1, t2, t3 = st.columns([2, 2, 1.2])
with t1: st.markdown('<div class="logo-container"><div class="box-orange">BEST</div><div class="box-green">SHOP</div></div>', unsafe_allow_html=True)
with t2: st.text_input("Search", placeholder="Search brand...", label_visibility="collapsed")
with t3: st.markdown(f"<p style='text-align:right; padding-top:20px; font-weight:bold;'>🛒 Cart ({st.session_state.cart_count})</p>", unsafe_allow_html=True)

st.markdown('<div class="category-bar"><span class="cat-link">Home</span><span class="cat-link">Categories</span><span class="cat-link">New Arrivals</span><span class="cat-link">Brands</span></div>', unsafe_allow_html=True)

# --- 8. MAIN CONTENT ---
if not all_images:
    st.info("Please add images.")
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
                        st.markdown(f'<p class="rating-text">{get_star_string(PRODUCT_RATINGS[idx])} ({PRODUCT_RATINGS[idx]})</p>', unsafe_allow_html=True)
                        st.markdown(f'<p class="price-text">{PRODUCT_PRICES[idx]}</p>', unsafe_allow_html=True)
                        if st.button("View Product", key=f"btn_{idx}", use_container_width=True):
                            st.session_state.viewed_history = True
                            st.session_state.user_interest = {"idx": idx, "path": all_images[idx], "name": PRODUCT_TITLES[idx], "price": PRODUCT_PRICES[idx], "rating": PRODUCT_RATINGS[idx]}
                            st.session_state.popup_closed = False # Reset panel for new view
                            st.rerun()
    else:
        # PRODUCT DETAIL VIEW (Static "Because" removed as requested)
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
                with sub1: st.image(all_images[16])
            if len(all_images) > 17:
                with sub2: st.image(all_images[17])
                
        with c_buy:
            title_col, heart_col = st.columns([5, 1])
            title_col.header(item['name'])
            if heart_col.button("❤️" if st.session_state.liked else "🤍", key="heart_btn"):
                st.session_state.liked = not st.session_state.liked
                st.rerun()
            st.markdown(f'<p class="rating-text" style="font-size:18px;">{get_star_string(item["rating"])} ({item["rating"]})</p>', unsafe_allow_html=True)
            st.subheader(item['price'])
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
