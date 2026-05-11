import pandas as pd
import streamlit as st

from datetime import datetime

import os
import base64

# --- 1. CONFIG ---
st.set_page_config(page_title="Best Shop | Mixed Portfolio", layout="wide")

# --- IMAGE BASE64 HELPER ---
def img_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# --- 2. CSS ---
st.markdown("""
<style>
.block-container { padding-top: 3.5rem !important; }

.logo-container {
    display: flex;
    font-family: "Arial Black";
    font-size: 42px;
    font-weight: 900;
}

.box-orange { background:#333; color:#f1c40f; padding:5px 15px; }
.box-green { background:#f1c40f; color:#333; padding:5px 15px; }

.category-bar {
    background:#333;
    padding:10px 0;
    display:flex;
    justify-content:center;
    gap:50px;
    margin-bottom:20px;
}

.cat-link { color:#F5F5DC; font-weight:bold; cursor:pointer; }

.stImage > img {
    width:100% !important;
    height:300px !important;
    object-fit:cover !important;
    border-radius:8px;
}

.detail-main-img img {
    max-height:300px !important;
    object-fit:contain !important;
}

.small-img img {
    height:60px !important;
}

.rating-text { color:#f39c12; font-weight:bold; }
.price-text { font-size:18px; font-weight:bold; }

.color-circle {
    height:22px;width:22px;border-radius:50%;
    display:inline-block;border:2px solid #ddd;
}

/* --- REC CONTAINER --- */
.rec-box {
    background:#f2f2f2;
    padding:20px;
    border-radius:12px;
    margin-top:20px;
}
</style>
""", unsafe_allow_html=True)

# --- 3. DATA ---
IMAGE_FOLDER = "./Pictures_New"
BACK_FOLDER = "./Pictures_Back"

PRODUCT_TITLES = [
    "Adidas Runfalcon 5 (Men)", "Reebok Energen Run 4 (Women)",
    "XTEP Running Shoes (Men)", "Skechers Track Ripkent Sneaker (Men)"
]

BACK_TITLES = [
    "Top Rated Choice", "Style Inspired", "Performance Pick",
    "Season's Best", "New Arrival"
]

PRODUCT_PRICES = ["$60", "$69", "$139", "$69"]
PRODUCT_RATINGS = [4.3, 4.7, 4.3, 4.5]

BACK_PRICES = ["$160", "$49", "$60", "$43", "$65"]
BACK_RATINGS = [4.7, 4.1, 4.3, 4.4, 4.4]

def star(r):
    return "★"*int(r) + "☆"*(5-int(r))

def get_images(folder):
    if os.path.exists(folder):
        return sorted([
            os.path.join(folder,f)
            for f in os.listdir(folder)
            if f.endswith((".jpg",".png",".jpeg"))
        ])
    return []

all_images = get_images(IMAGE_FOLDER)
back_images = get_images(BACK_FOLDER)

# --- 4. STATE ---
if "user_interest" not in st.session_state:
    st.session_state.user_interest = None

if "viewed_history" not in st.session_state:
    st.session_state.viewed_history = False

if "last_viewed_idx" not in st.session_state:
    st.session_state.last_viewed_idx = None

# --- 5. HEADER ---
t1,t2,t3 = st.columns([2,2,1])

with t1:
    st.markdown('<div class="logo-container"><div class="box-orange">BEST</div><div class="box-green">SHOP</div></div>', unsafe_allow_html=True)

with t2:
    st.text_input("Search", label_visibility="collapsed")

with t3:
    st.write("🛒 Cart")

st.markdown("""
<div class="category-bar">
<span class="cat-link">Home</span>
<span class="cat-link">Shop</span>
<span class="cat-link">Brands</span>
<span class="cat-link">Contact</span>
</div>
""", unsafe_allow_html=True)

# --- 6. GRID VIEW ---
if st.session_state.user_interest is None:

    for r in range(1):

        cols = st.columns(4)

        for i in range(4):

            idx = r*4 + i

            if idx < len(all_images):

                with cols[i]:

                    st.image(all_images[idx])
                    st.write(PRODUCT_TITLES[idx])

                    if st.button("View", key=idx):

                        st.session_state.user_interest = {
                            "idx": idx,
                            "path": all_images[idx],
                            "name": PRODUCT_TITLES[idx],
                            "price": PRODUCT_PRICES[idx],
                            "rating": PRODUCT_RATINGS[idx]
                        }

                        st.session_state.viewed_history = True
                        st.session_state.last_viewed_idx = idx

                        st.rerun()

    # --- SIMILAR SECTION (FIXED) ---
    if st.session_state.viewed_history:

        st.markdown("<div class='rec-box'>", unsafe_allow_html=True)

        st.subheader("Similar to what you viewed")

        cols = st.columns(5)

        for i in range(min(5,len(back_images))):

            with cols[i]:
                st.image(back_images[i])
                st.write(BACK_TITLES[i])
                st.write(star(BACK_RATINGS[i]))
                st.write(BACK_PRICES[i])

        st.markdown("</div>", unsafe_allow_html=True)

# --- 7. PRODUCT PAGE ---
else:

    item = st.session_state.user_interest

    if st.button("⬅ Back"):
        st.session_state.user_interest = None
        st.rerun()

    c1,c2 = st.columns([1,1])

    with c1:
        st.image(item["path"])

        st.write("### Editions")
        if len(all_images) > 2:
            st.image(all_images[:2])

    with c2:
        st.header(item["name"])
        st.write(star(item["rating"]))
        st.write(item["price"])

        st.write("Colors")
        for c in ["gray","black","white"]:
            st.markdown(f"<div class='color-circle' style='background:{c}'></div>", unsafe_allow_html=True)

        st.write("Sizes")
        st.button("42"); st.button("43"); st.button("44")

# --- 8. FLOATING DOCK ---
if st.session_state.user_interest is not None:

    rec_html = ""

    for i in range(min(4,len(all_images))):

        img = img_to_base64(all_images[i])

        rec_html += f"""
        <div style="min-width:200px;background:#fff;padding:10px;border-radius:10px;">
            <img src="data:image/jpeg;base64,{img}" style="width:100%;height:140px;object-fit:cover;">
            <b>{PRODUCT_TITLES[i]}</b><br>
            {star(PRODUCT_RATINGS[i])}<br>
            {PRODUCT_PRICES[i]}
        </div>
        """

    dock = f"""
    <style>
    #dock {{
        position:fixed;
        bottom:-400px;
        left:0;
        width:100%;
        height:45vh;
        background:white;
        z-index:999999;
        transition:0.7s;
        padding:20px;
        border-radius:20px 20px 0 0;
        box-shadow:0 -10px 30px rgba(0,0,0,0.2);
    }}
    #dock.show {{
        bottom:0;
    }}
    .dock-grid {{
        display:flex;
        gap:15px;
        overflow-x:auto;
    }}
    </style>

    <div id="dock">
        <h3>Because you viewed this</h3>
        <div class="dock-grid">
            {rec_html}
        </div>
    </div>

    <script>
    setTimeout(()=> {{
        document.getElementById("dock").classList.add("show");
    }}, 3000);
    </script>
    """

    st.markdown(dock, unsafe_allow_html=True)
