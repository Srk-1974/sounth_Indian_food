import streamlit as st
import base64
from pathlib import Path

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="South Indian Food App 🍛",
    page_icon="🍛",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Helpers to load local images as base64 ────────────────────────────────────
ASSETS = Path("public/assets")

def img_b64(path: Path) -> str:
    """Return a base64 data-URI for a local image file."""
    if path.exists():
        ext = path.suffix.lstrip(".").lower()
        ext = "jpeg" if ext in ("jpg", "jpeg") else ext
        encoded = base64.b64encode(path.read_bytes()).decode()
        return f"data:image/{ext};base64,{encoded}"
    return ""

def img_tag(path: Path, style: str = "", alt: str = "") -> str:
    uri = img_b64(path)
    if uri:
        return f'<img src="{uri}" alt="{alt}" style="{style}">'
    return ""

# Pre-load key images
LOGO_B64       = img_b64(ASSETS / "logo.png")
CHEF_B64       = img_b64(ASSETS / "south-indian-chef.png")
SUNRISE_B64    = img_b64(ASSETS / "sunrise-icon.png")
LOGIN_FOOD_B64 = img_b64(ASSETS / "login-food.png")

FOOD_IMAGES = {
    "IDLY":        ASSETS / "idly.png",
    "DOSA":        ASSETS / "dosa.png",
    "DOSHA":       ASSETS / "dosa.png",
    "VADA":        ASSETS / "vada.png",
    "MASALA VADA": ASSETS / "masala-vada.png",
    "POORI":       ASSETS / "poori.png",
    "TEA":         ASSETS / "tea.png",
    "COFFEE":      ASSETS / "coffee.png",
    "UPMA":        ASSETS / "upma-sambar.jpg",
    "FALUDA":      ASSETS / "faluda.jpg",
    "MANGO JUICE": ASSETS / "mango-juice.jpg",
    "FRUIT CUSTARD": ASSETS / "fruit-custard.jpg",
    "PANI PURI":   ASSETS / "pani-puri.jpg",
    "VEG BIRYANI": ASSETS / "Veg_Biryani.jpeg",
}

def get_food_img_b64(name: str) -> str:
    key = name.upper()
    path = FOOD_IMAGES.get(key)
    if path and path.exists():
        return img_b64(path)
    # fallback: try stock images in order
    for stock in ["stock-1.png", "stock-2.png", "stock-3.png"]:
        p = ASSETS / stock
        if p.exists():
            return img_b64(p)
    return ""

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Poppins:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {{ font-family: 'Poppins', sans-serif; }}

/* ---- Top banner ---- */
.top-banner {{
    background: linear-gradient(90deg, #4B0082, #6A0DAD);
    color: white;
    text-align: center;
    padding: 8px;
    font-size: 0.88rem;
    border-radius: 8px;
    margin-bottom: 16px;
    letter-spacing: 0.5px;
}}

/* ---- Header ---- */
.app-header {{
    background: linear-gradient(135deg, #FF9933 0%, #FF7700 100%);
    padding: 16px 28px;
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20px;
    box-shadow: 0 6px 24px rgba(255,102,0,0.3);
}}
.header-title {{
    font-family: 'Great Vibes', cursive;
    font-size: 3.2rem;
    color: #800020;
    text-shadow: 2px 2px 0 #fff, 0 4px 15px rgba(0,0,0,0.15);
    margin: 0;
    display: flex;
    align-items: center;
    gap: 10px;
}}
.header-user {{
    color: white;
    font-size: 1rem;
    font-weight: 600;
    text-align: right;
}}

/* ---- Login ---- */
.login-page {{
    min-height: 90vh;
    background: linear-gradient(135deg, #FF9933 0%, #FFFFFF 50%, #138808 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 40px 0;
    border-radius: 16px;
}}
.login-card {{
    background: white;
    border-radius: 24px;
    padding: 40px 36px;
    width: 380px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.15);
    text-align: center;
}}
.login-card h2 {{
    color: #FF9933;
    font-weight: 700;
    font-size: 1.5rem;
    margin: 12px 0 4px;
}}
.login-card .copy {{
    color: #FF7700;
    font-size: 0.78rem;
    font-style: italic;
    font-weight: 600;
    margin-bottom: 20px;
}}
.login-card .sub {{
    color: #333;
    font-weight: 600;
    font-size: 0.95rem;
    margin-bottom: 16px;
}}

/* ---- Food cards ---- */
.food-card {{
    background: linear-gradient(145deg, #fff8f0, #fff3e0);
    border: 2px solid #FF9933;
    border-radius: 16px;
    padding: 0 0 14px 0;
    overflow: hidden;
    text-align: center;
    box-shadow: 0 4px 16px rgba(255,153,51,0.18);
    transition: transform 0.2s, box-shadow 0.2s;
    margin-bottom: 8px;
    height: 100%;
}}
.food-card:hover {{ transform: translateY(-4px); box-shadow: 0 8px 24px rgba(255,153,51,0.3); }}
.food-card img {{
    width: 100%;
    height: 160px;
    object-fit: cover;
    border-radius: 14px 14px 0 0;
}}
.food-card h3 {{ color: #800020; font-size: 1rem; margin: 10px 0 4px; font-weight: 700; }}
.food-card .price {{ color: #FF6600; font-weight: 700; font-size: 1.15rem; margin: 4px 0; }}
.cat-badge {{
    display: inline-block;
    background: #FF9933;
    color: white;
    font-size: 0.72rem;
    font-weight: 600;
    border-radius: 12px;
    padding: 2px 10px;
    margin-bottom: 4px;
}}

/* ---- Cart ---- */
.cart-item {{
    background: #fff8f0;
    border-left: 4px solid #FF9933;
    border-radius: 8px;
    padding: 10px 12px;
    margin-bottom: 10px;
    font-size: 0.9rem;
}}
.cart-total {{
    background: linear-gradient(135deg, #FF9933, #FF6600);
    color: white;
    border-radius: 12px;
    padding: 14px;
    text-align: center;
    font-size: 1.15rem;
    font-weight: 700;
    margin-top: 10px;
}}

/* ---- Section title ---- */
.section-title {{
    font-size: 1.4rem;
    font-weight: 700;
    color: #800020;
    border-bottom: 3px solid #FF9933;
    padding-bottom: 6px;
    margin-bottom: 18px;
}}
.admin-badge {{
    background: linear-gradient(135deg,#4CAF50,#2e7d32);
    color: white;
    border-radius: 8px;
    padding: 5px 12px;
    font-size: 0.82rem;
    font-weight: 600;
    display: inline-block;
    margin-bottom: 8px;
}}
</style>
""", unsafe_allow_html=True)

# ── Default menu ──────────────────────────────────────────────────────────────
DEFAULT_MENU = [
    {"id": 1,  "name": "IDLY",        "price": 10, "category": "Breakfast",  "hot": True},
    {"id": 2,  "name": "DOSA",        "price": 20, "category": "Breakfast",  "hot": True},
    {"id": 3,  "name": "VADA",        "price": 30, "category": "Snacks",     "hot": True},
    {"id": 4,  "name": "POORI",       "price": 40, "category": "Breakfast",  "hot": True},
    {"id": 5,  "name": "TEA",         "price": 10, "category": "Beverages",  "hot": True},
    {"id": 6,  "name": "COFFEE",      "price": 15, "category": "Beverages",  "hot": True},
    {"id": 7,  "name": "MASALA VADA", "price": 35, "category": "Snacks",     "hot": True},
    {"id": 8,  "name": "UPMA",        "price": 25, "category": "Breakfast",  "hot": True},
    {"id": 9,  "name": "FALUDA",      "price": 50, "category": "Beverages",  "hot": False},
    {"id": 10, "name": "MANGO JUICE", "price": 40, "category": "Beverages",  "hot": False},
    {"id": 11, "name": "VEG BIRYANI", "price": 80, "category": "Lunch",      "hot": True},
    {"id": 12, "name": "PANI PURI",   "price": 30, "category": "Snacks",     "hot": False},
]

# ── Session state ─────────────────────────────────────────────────────────────
if "logged_in"       not in st.session_state: st.session_state["logged_in"]       = False
if "username"        not in st.session_state: st.session_state["username"]        = ""
if "menu_items"      not in st.session_state: st.session_state["menu_items"]      = list(DEFAULT_MENU)
if "cart"            not in st.session_state: st.session_state["cart"]            = {}
if "admin_unlocked"  not in st.session_state: st.session_state["admin_unlocked"]  = False
if "next_id"         not in st.session_state: st.session_state["next_id"]         = 13

ADMIN_PASSWORD = "sriram123"
LOGIN_PASSWORD = "Admin123"
CATEGORIES     = ["All", "Breakfast", "Lunch", "Snacks", "Beverages"]
SYM            = "₹"

# ── Cart helpers ──────────────────────────────────────────────────────────────
def add_to_cart(item):
    iid = item["id"]
    if iid in st.session_state["cart"]:
        st.session_state["cart"][iid]["qty"] += 1
    else:
        st.session_state["cart"][iid] = {"name": item["name"], "price": item["price"], "qty": 1}

def remove_from_cart(iid):
    st.session_state["cart"].pop(iid, None)

def cart_total():
    return sum(v["price"] * v["qty"] for v in st.session_state["cart"].values())

def delete_menu_item(iid):
    st.session_state["menu_items"] = [i for i in st.session_state["menu_items"] if i["id"] != iid]
    st.session_state["cart"].pop(iid, None)

# ─────────────────────────────────────────────────────────────────────────────
# LOGIN PAGE
# ─────────────────────────────────────────────────────────────────────────────
if not st.session_state["logged_in"]:
    chef_tag = img_tag(
        ASSETS / "south-indian-chef.png",
        style="width:100px;height:100px;border-radius:50%;border:3px solid #FF9933;object-fit:cover;"
    )
    st.markdown(f"""
    <div class="login-page">
        <div class="login-card">
            {chef_tag if chef_tag else '<div style="font-size:5rem;">🍛</div>'}
            <h2>Welcome to South Indian Food App</h2>
            <p class="copy">copyright@Bhadradri Technologies.Inc</p>
            <p class="sub">Login to South Indian Food</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.1, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("👤 Username", placeholder="Username")
            password = st.text_input("🔒 Password", type="password", placeholder="Password")
            submit   = st.form_submit_button("Login", use_container_width=True)

        if submit:
            if username.strip() and password.strip() == LOGIN_PASSWORD:
                st.session_state["logged_in"] = True
                st.session_state["username"]  = username.strip()
                st.rerun()
            else:
                st.error("❌ Invalid credentials. Password: **Admin123**")

        st.caption("💡 Password: **Admin123**")
    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# MAIN APP
# ─────────────────────────────────────────────────────────────────────────────

# Top purple banner
st.markdown("""
<div class="top-banner">
    🌟 &nbsp; This project @ designed by Bhadradri Technologies.inc
</div>
""", unsafe_allow_html=True)

# Header bar
logo_tag    = img_tag(ASSETS / "login-food.png",
                      style="width:70px;height:70px;border-radius:50%;border:3px solid white;")
sunrise_tag = img_tag(ASSETS / "sunrise-icon.png",
                      style="width:48px;height:48px;vertical-align:middle;margin-left:8px;")

st.markdown(f"""
<div class="app-header">
    <div style="display:flex;align-items:center;gap:14px;">
        {logo_tag}
        <span class="header-title">South Indian Food {sunrise_tag}</span>
    </div>
    <div class="header-user">Hello, {st.session_state["username"]}</div>
</div>
""", unsafe_allow_html=True)

_, col_logout = st.columns([5, 1])
with col_logout:
    if st.button("🚪 Logout", use_container_width=True):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

st.markdown("---")

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🛒 Your Cart")
    cart = st.session_state["cart"]

    if not cart:
        st.info("Cart is empty — add items from the menu!")
    else:
        for iid, item in list(cart.items()):
            st.markdown(f"""
            <div class="cart-item">
                <strong>{item['name']}</strong> × {item['qty']}
                &nbsp;
                <span style="color:#FF6600;font-weight:700;float:right;">
                    {SYM}{item['price'] * item['qty']}
                </span>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"❌ Remove", key=f"remove_{iid}"):
                remove_from_cart(iid)
                st.rerun()

        st.markdown(f'<div class="cart-total">🧾 Total: {SYM} {cart_total()}</div>',
                    unsafe_allow_html=True)
        st.markdown("")
        if st.button("✅ Checkout", use_container_width=True, type="primary"):
            st.balloons()
            st.success(f"🎉 Order placed! Total: {SYM}{cart_total()}")
            st.session_state["cart"] = {}
            st.rerun()

    st.markdown("---")
    st.markdown("### 🔐 Admin Panel")

    if not st.session_state["admin_unlocked"]:
        admin_pw = st.text_input("Admin Password", type="password", key="admin_pw_input")
        if st.button("🔓 Unlock Admin"):
            if admin_pw == ADMIN_PASSWORD:
                st.session_state["admin_unlocked"] = True
                st.rerun()
            else:
                st.error("❌ Wrong password!")
    else:
        st.markdown('<span class="admin-badge">✅ Admin Mode Active</span>', unsafe_allow_html=True)
        if st.button("🔒 Lock Admin"):
            st.session_state["admin_unlocked"] = False
            st.rerun()

        st.markdown("#### ➕ Add New Menu Item")
        with st.form("add_item_form"):
            new_name  = st.text_input("Item Name", placeholder="e.g. Masala Dosa")
            new_price = st.number_input("Price (₹)", min_value=1, value=30)
            new_cat   = st.selectbox("Category", ["Breakfast", "Lunch", "Snacks", "Beverages"])
            new_hot   = st.checkbox("🔥 Hot item", value=True)
            add_sub   = st.form_submit_button("➕ Add Item", use_container_width=True)

        if add_sub and new_name.strip():
            st.session_state["menu_items"].append({
                "id": st.session_state["next_id"],
                "name": new_name.strip().upper(),
                "price": int(new_price),
                "category": new_cat,
                "hot": new_hot,
            })
            st.session_state["next_id"] += 1
            st.success(f"✅ **{new_name}** added!")
            st.rerun()

# ── Menu ──────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">🍽️ Our Menu</div>', unsafe_allow_html=True)

s_col, c_col = st.columns([2, 2])
with s_col:
    search = st.text_input("🔍 Search items...", placeholder="e.g. Dosa, Tea…")
with c_col:
    selected_cat = st.selectbox("📂 Category", CATEGORIES)

menu_items = st.session_state["menu_items"]
filtered = [
    it for it in menu_items
    if (search.upper() in it["name"] if search else True)
    and (selected_cat == "All" or it["category"] == selected_cat)
]

if not filtered:
    st.warning("No items found. Try a different search or category.")
else:
    NUM_COLS = 4
    for row_start in range(0, len(filtered), NUM_COLS):
        row  = filtered[row_start: row_start + NUM_COLS]
        cols = st.columns(NUM_COLS)
        for col, item in zip(cols, row):
            with col:
                img_b64_str = get_food_img_b64(item["name"])
                hot_label   = "🔥 Hot & Fresh" if item.get("hot") else "❄️ Chilled"

                if img_b64_str:
                    img_html = f'<img src="{img_b64_str}" alt="{item["name"]}" style="width:100%;height:160px;object-fit:cover;border-radius:14px 14px 0 0;">'
                else:
                    img_html = '<div style="width:100%;height:160px;background:#ffe0b2;display:flex;align-items:center;justify-content:center;font-size:3rem;border-radius:14px 14px 0 0;">🍛</div>'

                st.markdown(f"""
                <div class="food-card">
                    {img_html}
                    <h3>{item['name']}</h3>
                    <span class="cat-badge">{item['category']}</span>
                    <p class="price">{SYM} {item['price']}</p>
                    <p style="font-size:0.78rem;color:#999;margin:0;">{hot_label}</p>
                </div>
                """, unsafe_allow_html=True)

                if st.session_state["admin_unlocked"]:
                    b1, b2 = st.columns(2)
                    with b1:
                        if st.button("🛒 Add", key=f"add_{item['id']}", use_container_width=True):
                            add_to_cart(item)
                            st.rerun()
                    with b2:
                        if st.button("🗑️ Del", key=f"del_{item['id']}", use_container_width=True):
                            delete_menu_item(item["id"])
                            st.rerun()
                else:
                    if st.button("🛒 Add to Cart", key=f"add_{item['id']}", use_container_width=True):
                        add_to_cart(item)
                        st.rerun()

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center;color:#999;font-size:0.82rem;padding:10px 0;">
    🍛 South Indian Food App &nbsp;|&nbsp;
    copyright © Bhadradri Technologies Inc. &nbsp;|&nbsp;
    Built with ❤️ using Streamlit
</div>
""", unsafe_allow_html=True)
