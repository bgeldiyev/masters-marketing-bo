
import pandas as pd
import streamlit as st

import os

# --- 1. CONFIG ---
st.set_page_config(page_title="Best Shop | Static Portfolio", layout="wide")

# --- 2. THE "EQUALIZER" CSS ---
st.markdown("""
    <style>
    .block-container { padding-top: 3.5rem !important; }
    
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
        padding: 12px 0px;
        display: flex;
        justify-content: center;
        gap: 50px;
        margin-top: 10px !important;
        margin-bottom: 25px !important;
        width: 100% !important;
        border-radius: 0px;
    }
    
    .cat-link { 
        font-weight: 800; 
        color: #F5F5DC !important; 
        font-size: 18px !important; 
        text-transform: uppercase; 
        cursor: pointer;
        letter-spacing: 1px;
    }
    .cat-link:hover { color: #ffffff !important; }

    .stImage > img { 
        width: 100% !important;
        height: 300px !important;   
        object-fit: cover !important; 
        border-radius: 8px;
        border: 1px solid #eee;
    }
    
    .small-img img {
        height: 80px !important;   
        width: auto !important;
        border-radius: 4px;
        border: 1px solid #ddd;
    }

    .rating-text { color: #f39c12; font-weight: bold; font-size: 14px; margin: 0; }
    .price-text { font-size: 18px; font-weight: bold; color: #333; margin: 0; }

    .color-circle {
        height: 25px; width: 25px; border-radius: 50%; display: inline-block; 
        border: 2px solid #ddd; margin-right: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATA ---
IMAGE_FOLDER = "./Pictures_New" 

PRODUCT_TITLES = [
    "Adidas Runfalcon 5 (Men)", "Reebok Energen Run 4 (Women)", "XTEP Running Shoes (Men)", "Skechers Track Ripkent Sneaker (Men)", 
    "WHITIN Running Shoes (Unisex)", "Nike Stellar Ride (Kids)", "Asics Gel-Excite 11 Sneaker (Men)", "New Balance Fresh Foam", 
    "Brooks Adrenaline Gts 25 (Men)", "Nike Vomero 18 GORE-TEX (Men)", "New Balance 411 Sneaker (Men)", "Under Armour Charged Edge (Men)", 
    "Nike Wildhorse 10 (Men)", "On Cloud 6 Sneaker (Men)", "HOKA Clifton 10 (Women)", "New Balance 1080"
]

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

# --- 4. STATE ---
if 'user_interest' not in st.session_state: st.session_state.user_interest = None
if 'cart_count' not in st.session_state: st.session_state.cart_count = 0

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
    st.info(f"Please add images to the folder.")
else:
    if st.session_state.user_interest is None:
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
                            st.session_state.user_interest = {"idx": idx, "path": all_images[idx], "name": PRODUCT_TITLES[idx], "price": PRODUCT_PRICES[idx], "rating": PRODUCT_RATINGS[idx]}
                            st.rerun()
    else:
        item = st.session_state.user_interest
        if st.button("⬅ Back to Collection"):
            st.session_state.user_interest = None
            st.rerun()
            
        col_l, col_r = st.columns([1.2, 1])
        with col_l:
            st.image(item['path'], use_container_width=True)
            # RESTORED: Small image thumbnails
            st.write("### Available Colors")
            sub1, sub2, spacer = st.columns([1, 1, 2])
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
                
        with col_r:
            st.header(item['name'])
            st.markdown(f'<p class="rating-text" style="font-size:24px;">{get_star_string(item["rating"])} ({item["rating"]})</p>', unsafe_allow_html=True)
            st.subheader(item['price'])
            
            # RESTORED: Color selection circles
            st.write("**Available Colors**")
            c_cols = st.columns([1, 1, 1, 7])
            for i, color in enumerate(["gray", "white", "black"]):
                c_cols[i].markdown(f'<div class="color-circle" style="background-color: {color};"></div>', unsafe_allow_html=True)

            st.write("**Select EU Size**")
            s_cols = st.columns(5)
            for i, s in enumerate(["42", "43", "44", "45", "46"]):
                s_cols[i].button(s, key=f"sz_{s}", use_container_width=True)
            
            st.divider()
            if st.button("ADD TO CART", key="main_add", use_container_width=True, type="primary"):
                st.session_state.cart_count += 1
                st.toast("Added!")
                st.rerun()
            st.button("BUY NOW", key="buy_now", use_container_width=True)