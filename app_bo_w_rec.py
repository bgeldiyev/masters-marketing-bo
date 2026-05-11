import pandas as pd
import streamlit as st

import streamlit.components.v1 as components

import os
import base64

# =========================================================
# CONFIG
# =========================================================
st.set_page_config(page_title="Best Shop | Mixed Portfolio", layout="wide")

# =========================================================
# IMAGE BASE64 HELPER (FIX BROKEN DOCK IMAGES)
# =========================================================
def img_to_base64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return ""

# =========================================================
# CSS
# =========================================================
st.markdown("""
<style>

.block-container {
    padding-top: 3.5rem !important;
    padding-bottom: 320px !important;
}

.logo-container {
    display: flex;
    font-family: "Arial Black", Gadget, sans-serif;
    font-size: 42px;
    font-weight: 900;
}

.box-orange {
    background:#333;
    color:#f1c40f;
    padding:5px 15px;
}

.box-green {
    background:#f1c40f;
    color:#333;
    padding:5px 15px;
}

.category-bar {
    background:#333;
    padding:10px;
    display:flex;
    justify-content:center;
    gap:40px;
}

.cat-link {
    color:#F5F5DC;
    font-weight:bold;
}

.stImage > img {
    height:300px !important;
    object-fit:cover;
}

.detail-main-img img {
    max-height:300px !important;
}

.color-circle {
    height:22px;
    width:22px;
    border-radius:50%;
    display:inline-block;
}

.rec-card {
    min-width:200px;
    background:#f8f8f8;
    padding:12px;
    border-radius:12px;
    text-align:center;
}

.rec-img-wrap {
    display:flex;
    justify-content:center;
}

.rec-card img {
    width:160px;
    height:140px;
    object-fit:cover;
    border-radius:10px;
}

.rec-name {
    font-weight:700;
    font-size:13px;
}

.rec-rating {
    color:#f39c12;
    font-size:12px;
}

.rec-price {
    font-weight:800;
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
def get_star_string(r):
    return "★"*int(r) + "☆"*(5-int(r))

def get_images(folder):
    valid = ('.png','.jpg','.jpeg','.webp')
    if os.path.exists(folder):
        return sorted([os.path.join(folder,f) for f in os.listdir(folder) if f.lower().endswith(valid)])
    return []

# =========================================================
# STATE
# =========================================================
if 'user_interest' not in st.session_state:
    st.session_state.user_interest = None
if 'cart_count' not in st.session_state:
    st.session_state.cart_count = 0
if 'liked' not in st.session_state:
    st.session_state.liked = False
if 'viewed_history' not in st.session_state:
    st.session_state.viewed_history = False

all_images = get_images(IMAGE_FOLDER)

# =========================================================
# HEADER
# =========================================================
t1, t2, t3 = st.columns([2,2,1.2])

with t1:
    st.markdown('<div class="logo-container"><div class="box-orange">BEST</div><div class="box-green">SHOP</div></div>', unsafe_allow_html=True)

with t2:
    st.text_input("Search", placeholder="Search...", label_visibility="collapsed")

with t3:
    st.markdown(f"🛒 Cart ({st.session_state.cart_count})")

st.markdown("""
<div class="category-bar">
<span class="cat-link">Home</span>
<span class="cat-link">Categories</span>
<span class="cat-link">Brands</span>
</div>
""", unsafe_allow_html=True)

# =========================================================
# GRID VIEW
# =========================================================
if st.session_state.user_interest is None:

    for r in range(4):
        cols = st.columns(4)

        for c in range(4):
            idx = r*4 + c

            if idx < len(all_images):

                with cols[c]:
                    st.image(all_images[idx])
                    st.markdown(f"**{PRODUCT_TITLES[idx]}**")
                    st.markdown(f"{get_star_string(PRODUCT_RATINGS[idx])} ({PRODUCT_RATINGS[idx]})")
                    st.markdown(PRODUCT_PRICES[idx])

                    if st.button("View Product", key=f"btn_{idx}"):
                        st.session_state.user_interest = {
                            "idx": idx,
                            "path": all_images[idx],
                            "name": PRODUCT_TITLES[idx],
                            "price": PRODUCT_PRICES[idx],
                            "rating": PRODUCT_RATINGS[idx]
                        }
                        st.rerun()

# =========================================================
# PRODUCT PAGE
# =========================================================
else:

    item = st.session_state.user_interest

    if st.button("⬅ Back"):
        st.session_state.user_interest = None
        st.session_state.viewed_history = True
        st.rerun()

    c1, c2, c3, c4, c5 = st.columns([0.6,1,0.3,1,0.6])

    with c2:
        st.image(item['path'])

    with c4:

        st.header(item['name'])
        st.subheader(item['price'])

        st.write("Colors")
        cols = st.columns(3)
        for i,color in enumerate(["gray","white","black"]):
            cols[i].markdown(f"<div class='color-circle' style='background:{color};'></div>", unsafe_allow_html=True)

        st.write("Size")
        for s in ["42","43","44","45","46"]:
            st.button(s)

        b1,b2 = st.columns(2)
        if b1.button("ADD"):
            st.session_state.cart_count += 1
            st.toast("Added")

        b2.button("BUY")

# =========================================================
# SIMILAR SECTION (RESTORED AFTER BACK)
# =========================================================
if st.session_state.viewed_history and st.session_state.user_interest is None:

    st.markdown("## Similar Products")

    rel = [11,10,3,14]
    cols = st.columns(4)

    for i,idx in enumerate(rel):
        with cols[i]:
            st.image(all_images[idx])
            st.markdown(PRODUCT_TITLES[idx])
            st.markdown(f"{get_star_string(PRODUCT_RATINGS[idx])}")
            st.markdown(PRODUCT_PRICES[idx])

# =========================================================
# FLOATING DOCK (FIXED)
# =========================================================
rel_indices = [11,10,3,14]

cards = ""

for i in rel_indices:
    if i < len(all_images):
        img64 = img_to_base64(all_images[i])

        cards += f"""
        <div class="rec-card">
            <div class="rec-img-wrap">
                <img src="data:image/png;base64,{img64}">
            </div>
            <div class="rec-name">{PRODUCT_TITLES[i]}</div>
            <div class="rec-rating">{get_star_string(PRODUCT_RATINGS[i])}</div>
            <div class="rec-price">{PRODUCT_PRICES[i]}</div>
        </div>
        """

dock = f"""
<style>
#dock {{
    position:fixed;
    left:50%;
    transform:translateX(-50%);
    bottom:-350px;
    width:95%;
    background:white;
    padding:15px;
    border-radius:20px 20px 0 0;
    box-shadow:0 -5px 20px rgba(0,0,0,0.2);
    transition:bottom 0.8s ease;
    z-index:9999;
}}

#dock.show {{
    bottom:0;
}}

.scroll {{
    display:flex;
    gap:10px;
    overflow-x:auto;
}}
</style>

<div id="dock">
<h3>Because you viewed this</h3>

<div class="scroll">
{cards}
</div>
</div>

<script>
setTimeout(()=>{
document.getElementById("dock").classList.add("show");
},3000);
</script>
"""

components.html(dock, height=320)
