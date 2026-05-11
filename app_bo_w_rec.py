import pandas as pd
import streamlit as st

import os
import time

# --- 1. CONFIG ---
st.set_page_config(page_title="Best Shop | Mixed Portfolio", layout="wide")

# --- 2. CSS ---
st.markdown("""
    <style>
    .block-container { padding-top: 3.5rem !important; }
    .logo-container { display: flex; font-family: "Arial Black", sans-serif; font-size: 42px; font-weight: 900; letter-spacing: -2px; line-height: 1; }
    .box-orange { background-color: #333333; color: #f1c40f; padding: 5px 15px; border: 2px solid #333333; display: flex; align-items: center; }
    .box-green { background-color: #f1c40f; color: #333333; padding: 5px 15px; border: 2px solid #f1c40f; display: flex; align-items: center; }
    .category-bar { background-color: #333333; padding: 10px 0px; display: flex; justify-content: center; gap: 50px; margin-top: 10px; margin-bottom: 20px; width: 100%; }
    .cat-link { font-weight: bold; color: #F5F5DC; font-size: 16px; text-transform: uppercase; cursor: pointer; }
    .stImage > img { width: 100% !important; height: 300px !important; object-fit: cover !important; border-radius: 8px; border: 1px solid #eee; }
    .detail-main-img img { max-height: 300px !important; width: auto !important; object-fit: contain !important; margin-bottom: 10px; }
    .small-img img { height: 60px !important; width: auto !important; border-radius: 4px; border: 1px solid #ddd; }
    .rating-text { color: #f39c12; font-weight: bold; font-size: 14px; margin: 0; }
    .price-text { font-size: 18px; font-weight: bold; color: #333; margin: 0; }
    .color-circle { height: 22px; width: 22px; border-radius: 50%; display: inline-block; border: 2px solid #ddd; margin-right: 8px; }
    [data-testid="stVerticalBlock"] > div:has(.rec-container) { background-color: #f2f2f2 !important; border-radius: 12px; padding: 20px; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATA ---
IMAGE_FOLDER, BACK_FOLDER = "./Pictures_New", "./Pictures_Back" 
PRODUCT_TITLES = ["Adidas Runfalcon 5 (Men)", "Reebok Energen Run 4 (Women)", "XTEP Running Shoes (Men)", "Skechers Track Ripkent Sneaker (Men)", "WHITIN Running Shoes (Unisex)", "Nike Stellar Ride (Kids)", "Asics Gel-Excite 11 Sneaker (Men)", "New Balance Fresh Foam", "Brooks Adrenaline Gts 25 (Men)", "Nike Vomero 18 GORE-TEX (Men)", "New Balance 411 Sneaker (Men)", "Under Armour Charged Edge (Men)", "Nike Wildhorse 10 (Men)", "On Cloud 6 Sneaker (Men)", "HOKA Clifton 10 (Women)", "New Balance 1080"]
BACK_TITLES = ["Top Rated Choice", "Style Inspired by You", "Performance Pick", "Season's Best", "New Arrival"]
PRODUCT_PRICES = ["$60.00", "$69.99", "$139.99", "$69.95", "$49.99", "$59.99", "$90.00", "$139.99", "$160.00", "$169.99", "$49.99", "$65.00", "$149.99", "$138.85", "$129.99", "$159.99"]
PRODUCT_RATINGS = [4.3, 4.7, 4.3, 4.5, 4.3, 4.4, 4.5, 4.6, 4.7, 4.3, 4.1, 4.4, 4.4, 4.2, 4.6, 4.5]

def get_star_string(rating): return ("★" * int(rating)) + ("☆" * (5 - int(rating)))
def get_images(folder):
    valid = ('.png', '.jpg', '.jpeg', '.webp', '.avif')
    return sorted([os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(valid)]) if os.path.exists(folder) else []

all_images, back_images = get_images(IMAGE_FOLDER), get_images(BACK_FOLDER)

# --- 4. STATE ---
if 'page' not in st.session_state: st.session_state.page = "home"
if 'user_interest' not in st.session_state: st.session_state.user_interest = None
if 'cart_count' not in st.session_state: st.session_state.cart_count = 0
if 'viewed_history' not in st.session_state: st.session_state.viewed_history = False 

# --- 5. SIDEBAR ---
with st.sidebar:
    st.header("Refine Search")
    st.divider()
    st.checkbox("Running", value=True); st.checkbox("Training"); st.checkbox("Lifestyle")
    st.subheader("Price Range")
    st.slider("Filter by Price", 0, 300, (40, 200))
    if st.button("Reset All Filters", use_container_width=True): st.rerun()

# --- 6. HEADER ---
t1, t2, t3 = st.columns([2, 2, 1.2])
with t1: st.markdown('<div class="logo-container"><div class="box-orange">BEST</div><div class="box-green">SHOP</div></div>', unsafe_allow_html=True)
with t2: st.text_input("Search", placeholder="Search brand...", label_visibility="collapsed")
with t3: st.markdown(f"<p style='text-align:right; padding-top:20px; font-weight:bold;'>🛒 Cart ({st.session_state.cart_count})</p>", unsafe_allow_html=True)
st.markdown('<div class="category-bar"><span class="cat-link">Home</span><span class="cat-link">Categories</span><span class="cat-link">Brands</span></div>', unsafe_allow_html=True)

# --- 7. MAIN ROUTING ---
if st.session_state.page == "home":
    for r in range(4):
        if r == 1 and st.session_state.viewed_history:
            st.markdown('<div class="rec-container">', unsafe_allow_html=True)
            st.subheader("Similar to what you just viewed")
            rel_cols = st.columns(5)
            for i in range(min(5, len(back_images))):
                with rel_cols[i]:
                    st.image(back_images[i])
                    st.markdown(f"**{BACK_TITLES[i]}**")
            st.markdown('</div>', unsafe_allow_html=True)

        cols = st.columns(4)
        for c in range(4):
            idx = r * 4 + c
            if idx < len(all_images):
                with cols[c]:
                    st.image(all_images[idx])
                    st.markdown(f"**{PRODUCT_TITLES[idx]}**")
                    st.markdown(f'<p class="price-text">{PRODUCT_PRICES[idx]}</p>', unsafe_allow_html=True)
                    if st.button("View Product", key=f"btn_{idx}", use_container_width=True):
                        st.session_state.user_interest = {"idx": idx, "path": all_images[idx], "name": PRODUCT_TITLES[idx], "price": PRODUCT_PRICES[idx], "rating": PRODUCT_RATINGS[idx]}
                        st.session_state.viewed_history, st.session_state.page = True, "detail"
                        st.rerun()
else:
    item = st.session_state.user_interest
    if st.button("⬅ Back to Collection"):
        st.session_state.page, st.session_state.user_interest = "home", None
        st.rerun()
        
    c_left, c_img, c_gap, c_buy, c_right = st.columns([0.6, 1, 0.3, 1, 0.6])
    with c_img:
        st.markdown('<div class="detail-main-img">', unsafe_allow_html=True)
        st.image(item['path'])
        st.markdown('</div>', unsafe_allow_html=True)
        st.write("### Editions")
        sub1, sub2, _ = st.columns([1, 1, 1.5])
        if len(all_images) > 17:
            with sub1: st.markdown('<div class="small-img">', unsafe_allow_html=True); st.image(all_images[16]); st.markdown('</div>', unsafe_allow_html=True)
            with sub2: st.markdown('<div class="small-img">', unsafe_allow_html=True); st.image(all_images[17]); st.markdown('</div>', unsafe_allow_html=True)
                
    with c_buy:
        st.header(item['name'])
        st.markdown(f'<p class="rating-text" style="font-size:18px;">{get_star_string(item["rating"])} ({item["rating"]})</p>', unsafe_allow_html=True)
        st.subheader(item['price'])
        st.write("**Colors**")
        c_cols = st.columns([1, 1, 1, 6])
        for i, color in enumerate(["gray", "white", "black"]):
            c_cols[i].markdown(f'<div class="color-circle" style="background-color: {color};"></div>', unsafe_allow_html=True)
        st.write("**Size**")
        s_cols = st.columns(5)
        for i, s in enumerate(["42", "43", "44", "45", "46"]): s_cols[i].button(s, key=f"sz_{s}")
        st.divider()
        if st.button("ADD TO CART", use_container_width=True, type="primary"):
            st.session_state.cart_count += 1
            st.toast("Added!")

    # --- DOCKER LOGIC ---
    docker_slot = st.empty()
    time.sleep(3)
    with docker_slot.container():
        st.write("---")
        _, mid, _ = st.columns([0.5, 3, 0.5])
        with mid:
            st.subheader("Because you viewed this, you may also like")
            rel_cols = st.columns(4)
            for i, r_idx in enumerate([11, 10, 3, 14]):
                with rel_cols[i]:
                    st.image(all_images[r_idx])
                    st.markdown(f"**{PRODUCT_TITLES[r_idx]}**")
                    st.markdown(f'<p class="price-text" style="font-size:15px;">{PRODUCT_PRICES[r_idx]}</p>', unsafe_allow_html=True)
