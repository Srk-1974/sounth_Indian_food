import streamlit as st

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="South Indian Food App 🍛",
    page_icon="🍛",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Poppins:wght@300;400;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }

.app-header {
    background: linear-gradient(135deg, #FF9933 0%, #FF6600 100%);
    padding: 24px 32px;
    border-radius: 16px;
    text-align: center;
    margin-bottom: 24px;
    box-shadow: 0 8px 32px rgba(255,102,0,0.3);
}
.app-header h1 {
    font-family: 'Great Vibes', cursive;
    font-size: 3.5rem;
    color: #800020;
    text-shadow: 2px 2px 0px #fff, 0 4px 15px rgba(0,0,0,0.15);
    margin: 0;
}
.app-header p { color: #fff; margin: 4px 0 0; font-size: 0.9rem; opacity: 0.9; }

.food-card {
    background: linear-gradient(135deg, #fff8f0, #fff3e0);
    border: 2px solid #FF9933;
    border-radius: 16px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 4px 16px rgba(255,153,51,0.15);
    margin-bottom: 8px;
}
.food-card h3 { color: #800020; font-size: 1.1rem; margin: 8px 0 4px; }
.food-card .price { color: #FF6600; font-weight: 700; font-size: 1.2rem; }
.food-emoji { font-size: 3.5rem; }

.cart-item {
    background: #fff8f0;
    border-left: 4px solid #FF9933;
    border-radius: 8px;
    padding: 10px 14px;
    margin-bottom: 10px;
}
.cart-total {
    background: linear-gradient(135deg, #FF9933, #FF6600);
    color: white;
    border-radius: 12px;
    padding: 14px;
    text-align: center;
    font-size: 1.2rem;
    font-weight: 700;
    margin-top: 12px;
}

.login-wrapper {
    max-width: 420px;
    margin: 60px auto;
    background: linear-gradient(145deg, #fff8f0, #fff3e0);
    border: 2px solid #FF9933;
    border-radius: 24px;
    padding: 40px 36px;
    box-shadow: 0 16px 48px rgba(255,153,51,0.25);
    text-align: center;
}
.login-wrapper h2 {
    color: #800020;
    font-family: 'Great Vibes', cursive;
    font-size: 2.4rem;
    margin-bottom: 4px;
}

.admin-badge {
    background: linear-gradient(135deg, #4CAF50, #2e7d32);
    color: white;
    border-radius: 8px;
    padding: 6px 14px;
    font-size: 0.85rem;
    font-weight: 600;
    display: inline-block;
}
.section-title {
    font-size: 1.4rem;
    font-weight: 700;
    color: #800020;
    border-bottom: 3px solid #FF9933;
    padding-bottom: 6px;
    margin-bottom: 18px;
}
</style>
""", unsafe_allow_html=True)

# ── Default menu data ────────────────────────────────────────────────────────
DEFAULT_MENU = [
    {"id": 1,  "name": "IDLY",       "price": 10, "category": "Breakfast",  "emoji": "🍚", "hot": True},
    {"id": 2,  "name": "DOSA",       "price": 20, "category": "Breakfast",  "emoji": "🥞", "hot": True},
    {"id": 3,  "name": "VADA",       "price": 30, "category": "Snacks",     "emoji": "🍩", "hot": True},
    {"id": 4,  "name": "POORI",      "price": 40, "category": "Breakfast",  "emoji": "🍘", "hot": True},
    {"id": 5,  "name": "Tea",        "price": 10, "category": "Beverages",  "emoji": "☕", "hot": True},
    {"id": 6,  "name": "Coffee",     "price": 15, "category": "Beverages",  "emoji": "☕", "hot": True},
    {"id": 7,  "name": "Sambar Rice","price": 60, "category": "Lunch",      "emoji": "🍛", "hot": True},
    {"id": 8,  "name": "Curd Rice",  "price": 50, "category": "Lunch",      "emoji": "🍚", "hot": False},
    {"id": 9,  "name": "Upma",       "price": 25, "category": "Breakfast",  "emoji": "🍲", "hot": True},
    {"id": 10, "name": "Pongal",     "price": 35, "category": "Breakfast",  "emoji": "🥣", "hot": True},
    {"id": 11, "name": "Rasam",      "price": 20, "category": "Lunch",      "emoji": "🍵", "hot": True},
    {"id": 12, "name": "Buttermilk", "price": 15, "category": "Beverages",  "emoji": "🥛", "hot": False},
]

# ── Session-state initialisation ─────────────────────────────────────────────
# NOTE: avoid using 'items' as a key — it shadows the dict.items() builtin
#       on Streamlit's AttrDict-style session_state object.
if "logged_in"       not in st.session_state: st.session_state["logged_in"]       = False
if "username"        not in st.session_state: st.session_state["username"]        = ""
if "menu_items"      not in st.session_state: st.session_state["menu_items"]      = list(DEFAULT_MENU)
if "cart"            not in st.session_state: st.session_state["cart"]            = {}
if "admin_unlocked"  not in st.session_state: st.session_state["admin_unlocked"]  = False
if "next_id"         not in st.session_state: st.session_state["next_id"]         = 13
if "currency_symbol" not in st.session_state: st.session_state["currency_symbol"] = "₹"

# ── Constants ────────────────────────────────────────────────────────────────
ADMIN_PASSWORD = "sriram123"
LOGIN_PASSWORD = "Admin123"
CATEGORIES     = ["All", "Breakfast", "Lunch", "Snacks", "Beverages"]

# ── Helper functions ──────────────────────────────────────────────────────────
def add_to_cart(item):
    iid = item["id"]
    if iid in st.session_state["cart"]:
        st.session_state["cart"][iid]["qty"] += 1
    else:
        st.session_state["cart"][iid] = {
            "name": item["name"],
            "price": item["price"],
            "qty": 1,
            "emoji": item["emoji"],
        }

def remove_from_cart(iid):
    if iid in st.session_state["cart"]:
        del st.session_state["cart"][iid]

def cart_total():
    return sum(v["price"] * v["qty"] for v in st.session_state["cart"].values())

def delete_menu_item(iid):
    st.session_state["menu_items"] = [
        i for i in st.session_state["menu_items"] if i["id"] != iid
    ]
    if iid in st.session_state["cart"]:
        del st.session_state["cart"][iid]

# ─────────────────────────────────────────────────────────────────────────────
#  LOGIN PAGE
# ─────────────────────────────────────────────────────────────────────────────
if not st.session_state["logged_in"]:
    st.markdown("""
    <div class="login-wrapper">
        <div style="font-size:5rem;">🍛</div>
        <h2>South Indian Food</h2>
        <p style="font-size:0.75rem;color:#999;margin-bottom:24px;">
            copyright © Bhadradri Technologies Inc.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("👤 Username", placeholder="Enter your name")
            password = st.text_input("🔒 Password", type="password", placeholder="Enter password")
            submit   = st.form_submit_button("🚀 Login", use_container_width=True)

        if submit:
            if username.strip() and password.strip() == LOGIN_PASSWORD:
                st.session_state["logged_in"] = True
                st.session_state["username"]  = username.strip()
                st.rerun()
            else:
                st.error("❌ Invalid credentials. Password must be **Admin123**")

        st.info("💡 Hint: password is **Admin123**")
    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
#  MAIN APP
# ─────────────────────────────────────────────────────────────────────────────

# Header
st.markdown(f"""
<div class="app-header">
    <h1>🍛 South Indian Food</h1>
    <p>Welcome, <strong>{st.session_state["username"]}</strong> &nbsp;|&nbsp;
       copyright © Bhadradri Technologies Inc.</p>
</div>
""", unsafe_allow_html=True)

_, col_logout = st.columns([5, 1])
with col_logout:
    if st.button("🚪 Logout", use_container_width=True):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

st.markdown("---")

# ── Sidebar – Cart + Admin ────────────────────────────────────────────────────
with st.sidebar:
    # ---- Cart ----
    st.markdown("## 🛒 Your Cart")
    cart = st.session_state["cart"]
    sym  = st.session_state["currency_symbol"]

    if not cart:
        st.info("Your cart is empty. Add items from the menu!")
    else:
        for iid, item in list(cart.items()):
            st.markdown(f"""
            <div class="cart-item">
                {item['emoji']} <strong>{item['name']}</strong> × {item['qty']}
                &nbsp;&nbsp;
                <span style="color:#FF6600;font-weight:700;">
                    {sym}{item['price'] * item['qty']}
                </span>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"❌ Remove {item['name']}", key=f"remove_{iid}"):
                remove_from_cart(iid)
                st.rerun()

        st.markdown(f"""
        <div class="cart-total">🧾 Total: {sym} {cart_total()}</div>
        """, unsafe_allow_html=True)
        st.markdown("")

        if st.button("✅ Checkout", use_container_width=True, type="primary"):
            st.balloons()
            st.success(f"🎉 Order placed! Total: {sym}{cart_total()}")
            st.session_state["cart"] = {}
            st.rerun()

    st.markdown("---")

    # ---- Admin ----
    st.markdown("### 🔐 Admin Panel")
    if not st.session_state["admin_unlocked"]:
        admin_pw = st.text_input("Admin Password", type="password", key="admin_pw_input")
        if st.button("🔓 Unlock Admin"):
            if admin_pw == ADMIN_PASSWORD:
                st.session_state["admin_unlocked"] = True
                st.success("✅ Admin access granted!")
                st.rerun()
            else:
                st.error("❌ Wrong password!")
    else:
        st.markdown('<span class="admin-badge">✅ Admin Mode Active</span>',
                    unsafe_allow_html=True)
        if st.button("🔒 Lock Admin"):
            st.session_state["admin_unlocked"] = False
            st.rerun()

        st.markdown("#### ➕ Add New Menu Item")
        with st.form("add_item_form"):
            new_name  = st.text_input("Item Name", placeholder="e.g. Masala Dosa")
            new_price = st.number_input("Price (₹)", min_value=1, value=30)
            new_cat   = st.selectbox("Category", ["Breakfast", "Lunch", "Snacks", "Beverages"])
            new_emoji = st.text_input("Emoji", value="🍛", max_chars=4)
            new_hot   = st.checkbox("🔥 Hot item (show steam)", value=True)
            add_sub   = st.form_submit_button("➕ Add Item", use_container_width=True)

        if add_sub and new_name.strip():
            st.session_state["menu_items"].append({
                "id":       st.session_state["next_id"],
                "name":     new_name.strip(),
                "price":    int(new_price),
                "category": new_cat,
                "emoji":    new_emoji or "🍛",
                "hot":      new_hot,
            })
            st.session_state["next_id"] += 1
            st.success(f"✅ **{new_name}** added!")
            st.rerun()

# ── Menu Section ──────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">🍽️ Our Menu</div>', unsafe_allow_html=True)

search_col, cat_col = st.columns([2, 2])
with search_col:
    search = st.text_input("🔍 Search dishes...", placeholder="e.g. Dosa, Tea…")
with cat_col:
    selected_cat = st.selectbox("📂 Category", CATEGORIES)

# Filter — read from "menu_items" key (NOT session_state.items)
menu_items = st.session_state["menu_items"]
filtered = [
    item for item in menu_items
    if (search.lower() in item["name"].lower() if search else True)
    and (selected_cat == "All" or item["category"] == selected_cat)
]

if not filtered:
    st.warning("No items match your search. Try a different keyword or category.")
else:
    num_cols = 4
    rows = [filtered[i:i + num_cols] for i in range(0, len(filtered), num_cols)]

    for row in rows:
        cols = st.columns(num_cols)
        for col, item in zip(cols, row):
            with col:
                hot_badge = "🔥 Hot & Fresh" if item.get("hot") else "❄️ Chilled"
                st.markdown(f"""
                <div class="food-card">
                    <div class="food-emoji">{item['emoji']}</div>
                    <h3>{item['name']}</h3>
                    <span style="font-size:0.75rem;background:#FF9933;color:white;
                          border-radius:10px;padding:2px 8px;">{item['category']}</span>
                    <p class="price">{sym} {item['price']}</p>
                    <p style="font-size:0.8rem;color:#999;">{hot_badge}</p>
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
<div style="text-align:center;color:#999;font-size:0.82rem;padding:12px 0;">
    🍛 South Indian Food App &nbsp;|&nbsp; copyright © Bhadradri Technologies Inc.
    &nbsp;|&nbsp; Built with ❤️ using Streamlit
</div>
""", unsafe_allow_html=True)
