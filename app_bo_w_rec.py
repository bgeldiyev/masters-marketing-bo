import pandas as pd
import streamlit as st

from datetime import datetime

import os
import random

# --- 1. CONFIG ---
st.set_page_config(
    page_title="Best Shop | Mixed Portfolio",
    layout="wide"
)

# --- 2. CSS ---
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

/* GRID IMAGES */
.stImage > img {
    width: 100% !important;
    height: 300px !important;
    object-fit: cover !important;
    border-radius: 8px;
    border: 1px solid #eee;
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

# --- 3. DATA ---
IMAGE_FOLDER = "./Pictures_New"
BACK_FOLDER = "./Pictures_Back"

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

BACK_TITLES = [
    "Top Rated Choice",
    "Style Inspired by You",
    "Performance Pick",
    "Season's Best",
    "New Arrival"
]

BACK_PRICES = [
    "$160.00",
    "$49.99",
    "$60.00",
    "$43.99",
    "$65.00"
]

BACK_RATINGS = [
    4.7,
    4.1,
    4.3,
    4.4,
    4.4
]

# --- 4. HELPERS ---
def get_star_string(rating):
    return ("★" * int(rating)) + ("☆" * (5 - int(rating)))

def get_images(folder):
    valid = ('.png', '.jpg', '.jpeg', '.webp', '.avif')

    if os.path.exists(folder):
        files = [
            os.path.join(folder, f)
            for f in os.listdir(folder)
            if f.lower().endswith(valid)
        ]

        return sorted(files)

    return []

# --- 5. STATE ---
if 'user_interest' not in st.session_state:
    st.session_state.user_interest = None

if 'cart_count' not in st.session_state:
    st.session_state.cart_count = 0

if 'liked' not in st.session_state:
    st.session_state.liked = False

if 'viewed_history' not in st.session_state:
    st.session_state.viewed_history = False

# --- 6. LOAD IMAGES ---
all_images = get_images(IMAGE_FOLDER)
back_images = get_images(BACK_FOLDER)

# --- 7. SIDEBAR ---
if st.session_state.user_interest is None:

    with st.sidebar:

        st.header("Refine Search")
        st.divider()

        st.subheader("Category")

        st.checkbox("Running", value=True)
        st.checkbox("Training")
        st.checkbox("Lifestyle")

        st.subheader("Price Range")

        st.slider(
            "Filter by Price",
            0,
            300,
            (40, 200)
        )

        if st.button(
            "Reset All Filters",
            use_container_width=True
        ):
            st.rerun()

# --- 8. HEADER ---
t1, t2, t3 = st.columns([2, 2, 1.2])

with t1:
    st.markdown(
        '''
        <div class="logo-container">
            <div class="box-orange">BEST</div>
            <div class="box-green">SHOP</div>
        </div>
        ''',
        unsafe_allow_html=True
    )

with t2:
    st.text_input(
        "Search",
        placeholder="Search brand or style...",
        label_visibility="collapsed"
    )

with t3:
    st.markdown(
        f"""
        <p style='text-align:right;
        padding-top:20px;
        font-size:14px;
        font-weight:bold;'>
        🛒 Cart ({st.session_state.cart_count})
        </p>
        """,
        unsafe_allow_html=True
    )

st.markdown(
    '''
    <div class="category-bar">
        <span class="cat-link">Home</span>
        <span class="cat-link">Categories</span>
        <span class="cat-link">New Arrivals</span>
        <span class="cat-link">Brands</span>
        <span class="cat-link">Checkout</span>
        <span class="cat-link">Contact</span>
    </div>
    ''',
    unsafe_allow_html=True
)

# --- 9. MAIN CONTENT ---
if not all_images:

    st.info("Please add images to the folder.")

else:

    # =========================================================
    # GRID VIEW
    # =========================================================
    if st.session_state.user_interest is None:

        for r in range(4):

            if r == 1 and st.session_state.viewed_history:

                with st.container():

                    st.markdown(
                        '<div class="rec-container">',
                        unsafe_allow_html=True
                    )

                    st.subheader("Similar to what you just viewed")

                    rel_cols = st.columns(5)

                    for i in range(5):

                        with rel_cols[i]:

                            if i < len(back_images):

                                st.image(back_images[i])

                                st.markdown(
                                    f"**{BACK_TITLES[i]}**"
                                )

                                st.markdown(
                                    f'''
                                    <p class="rating-text">
                                    {get_star_string(BACK_RATINGS[i])}
                                    ({BACK_RATINGS[i]})
                                    </p>
                                    ''',
                                    unsafe_allow_html=True
                                )

                                st.markdown(
                                    f'''
                                    <p class="price-text">
                                    {BACK_PRICES[i]}
                                    </p>
                                    ''',
                                    unsafe_allow_html=True
                                )

                    st.markdown(
                        '</div>',
                        unsafe_allow_html=True
                    )

            cols = st.columns(4)

            for c in range(4):

                idx = r * 4 + c

                if idx < len(all_images):

                    with cols[c]:

                        st.image(all_images[idx])

                        st.markdown(
                            f"**{PRODUCT_TITLES[idx]}**"
                        )

                        st.markdown(
                            f'''
                            <p class="rating-text">
                            {get_star_string(PRODUCT_RATINGS[idx])}
                            ({PRODUCT_RATINGS[idx]})
                            </p>
                            ''',
                            unsafe_allow_html=True
                        )

                        st.markdown(
                            f'''
                            <p class="price-text">
                            {PRODUCT_PRICES[idx]}
                            </p>
                            ''',
                            unsafe_allow_html=True
                        )

                        if st.button(
                            "View Product",
                            key=f"btn_{idx}",
                            use_container_width=True
                        ):

                            if idx == 1:
                                st.session_state.viewed_history = True

                            st.session_state.user_interest = {
                                "idx": idx,
                                "path": all_images[idx],
                                "name": PRODUCT_TITLES[idx],
                                "price": PRODUCT_PRICES[idx],
                                "rating": PRODUCT_RATINGS[idx]
                            }

                            st.rerun()

    # =========================================================
    # PRODUCT DETAIL PAGE
    # =========================================================
    else:

        item = st.session_state.user_interest

        if st.button("⬅ Back to Collection"):

            st.session_state.user_interest = None
            st.rerun()

        c_left, c_img, c_gap, c_buy, c_right = st.columns(
            [0.6, 1, 0.3, 1, 0.6]
        )

        # ---------------- IMAGE COLUMN ----------------
        with c_img:

            st.markdown(
                '<div class="detail-main-img">',
                unsafe_allow_html=True
            )

            st.image(item['path'])

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )

            st.write("### Editions")

            sub1, sub2, _ = st.columns([1, 1, 1.5])

            if len(all_images) >= 17:

                with sub1:

                    st.markdown(
                        '<div class="small-img">',
                        unsafe_allow_html=True
                    )

                    st.image(all_images[16])

                    st.markdown(
                        '</div>',
                        unsafe_allow_html=True
                    )

            if len(all_images) >= 18:

                with sub2:

                    st.markdown(
                        '<div class="small-img">',
                        unsafe_allow_html=True
                    )

                    st.image(all_images[17])

                    st.markdown(
                        '</div>',
                        unsafe_allow_html=True
                    )

        # ---------------- BUY COLUMN ----------------
        with c_buy:

            title_col, heart_col = st.columns([5, 1])

            title_col.header(item['name'])

            if heart_col.button(
                "❤️" if st.session_state.liked else "🤍",
                key="heart_btn"
            ):

                st.session_state.liked = (
                    not st.session_state.liked
                )

                st.rerun()

            st.markdown(
                f'''
                <p class="rating-text"
                style="font-size:18px;">
                {get_star_string(item["rating"])}
                ({item["rating"]})
                </p>
                ''',
                unsafe_allow_html=True
            )

            st.subheader(item['price'])

            st.write("**Colors**")

            c_cols = st.columns([1, 1, 1, 6])

            for i, color in enumerate(
                ["gray", "white", "black"]
            ):

                c_cols[i].markdown(
                    f'''
                    <div class="color-circle"
                    style="background-color:{color};">
                    </div>
                    ''',
                    unsafe_allow_html=True
                )

            st.write("**Size**")

            s_cols = st.columns(5)

            for s in ["42", "43", "44", "45", "46"]:

                s_cols[int(s)-42].button(
                    s,
                    key=f"sz_{s}",
                    use_container_width=True
                )

            st.divider()

            b1, b2 = st.columns(2)

            if b1.button(
                "ADD",
                key="main_add",
                use_container_width=True,
                type="primary"
            ):

                st.session_state.cart_count += 1
                st.toast("Added!")

            b2.button(
                "BUY",
                key="buy_now",
                use_container_width=True
            )

        # =========================================================
        # FLOATING RECOMMENDATION DOCK
        # =========================================================
        rel_indices = [11, 10, 3, 14]

        recommend_cards = ""

        for r_idx in rel_indices:

            if r_idx < len(all_images):

                recommend_cards += f"""
                <div class="rec-card">

                    <img src="file/{all_images[r_idx]}">

                    <div class="rec-name">
                        {PRODUCT_TITLES[r_idx]}
                    </div>

                    <div class="rec-rating">
                        {get_star_string(PRODUCT_RATINGS[r_idx])}
                        ({PRODUCT_RATINGS[r_idx]})
                    </div>

                    <div class="rec-price">
                        {PRODUCT_PRICES[r_idx]}
                    </div>

                </div>
                """

        dock_html = f"""
        <style>

        #recommend-dock {{

            position: fixed;

            left: 50%;
            transform: translateX(-50%);

            bottom: -450px;

            width: 94%;
            max-width: 1400px;

            background: white;

            border-radius: 22px 22px 0px 0px;

            box-shadow:
                0px -8px 35px rgba(0,0,0,0.18);

            padding: 22px;

            z-index: 99999;

            transition:
                bottom 0.9s cubic-bezier(0.22,1,0.36,1);

            border: 1px solid #eaeaea;
        }}

        #recommend-dock.show {{
            bottom: 0px;
        }}

        .rec-header {{

            display: flex;
            justify-content: space-between;
            align-items: center;

            margin-bottom: 18px;
        }}

        .rec-title {{

            font-size: 22px;
            font-weight: 800;
            color: #222;
        }}

        .rec-close {{

            cursor: pointer;
            font-size: 24px;
            font-weight: bold;
            color: #777;
        }}

        .rec-close:hover {{
            color: black;
        }}

        .rec-grid {{

            display: flex;
            gap: 18px;

            overflow-x: auto;

            padding-bottom: 5px;
        }}

        .rec-card {{

            min-width: 210px;

            background: #fafafa;

            border-radius: 16px;

            padding: 12px;

            border: 1px solid #ececec;

            transition:
                transform 0.25s ease,
                box-shadow 0.25s ease;
        }}

        .rec-card:hover {{

            transform: translateY(-5px);

            box-shadow:
                0px 8px 20px rgba(0,0,0,0.10);
        }}

        .rec-card img {{

            width: 100%;
            height: 170px;

            object-fit: cover;

            border-radius: 12px;

            margin-bottom: 10px;
        }}

        .rec-name {{

            font-weight: 700;
            font-size: 14px;

            color: #222;

            min-height: 42px;
        }}

        .rec-rating {{

            color: #f39c12;

            font-size: 13px;

            margin-top: 5px;
        }}

        .rec-price {{

            font-size: 16px;
            font-weight: 800;

            color: #111;

            margin-top: 6px;
        }}

        </style>

        <div id="recommend-dock">

            <div class="rec-header">

                <div class="rec-title">
                    Because you viewed this,
                    you may also like
                </div>

                <div class="rec-close"
                    onclick="
                    document.getElementById(
                    'recommend-dock'
                    ).style.display='none';
                    ">
                    ✕
                </div>

            </div>

            <div class="rec-grid">

                {recommend_cards}

            </div>

        </div>

        <script>

        setTimeout(() => {{

            const dock =
                document.getElementById(
                    "recommend-dock"
                );

            if (dock) {{
                dock.classList.add("show");
            }}

        }}, 3000);

        </script>
        """

        st.markdown(
            dock_html,
            unsafe_allow_html=True
        )
