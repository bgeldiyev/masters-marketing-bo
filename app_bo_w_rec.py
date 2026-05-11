
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
# 2. CSS (RESTORED ESSENTIALS)
# =========================================================
st.markdown("""
<style>
.block-container { padding-top: 3.5rem !important; padding-bottom: 100px !important; }
.logo-container { display: flex; font-family: "Arial Black", sans-serif; font-size: 42px; font-weight: 900; letter-spacing: -2px; line-height: 1; }
.box-orange { background-color: #333333; color: #f1c40f; padding: 5px 15px; border: 2px solid #333333; display: flex; align-items: center; }
.box-green { background-color: #f1c40f; color: #333333; padding: 5px 15px; border: 2px solid #f1c40f; display: flex; align-items: center; }
.category-bar { background-color: #333333; padding: 10px 0px; display: flex; justify-content: center; gap: 50px; margin-top: 10px; margin-bottom: 20px; width: 100%; }
.cat-link { font-weight: bold; color: #F5F5DC; font-size: 16px; text-transform: uppercase; cursor: pointer; }

/* THE GRAY BOX (HOME PAGE) */
.rec-container { 
    background-color: #f2f2f2 !important; 
    border-radius: 12px; 
    padding: 20px !important; 
    margin-bottom: 20px !important;
}

.stImage > img { width: 100% !important; height: 300px !important; object-fit: cover !important; border-radius: 8px; border: 1px solid #eee; }
.detail-main-img img { max-height: 300px !important; width: auto !important; object-fit: contain !important; }
.rating-text { color: #f39c12; font-weight: bold; font-size: 14px; margin: 0; }
.price-text { font-size: 18px; font-weight: bold; color: #333; margin: 0; }
.color-circle { height: 22px; width: 22px; border-radius: 50%; display: inline-block; border: 2px solid #ddd; margin-right: 8px; }
</style>
""", unsafe_allow_html=True)

# =========================================================
# 3. DATA & HELPERS
# =========================================================
IMAGE_FOLDER, BACK_FOLDER = "./Pictures_New", "./Pictures_Back"
PRODUCT_TITLES = ["Adidas Runfalcon 5", "Reebok Energen Run 4", "XTEP Running Shoes", "Skechers Track Ripkent", "WHITIN Running", "Nike Stellar Ride", "Asics Gel-Excite 11", "New Balance Fresh Foam", "Brooks Adrenaline Gts 25", "Nike Vomero 18", "New Balance 411", "Under Armour Charged Edge", "Nike Wildhorse 10", "On Cloud 6", "HOKA Clifton 10", "New Balance 1080"]
BACK_TITLES = ["Top Rated", "Inspired", "Performance", "Season Best", "New Arrival"]
PRODUCT_PRICES = ["$60.00", "$69.99", "$139.99", "$69.95", "$49.99", "$59.99", "$90.00", "$139.99", "$160.00", "$169.99", "$49.99", "$65.00", "$149.99", "$138.85", "$129.99", "$159.99"]
PRODUCT_RATINGS = [4.3, 4.7, 4.3, 4.5, 4.3, 4.4, 4.5, 4.6, 4.7, 4.3, 4.1, 4.4, 4.4, 4.2, 4.6, 4.5]

def get_star_string(rating): return ("★" * int(rating)) + ("☆" * (5 - int(rating)))
def get_images(folder):
    valid = ('.png', '.jpg', '.jpeg', '.webp', '.avif')
    return sorted([os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(valid)]) if os.path.exists(folder) else []

all_images, back_images = get_images(IMAGE_FOLDER), get_images(BACK_FOLDER)

# =========================================================
# 4. STATE & SIDEBAR
# =========================================================
if 'user_interest' not in st.session_state: st.session_state.user_interest = None
if 'cart_count' not in st.session_state: st.session_state.cart_count = 0
if 'viewed_history' not in st.session_state: st.session_state.viewed_history = False

with st.sidebar:
    st.header("Refine Search")
    st.divider()
    st.checkbox("Running", value=True); st.checkbox("Training"); st.checkbox("Lifestyle")
    st.subheader("Price Range")
    st.slider("Filter", 0, 300, (40, 200))

# =========================================================
# 5. HEADER
# =========================================================
t1, t2, t3 = st.columns([2, 2, 1.2])
with t1: st.markdown('<div class="logo-container"><div class="box-orange">BEST</div><div class="box-green">SHOP</div></div>', unsafe_allow_html=True)
with t2: st.text_input("Search", placeholder="Search...", label_visibility="collapsed")
with t3: st.markdown(f"<p style='text-align:right; padding-top:20px; font-weight:bold;'>🛒 Cart ({st.session_state.cart_count})</p>", unsafe_allow_html=True)
st.markdown('<div class="category-bar"><span class="cat-link">Home</span><span class="cat-link">Categories</span><span class="cat-link">Brands</span></div>', unsafe_allow_html=True)

# =========================================================
# 6. MAIN ROUTING
# =========================================================
if st.session_state.user_interest is None:
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
                    st.markdown(f'<p class="rating-text">{get_star_string(PRODUCT_RATINGS[idx])}</p>', unsafe_allow_html=True)
                    if st.button("View Product", key=f"v_{idx}", use_container_width=True):
                        st.session_state.user_interest = {"idx": idx, "path": all_images[idx], "name": PRODUCT_TITLES[idx], "price": PRODUCT_PRICES[idx], "rating": PRODUCT_RATINGS[idx]}
                        st.session_state.viewed_history = True
                        st.rerun()
else:
    # PRODUCT DETAIL VIEW
    item = st.session_state.user_interest
    if st.button("⬅ Back"):
        st.session_state.user_interest = None
        st.rerun()
        
    c1, c2, gap, c3, c4 = st.columns([0.1, 1, 0.1, 1, 0.1])
    with c2:
        st.markdown('<div class="detail-main-img">', unsafe_allow_html=True)
        st.image(item['path'])
        st.markdown('</div>', unsafe_allow_html=True)
    with c3:
        st.header(item['name'])
        st.markdown(f'<p class="rating-text" style="font-size:18px;">{get_star_string(item["rating"])}</p>', unsafe_allow_html=True)
        st.subheader(item['price'])
        st.write("**Colors**")
        st.markdown('<div class="color-circle" style="background-color:gray;"></div><div class="color-circle" style="background-color:black;"></div>', unsafe_allow_html=True)
        if st.button("ADD TO CART", use_container_width=True, type="primary"):
            st.session_state.cart_count += 1
            st.toast("Added!")

    # =========================================================
    # 7. THE DOCK (AUTO-SHOWS AFTER 3 SECONDS)
    # =========================================================
    rel_indices = [11, 10, 3, 14]
    cards_html = ""
    for i in rel_indices:
        img64 = img_to_base64(all_images[i])
        cards_html += f"""
        <div style="min-width:160px; background:#f9f9f9; padding:10px; border-radius:10px; text-align:center; border:1px solid #ddd;">
            <img src="data:image/png;base64,{img64}" style="width:100%; height:100px; object-fit:cover; border-radius:5px;">
            <div style="font-size:12px; font-weight:bold; margin-top:5px;">{PRODUCT_TITLES[i]}</div>
            <div style="color:#f39c12; font-size:10px;">{get_star_string(PRODUCT_RATINGS[i])}</div>
            <div style="font-size:12px;">{PRODUCT_PRICES[i]}</div>
        </div>
        """

    dock_component = f"""
    <div id="dock-container" style="position:fixed; bottom:-300px; left:50%; transform:translateX(-50%); width:90%; background:white; padding:20px; border-radius:20px 20px 0 0; box-shadow:0 -10px 30px rgba(0,0,0,0.15); transition: bottom 0.8s ease; z-index:9999; font-family: sans-serif;">
        <h3 style="margin-top:0;">Because you viewed this...</h3>
        <div style="display:flex; gap:15px; overflow-x:auto; padding-bottom:10px;">
            {cards_html}
        </div>
    </div>
    <script>
        setTimeout(() => {{
            document.getElementById("dock-container").style.bottom = "0px";
        }}, 3000);
    </script>
    """
    components.html(dock_component, height=300)
