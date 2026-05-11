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
# IMAGE BASE64
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
    padding-bottom: 150px !important;
}

.logo-container {
    display: flex;
    font-family: "Arial Black", sans-serif;
    font-size: 42px;
    font-weight: 900;
}

.box-orange {
    background: #333;
    color: #f1c40f;
    padding: 5px 15px;
}

.box-green {
    background: #f1c40f;
    color: #333;
    padding: 5px 15px;
}

.category-bar {
    background: #333;
    padding: 10px;
    display: flex;
    justify-content: center;
    gap: 50px;
    width: 100%;
}

.cat-link {
    color: #F5F5DC;
    font-weight: bold;
}

.stImage > img {
    width: 100% !important;
    height: 300px !important;
    object-fit: cover;
    border-radius: 8px;
}

.detail-main-img img {
    max-height: 300px;
    display: block;
    margin: auto;
}

.rating-text {
    color: #f39c12;
    font-weight: bold;
}

.price-text {
    font-weight: bold;
}

.color-circle {
    width: 22px;
    height: 22px;
    border-radius: 50%;
    display: inline-block;
    margin-right: 6px;
    border: 1px solid #ccc;
}

/* FIXED SIMILAR BOX */
.similar-box {
    background: #f2f2f2;
    padding: 25px;
    border-radius: 14px;
    margin: 20px 0;
}

.similar-title {
    font-size: 18px;
    font-weight: 800;
    margin-bottom: 15px;
}

.similar-row {
    display: flex;
    gap: 15px;
    overflow-x: auto;
}

.sim-card {
    min-width: 180px;
    background: white;
    padding: 12px;
    border-radius: 12px;
    text-align: center;
    border: 1px solid #ddd;
}

.sim-card img {
    width: 100%;
    height: 120px;
    object-fit: cover;
    border-radius: 8px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# DATA
# =========================================================
IMAGE_FOLDER = "./Pictures_New"

PRODUCT_TITLES = [
    "Adidas Runfalcon 5 (Men)", "Reebok Energen Run 4 (Women)",
    "XTEP Running Shoes (Men)", "Skechers Track Ripkent Sneaker (Men)",
    "WHITIN Running Shoes (Unisex)", "Nike Stellar Ride (Kids)",
    "Asics Gel-Excite 11 Sneaker (Men)", "New Balance Fresh Foam",
    "Brooks Adrenaline Gts 25 (Men)", "Nike Vomero 18",
    "New Balance 411", "Under Armour Charged Edge",
    "Nike Wildhorse 10", "On Cloud 6",
    "HOKA Clifton 10", "New Balance 1080"
]

PRODUCT_PRICES = ["$60.00", "$69.99", "$139.99", "$69.95",
                  "$49.99", "$59.99", "$90.00", "$139.99",
                  "$160.00", "$169.99", "$49.99", "$65.00",
                  "$149.99", "$138.85", "$129.99", "$159.99"]

PRODUCT_RATINGS = [4.3,4.7,4.3,4.5,4.3,4.4,4.5,4.6,
                   4.7,4.3,4.1,4.4,4.4,4.2,4.6,4.5]

def stars(r):
    return "★"*int(r) + "☆"*(5-int(r))

def get_images(folder):
    if not os.path.exists(folder):
        return []
    return sorted([os.path.join(folder,f) for f in os.listdir(folder) if f.endswith(("jpg","png","jpeg"))])

all_images = get_images(IMAGE_FOLDER)

# =========================================================
# SESSION
# =========================================================
if "user_interest" not in st.session_state:
    st.session_state.user_interest = None

if "viewed_history" not in st.session_state:
    st.session_state.viewed_history = False

# =========================================================
# GRID
# =========================================================
if st.session_state.user_interest is None:

    for r in range(4):

        # =========================
        # FIXED SIMILAR SECTION
        # =========================
        if r == 1 and st.session_state.viewed_history:

            rel_html = ""

            for i in [11,10,3,14]:

                if i < len(all_images):

                    img64 = img_to_base64(all_images[i])

                    rel_html += f"""
                    <div class="sim-card">
                        <img src="data:image/png;base64,{img64}">
                        <div><b>{PRODUCT_TITLES[i]}</b></div>
                        <div style="color:#f39c12">{stars(PRODUCT_RATINGS[i])}</div>
                        <div>{PRODUCT_PRICES[i]}</div>
                    </div>
                    """

            st.markdown(f"""
            <div class="similar-box">

                <div class="similar-title">
                    Similar to what you just viewed
                </div>

                <div class="similar-row">
                    {rel_html}
                </div>

            </div>
            """, unsafe_allow_html=True)

        cols = st.columns(4)

        for c in range(4):

            idx = r*4 + c

            if idx < len(all_images):

                with cols[c]:

                    st.image(all_images[idx])
                    st.write(PRODUCT_TITLES[idx])
                    st.write(stars(PRODUCT_RATINGS[idx]))
                    st.write(PRODUCT_PRICES[idx])

                    if st.button("View Product", key=f"v{idx}"):

                        st.session_state.user_interest = {
                            "idx": idx,
                            "img": all_images[idx],
                            "name": PRODUCT_TITLES[idx],
                            "price": PRODUCT_PRICES[idx],
                            "rating": PRODUCT_RATINGS[idx]
                        }

                        if idx == 1:
                            st.session_state.viewed_history = True

                        st.rerun()

# =========================================================
# PRODUCT PAGE
# =========================================================
else:

    item = st.session_state.user_interest

    if st.button("⬅ Back"):
        st.session_state.user_interest = None
        st.rerun()

    c1,c2,c3 = st.columns([1,2,1])

    with c2:
        st.markdown('<div class="detail-main-img">', unsafe_allow_html=True)
        st.image(item["img"])
        st.markdown("</div>", unsafe_allow_html=True)

    st.header(item["name"])
    st.write(stars(item["rating"]))
    st.subheader(item["price"])

    st.write("Colors")
    st.markdown("⚫ ⚪ 🔘", unsafe_allow_html=True)

    st.write("Size")
    st.write("42 43 44 45 46")

    st.button("ADD TO CART")
    st.button("BUY NOW")

    # =====================================================
    # FLOATING DOCK (UNCHANGED LOGIC)
    # =====================================================
    rel = [11,10,3,14]

    cards = ""

    for i in rel:

        if i < len(all_images):

            img64 = img_to_base64(all_images[i])

            cards += f"""
            <div class="sim-card">
                <img src="data:image/png;base64,{img64}">
                <div><b>{PRODUCT_TITLES[i]}</b></div>
                <div>{stars(PRODUCT_RATINGS[i])}</div>
                <div>{PRODUCT_PRICES[i]}</div>
            </div>
            """

    dock = f"""
    <div id="dock" style="
        position:fixed;
        bottom:-400px;
        left:50%;
        transform:translateX(-50%);
        width:95%;
        background:white;
        padding:20px;
        border-radius:20px 20px 0 0;
        box-shadow:0 -10px 40px rgba(0,0,0,0.2);
        transition:0.8s;
        z-index:9999;
    ">

        <h3>Because you viewed this</h3>

        <div style="display:flex; gap:15px; overflow-x:auto;">
            {cards}
        </div>

    </div>

    <script>
        setTimeout(function(){{
            document.getElementById("dock").style.bottom = "0px";
        }}, 3000);
    </script>
    """

    components.html(dock, height=350)
