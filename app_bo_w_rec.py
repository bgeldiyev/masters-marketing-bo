import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from datetime import datetime
import os
import random
import base64

# =========================================================
# CONFIG
# =========================================================
st.set_page_config(
    page_title="Best Shop | Mixed Portfolio",
    layout="wide"
)

# =========================================================
# IMAGE BASE64 HELPER (FIX #1)
# =========================================================
def img_to_base64(img_path):
    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# =========================================================
# CSS
# =========================================================
st.markdown("""
<style>

.block-container {
    padding-top: 3.5rem !important;
}

.logo-container {
    display: flex;
    font-family: "Arial Black", Gadget, sans-serif;
    font-size: 42px;
    font-weight: 900;
    letter-spacing: -2px;
    line-height: 1;
}

.box-orange {
    background-color: #333333;
    color: #f1c40f;
    padding: 5px 15px;
    border: 2px solid #333333;
    display: flex;
    align-items: center;
}

.box-green {
    background-color: #f1c40f;
    color: #333333;
    padding: 5px 15px;
    border: 2px solid #f1c40f;
    display: flex;
    align-items: center;
}

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

.cat-link:hover {
    color: white;
}

.stImage > img {
    width: 100% !important;
    height: 300px !important;
    object-fit: cover !important;
    border-radius: 8px;
    border: 1px solid #eee;
}

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

.rating-text {
    color: #f39c12;
    font-weight: bold;
    font-size: 14px;
    margin: 0;
}

.price-text {
    font-size: 18px;
    font-weight: bold;
    color: #333;
    margin: 0;
}

.color-circle {
    height: 22px;
    width: 22px;
    border-radius: 50%;
    display: inline-block;
    border: 2px solid #ddd;
    margin-right: 8px;
}

.rec-container {
    background-color: #f2f2f2;
    border-radius: 12px;
    padding: 20px;
    margin-top: 15px;
}

button[kind="primary"] {
    background-color: #f1c40f !important;
    color: #333 !important;
    border: none !important;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# DATA
# =========================================================
IMAGE_FOLDER = "./Pictures_New"

PRODUCT_TITLES = [
    "Adidas Runfalcon 5 (Men)",
    "Reebok Energen Run 4 (Women)",
    "XTEP Running Shoes (Men)",
    "Skechers Track Ripkent Sneaker (Men)",
    "WHITIN Running Shoes (Unisex)",
    "Nike Stellar Ride (Kids)",
    "Asics Gel-Excite 11 Sneaker (Men)",
    "New Balance Fresh Foam",
    "Brooks Adrenaline Gts 25 (Men)",
    "Nike Vomero 18 GORE-TEX (Men)",
    "New Balance 411 Sneaker (Men)",
    "Under Armour Charged Edge (Men)",
    "Nike Wildhorse 10 (Men)",
    "On Cloud 6 Sneaker (Men)",
    "HOKA Clifton 10 (Women)",
    "New Balance 1080"
]

PRODUCT_PRICES = [
    "$60.00", "$69.99", "$139.99", "$69.95",
    "$49.99", "$59.99", "$90.00", "$139.99",
    "$160.00", "$169.99", "$49.99", "$65.00",
    "$149.99", "$138.85", "$129.99", "$159.99"
]

PRODUCT_RATINGS = [
    4.3, 4.7, 4.3, 4.5,
    4.3, 4.4, 4.5, 4.6,
    4.7, 4.3, 4.1, 4.4,
    4.4, 4.2, 4.6, 4.5
]

# =========================================================
# HELPERS
# =========================================================
def get_star_string(rating):
    return ("★" * int(rating)) + ("☆" * (5 - int(rating)))

def get_images(folder):
    valid = ('.png', '.jpg', '.jpeg', '.webp', '.avif')

    if os.path.exists(folder):
        return [
            os.path.join(folder, f)
            for f in os.listdir(folder)
            if f.lower().endswith(valid)
        ]
    return []

# =========================================================
# SESSION STATE (FIX #2)
# =========================================================
if "user_interest" not in st.session_state:
    st.session_state.user_interest = None

if "cart_count" not in st.session_state:
    st.session_state.cart_count = 0

if "liked" not in st.session_state:
    st.session_state.liked = False

if "show_similar" not in st.session_state:
    st.session_state.show_similar = False

# =========================================================
# LOAD
# =========================================================
all_images = get_images(IMAGE_FOLDER)

# =========================================================
# HEADER (unchanged)
# =========================================================
t1, t2, t3 = st.columns([2, 2, 1.2])

with t1:
    st.markdown("""
    <div class="logo-container">
        <div class="box-orange">BEST</div>
        <div class="box-green">SHOP</div>
    </div>
    """, unsafe_allow_html=True)

with t2:
    st.text_input("Search", placeholder="Search brand or style...", label_visibility="collapsed")

with t3:
    st.markdown(f"<p style='text-align:right;padding-top:20px;font-weight:bold;'>🛒 Cart ({st.session_state.cart_count})</p>", unsafe_allow_html=True)

st.markdown("""
<div class="category-bar">
    <span class="cat-link">Home</span>
    <span class="cat-link">Categories</span>
    <span class="cat-link">New Arrivals</span>
    <span class="cat-link">Brands</span>
    <span class="cat-link">Checkout</span>
    <span class="cat-link">Contact</span>
</div>
""", unsafe_allow_html=True)

# =========================================================
# MAIN
# =========================================================
if not all_images:
    st.info("Add images first.")
else:

    # ================= GRID =================
    if st.session_state.user_interest is None:

        # FIX #2: SHOW SIMILAR AFTER BACK
        if st.session_state.show_similar:

            st.markdown("""
            <div class="rec-container">
                <h3>Similar to what you just viewed</h3>
            </div>
            """, unsafe_allow_html=True)

            rel_indices = [11, 10, 3, 14]
            cols = st.columns(4)

            for i, r_idx in enumerate(rel_indices):
                if r_idx < len(all_images):
                    with cols[i]:
                        st.image(all_images[r_idx])
                        st.markdown(f"**{PRODUCT_TITLES[r_idx]}**")
                        st.markdown(f"<p class='rating-text'>{get_star_string(PRODUCT_RATINGS[r_idx])}</p>", unsafe_allow_html=True)
                        st.markdown(f"<p class='price-text'>{PRODUCT_PRICES[r_idx]}</p>", unsafe_allow_html=True)

            st.session_state.show_similar = False

        for r in range(4):
            cols = st.columns(4)

            for c in range(4):
                idx = r * 4 + c

                if idx < len(all_images):

                    with cols[c]:
                        st.image(all_images[idx])
                        st.markdown(f"**{PRODUCT_TITLES[idx]}**")
                        st.markdown(f"<p class='rating-text'>{get_star_string(PRODUCT_RATINGS[idx])}</p>", unsafe_allow_html=True)
                        st.markdown(f"<p class='price-text'>{PRODUCT_PRICES[idx]}</p>", unsafe_allow_html=True)

                        if st.button("View Product", key=f"btn_{idx}"):

                            st.session_state.user_interest = {
                                "idx": idx,
                                "path": all_images[idx],
                                "name": PRODUCT_TITLES[idx],
                                "price": PRODUCT_PRICES[idx],
                                "rating": PRODUCT_RATINGS[idx]
                            }
                            st.rerun()

    # ================= DETAIL =================
    else:

        item = st.session_state.user_interest

        if st.button("⬅ Back to Collection"):
            st.session_state.user_interest = None
            st.session_state.show_similar = True
            st.rerun()

        c_left, c_img, c_gap, c_buy, c_right = st.columns([0.6,1,0.3,1,0.6])

        with c_img:
            st.image(item["path"])

        with c_buy:
            st.header(item["name"])

            st.subheader(item["price"])

        # ================= DOCK (FIX #1) =================
        rel_indices = [11, 10, 3, 14]

        cards = ""

        for r_idx in rel_indices:
            if r_idx < len(all_images):

                img_b64 = img_to_base64(all_images[r_idx])

                cards += f"""
                <div class="rec-card">
                    <img src="data:image/jpeg;base64,{img_b64}">
                    <div>{PRODUCT_TITLES[r_idx]}</div>
                </div>
                """

        dock = f"""
        <style>
        #dock {{
            position:fixed;
            bottom:-400px;
            left:50%;
            transform:translateX(-50%);
            width:95%;
            background:white;
            border-radius:20px 20px 0 0;
            transition:0.8s;
            padding:20px;
            z-index:99999;
        }}

        #dock.show {{
            bottom:0;
        }}

        .rec-card img {{
            width:100%;
            height:160px;
            object-fit:cover;
        }}
        </style>

        <div id="dock">
            {cards}
        </div>

        <script>
        setTimeout(() => {{
            document.getElementById("dock").classList.add("show");
        }}, 3000);
        </script>
        """

        components.html(dock, height=350)
