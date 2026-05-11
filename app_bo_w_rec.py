
import os
import random

import pandas as pd
import streamlit as st

from datetime import datetime

# --- 1. CONFIG ---
st.set_page_config(page_title="Best Shop | Mixed Portfolio", layout="wide")

# --- 2. THE IMPROVED CSS (MATCHES WOREC + MOBILE READY) ---
st.markdown("""
    <style>
    .block-container { padding-top: 3.5rem !important; }
    
    .logo-container {
        display: flex;
        font-family: "Arial Black", Gadget, sans-serif;
        font-size: clamp(28px, 5vw, 42px);
        font-weight: 900;
        letter-spacing: -2px;
        line-height: 1;
    }
    
    .box-orange { background-color: #333333; color: #f1c40f; padding: 5px 15px; border: 2px solid #333333; display: flex; align-items: center; }
    .box-green { background-color: #f1c40f; color: #333333; padding: 5px 15px; border: 2px solid #f1c40f; display: flex; align-items: center; }
    
    .category-bar {
        background-color: #333333; 
        padding: 12px 10px;
        display: flex;
        justify-content: center;
        gap: clamp(15px, 3vw, 50px);
        margin-top: 10px !important;
        margin-bottom: 25px !important;
        width: 100% !important;
        overflow-x: auto;
        white-space: nowrap;
    }
    
    .cat-link { 
        font-weight: 800; 
        color: #F5F5DC !important; 
        font-size: 16px !important; 
        text-transform: uppercase; 
        cursor: pointer;
        letter-spacing: 1px;
    }
    .cat-link:hover { color: #ffffff !important; }

    /* GRID IMAGES */
    .stImage > img { 
        width: 100% !important;
        height: 280px !important;   
        object-fit: cover !important; 
        border-radius: 8px;
        border: 1px solid #eee;
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

    /* RECOMMENDATION CONTAINER */
    [data-testid="stVerticalBlock"] > div:has(.rec-container) {
        background-color: #f8f9fa !important; 
        border-radius: 12px;
        padding: 20px !important;
        margin-bottom: 20px !important;
        border: 1px solid #eee;
    }

    /* MOBILE FIX: Stack columns on small screens */
    @media (max-width: 680px) {
        [data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
            min-width: 100% !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATA (Restored & Path Fixed) ---
IMAGE_FOLDER = "Pictures_New" 
BACK_FOLDER = "Pictures_Back" 

PRODUCT_TITLES = [
    "Adidas Runfalcon 5", "Reebok Energen Run 4", "XTEP Running Shoes", "Skechers Track Ripkent Sneaker", 
    "WHITIN Running Shoes", "Nike Stellar Ride", "Asics Gel-Excite 11 Sneaker", "New Balance Fresh Foam", 
    "Brooks Adrenaline Gts 25", "Nike Vomero 18 GORE-TEX", "New Balance 411 Sneaker", "Under Armour Charged Edge", 
    "Nike Wildhorse 10", "On Cloud 6 Sneaker", "HOKA Clifton 10", "New Balance 1080"
]

BACK_TITLES = ["Top Rated Choice (Brooks Adrenaline Gts 25)", "Style Inspired by You (New Balance 411 Sneaker)", "Performance Pick (Reebok Work N Cushion 4.0)", "Season's Best (Puma Flyer Lite 3)", "New Arrival (Under Armour Charged Edge)"]
BACK_PRICES = ["$160.00", "$49.99", "$60.00", "$43.99", "$65.00"]
BACK_RATINGS = [4.7, 4.1, 4.3, 4.4, 4.4]

PRODUCT_PRICES = ["$60.00", "$69.99", "$139.99", "$69.95", "$49.99", "$59.99", "$90.00", "$139.99", "$160.00", "$169.99", "$49.99", "$65.00", "$149.99", "$138.85", "$129.99", "$159.99"]
PRODUCT_RATINGS = [4.3, 4.7, 4.3, 4.5, 4.3, 4.4, 4.5, 4.6, 4.7, 4.3, 4.1, 4.4, 4.4, 4.2, 4.6, 4.5]

def get_star_string(rating):
    return ("★" * int(rating)) + ("☆" * (5 - int(rating)))

def get_images(folder):
    valid = ('.png', '.jpg', '.jpeg', '.webp', '.avif')
    if os.path.exists(folder):
        files = [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(valid)]
        return sorted(files)
    return []

all_images = get_images(IMAGE_FOLDER)
back_images = get_images(BACK_FOLDER)

# --- 4. STATE ---
if 'user_interest' not in st.session_state: st.session_state.user_interest = None
if 'cart_count' not in st.session_state: st.session_state.cart_count = 0
if 'liked' not in st.session_state: st.session_state.liked = False
if 'viewed_history' not in st.session_state: st.session_state.viewed_history = False 

# --- 5. SIDEBAR ---
if st.session_state.user_interest is None:
    with st.sidebar:
        st.header("Refine Search")
        st.divider()
        st.subheader("Category")
        st.checkbox("Running", value=True)
        st.checkbox("Training")
        st.checkbox("Lifestyle")
        st.subheader("Price Range")
        st.slider("Filter by Price", 0, 300, (40, 200))
        if st.button("Reset All Filters", use_container_width=True): st.rerun()

# --- 6. HEADER ---
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

# --- 7. MAIN CONTENT ---
if not all_images:
    st.info(f"Please add images to the 'Pictures_New' folder.")
else:
    if st.session_state.user_interest is None:
        for r in range(4): 
            # Recommendation Row Logic
            if r == 1 and st.session_state.viewed_history:
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
                        if st.button("View Product", key=f"btn_{idx}", use_container_width=True):
                            if idx == 1: st.session_state.viewed_history = True
                            # Your Demo Logic
                            if "Reebok" in PRODUCT_TITLES[idx] or idx == 1:
                                st.session_state.user_interest = {"idx": idx, "path": all_images[idx], "name": PRODUCT_TITLES[idx], "price": PRODUCT_PRICES[idx], "rating": PRODUCT_RATINGS[idx]}
                                st.rerun()
                            else:
                                st.toast("Demo restricted to Reebok.")
    else:
        # DETAIL VIEW
        item = st.session_state.user_interest
        if st.button("⬅ Back to Collection"):
            st.session_state.user_interest = None
            st.rerun()
            
        c_left_margin, c_img, c_mid_gap, c_buy, c_right_margin = st.columns([0.2, 1, 0.1, 1, 0.2])
        
        with c_img:
            st.image(item['path'], use_container_width=True)
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
            if heart_col.button("❤️" if st.session_state.liked else "🤍", key="heart_btn"):
                st.session_state.liked = not st.session_state.liked
                st.rerun()
                
            st.markdown(f'<p class="rating-text" style="font-size:18px;">{get_star_string(item["rating"])} ({item["rating"]})</p>', unsafe_allow_html=True)
            st.subheader(item['price'])
            st.write("**Colors**")
            c_cols = st.columns([1, 1, 1, 6])
            for i, color in enumerate(["gray", "white", "black"]):
                c_cols[i].markdown(f'<div class="color-circle" style="background-color: {color};"></div>', unsafe_allow_html=True)
            
            st.write("**Size**")
            s_cols = st.columns(5)
            for i, s in enumerate(["42", "43", "44", "45", "46"]):
                s_cols[i].button(s, key=f"sz_{s}", use_container_width=True)
            
            st.divider()
            b1, b2 = st.columns(2)
            if b1.button("ADD", key="main_add", use_container_width=True, type="primary"):
                st.session_state.cart_count += 1
                st.toast(f"Added {item['name']}!")
            b2.button("BUY", key="buy_now", use_container_width=True)

        # BOTTOM RECOMMENDATIONS
        st.write("---")
        st.subheader("Because you viewed this, you may also like")
        rel_indices = [11, 10, 3, 14] 
        rel_cols = st.columns(4)
        for i, r_idx in enumerate(rel_indices):
            with rel_cols[i]:
                st.image(all_images[r_idx], use_container_width=True)
                st.markdown(f"**{PRODUCT_TITLES[r_idx]}**")
                st.markdown(f'<p class="rating-text">{get_star_string(PRODUCT_RATINGS[r_idx])} ({PRODUCT_RATINGS[r_idx]})</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="price-text" style="font-size:15px;">{PRODUCT_PRICES[r_idx]}</p>', unsafe_allow_html=True)
