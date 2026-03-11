import streamlit as st
import base64
from pathlib import Path
from datetime import datetime

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="South Indian Food App 🍛",
    page_icon="🍛",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Image loader ──────────────────────────────────────────────────────────────
ASSETS = Path("public/assets")

def img_b64(path: Path) -> str:
    if path.exists():
        ext = path.suffix.lstrip(".").lower()
        ext = "jpeg" if ext in ("jpg", "jpeg") else ext
        encoded = base64.b64encode(path.read_bytes()).decode()
        return f"data:image/{ext};base64,{encoded}"
    return ""

# Pre-load required assets
BHADRADRI_B64  = img_b64(ASSETS / "bhadradri-icon-small.png")
LOGIN_FOOD_B64 = img_b64(ASSETS / "login-food.png")
CHEF_B64       = img_b64(ASSETS / "south-indian-chef.png")
SUNRISE_B64    = img_b64(ASSETS / "sunrise-icon.png")
CHATBOT_ICON_B64 = img_b64(ASSETS / "chatbot-icon.png")

# Food image mapping
FOOD_IMAGES = {
    "IDLY":          ASSETS / "idly.png",
    "DOSA":          ASSETS / "dosa.png",
    "DOSHA":         ASSETS / "dosa.png",
    "VADA":          ASSETS / "vada.png",
    "MASALA VADA":   ASSETS / "masala-vada.png",
    "POORI":         ASSETS / "poori.png",
    "TEA":           ASSETS / "tea.png",
    "COFFEE":        ASSETS / "coffee.png",
    "UPMA":          ASSETS / "upma-sambar.jpg",
    "FALUDA":        ASSETS / "faluda.jpg",
    "MANGO JUICE":   ASSETS / "mango-juice.jpg",
    "FRUIT CUSTARD": ASSETS / "fruit-custard.jpg",
    "PANI PURI":     ASSETS / "pani-puri.jpg",
    "VEG BIRYANI":   ASSETS / "Veg_Biryani.jpeg",
}

def get_food_img(name: str) -> str:
    key = name.upper()
    path = FOOD_IMAGES.get(key)
    if path and path.exists():
        return img_b64(path)
    for stock in ["stock-1.png", "stock-2.png", "stock-food-1.jpg"]:
        p = ASSETS / stock
        if p.exists():
            return img_b64(p)
    return ""

# ── SVG Smoke Animation ───────────────────────────────────────────────────────
SMOKE_SVG = """
<div class="smoke-container">
    <svg viewBox="0 0 100 100" class="smoke-svg">
        <circle class="p1" cx="50" cy="80" r="10" />
        <circle class="p2" cx="40" cy="85" r="12" />
        <circle class="p3" cx="60" cy="82" r="11" />
        <circle class="p4" cx="45" cy="88" r="9" />
        <circle class="p5" cx="55" cy="84" r="10" />
    </svg>
</div>
"""

# ── Global CSS ─────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Poppins:wght@300;400;600;700&display=swap');
html, body, [class*="css"] {{ font-family: 'Poppins', sans-serif; }}

/* === MARQUEE BANNER === */
.top-banner {{
    width:100%; background:blueviolet; padding:8px 12px;
    display:flex; align-items:center; gap:12px;
    border-radius:10px; margin-bottom:15px; overflow:hidden;
}}
.banner-icon {{ width:24px; height:24px; object-fit:contain; background:white; border-radius:50%; padding:2px; }}
.marquee-box {{ flex:1; overflow:hidden; white-space:nowrap; }}
.banner-text {{
    display:inline-block; font-size:0.85rem; color:white; font-weight:600; font-style:italic;
    animation: marqueeScroll 25s linear infinite;
}}
@keyframes marqueeScroll {{ 0% {{ transform:translateX(100%); }} 100% {{ transform:translateX(-100%); }} }}

/* === HEADER === */
.app-header {{
    background:linear-gradient(135deg,#FF9933 0%,#FF7700 100%);
    padding:18px 25px; border-radius:16px; margin-bottom:20px;
    box-shadow:0 6px 24px rgba(255,102,0,0.3); display:flex; align-items:center; justify-content:space-between;
}}
.header-title {{
    font-family:'Great Vibes', cursive; font-size:3.5rem; color:#800020;
    text-shadow:2px 2px 0 #fff; margin:0; display:flex; align-items:center; gap:12px;
}}

/* === FOOD CARDS === */
.food-card {{
    background:white; border:2px solid #FF9933; border-radius:18px; 
    padding:0 0 15px 0; overflow:hidden; text-align:center;
    box-shadow:0 5px 15px rgba(0,0,0,0.08); transition:0.3s; height:100%;
}}
.food-card:hover {{ transform:translateY(-5px); border-color:#FF5500; }}
.img-wrap {{ position:relative; width:100%; height:170px; background:#f9f9f9; }}
.card-img {{ width:100%; height:100%; object-fit:cover; }}

/* === SMOKE SVG ANIMATION === */
.smoke-container {{ position:absolute; bottom:0; left:0; width:100%; height:100%; pointer-events:none; z-index:99; }}
.smoke-svg {{ width:100%; height:100%; filter:blur(5px); }}
.smoke-svg circle {{ fill:rgba(255,255,255,0.85); opacity:0; animation: smokeRise 2.5s infinite ease-out; }}
.p1 {{ animation-delay:0s; }} .p2 {{ animation-delay:0.5s; }} .p3 {{ animation-delay:1s; }} .p4 {{ animation-delay:1.5s; }} .p5 {{ animation-delay:2s; }}
@keyframes smokeRise {{ 0% {{ transform:translateY(0) scale(1); opacity:0; }} 20% {{ opacity:0.8; }} 100% {{ transform:translateY(-130px) scale(4); opacity:0; }} }}

/* === LOGIN PAGE === */
.login-page {{ background:linear-gradient(135deg,#FF9933 0%,#FFFFFF 50%,#138808 100%); padding:60px 0; border-radius:16px; min-height:80vh; }}
.login-card {{ background:white; border-radius:24px; padding:45px 35px; max-width:400px; margin:0 auto; box-shadow:0 25px 50px rgba(0,0,0,0.2); text-align:center; }}
.lc-copy {{ font-size:0.85rem; font-style:italic; font-weight:700; background:linear-gradient(to right,#FF9933,#000080,#138808); -webkit-background-clip:text; background-clip:text; color:transparent; }}

/* === CARD TEXT === */
.food-card h3 {{ color:#800020; font-size:1.15rem; margin:12px 0 5px; font-weight:700; }}
.price-tag {{ color:#FF6600; font-weight:800; font-size:1.25rem; margin:5px 0; }}
.cat-badge {{ display:inline-block; background:#FF9933; color:white; font-size:0.75rem; font-weight:700; border-radius:20px; padding:3px 12px; margin-bottom:8px; }}

/* === CHATBOT UI === */
.chatbot-bubble {{
    position: fixed; bottom: 20px; right: 20px; z-index: 1000;
    cursor: pointer; transition: 0.3s;
}}
.chatbot-bubble:hover {{ transform: scale(1.1); rotate: 5deg; }}
.chatbot-bubble img {{ width: 70px; height: 70px; border-radius: 50%; box-shadow: 0 4px 15px rgba(0,0,0,0.3); border: 2px solid white; }}
</style>
""", unsafe_allow_html=True)

# ── Session State Logic ───────────────────────────────────────────────────────
if "logged_in" not in st.session_state: st.session_state["logged_in"] = False
if "username" not in st.session_state: st.session_state["username"] = ""
if "cart" not in st.session_state: st.session_state["cart"] = {}
if "chat_open" not in st.session_state: st.session_state["chat_open"] = False
if "messages" not in st.session_state: 
    hour = datetime.now().hour
    greeting = "Good Morning" if hour < 12 else "Good Afternoon" if hour < 18 else "Good Evening"
    st.session_state["messages"] = [{"role": "assistant", "content": f"{greeting}! 👋 I'm your food assistant. What would you like to eat today?"}]

if "menu_items" not in st.session_state:
    st.session_state["menu_items"] = [
        {"id":1, "name":"IDLY", "price":10, "category":"Breakfast", "hot":True},
        {"id":2, "name":"DOSA", "price":20, "category":"Breakfast", "hot":True},
        {"id":3, "name":"VADA", "price":30, "category":"Snacks", "hot":True},
        {"id":4, "name":"POORI", "price":40, "category":"Breakfast", "hot":True},
        {"id":5, "name":"TEA", "price":10, "category":"Beverages", "hot":True},
        {"id":6, "name":"COFFEE", "price":15, "category":"Beverages", "hot":True},
        {"id":7, "name":"MASALA VADA", "price":35, "category":"Snacks", "hot":True},
        {"id":8, "name":"UPMA", "price":25, "category":"Breakfast", "hot":True},
        {"id":9, "name":"FALUDA", "price":50, "category":"Beverages", "hot":False},
        {"id":10, "name":"MANGO JUICE", "price":40, "category":"Beverages", "hot":False},
    ]

# ── Cart Logic ────────────────────────────────────────────────────────────────
def add_to_cart(item):
    iid = str(item["id"])
    if iid in st.session_state["cart"]:
        st.session_state["cart"][iid]["qty"] += 1
    else:
        st.session_state["cart"][iid] = {"name": item["name"], "price": item["price"], "qty": 1}
    st.toast(f"Added {item['name']} to cart! 🛒")

# ── Chatbot Logic ─────────────────────────────────────────────────────────────
def get_bot_response(user_input):
    msg = user_input.lower()
    items = st.session_state["menu_items"]
    
    if any(k in msg for k in ['hi', 'hello', 'hey']):
        return "Hello! 😊 I'm here to help you order delicious South Indian food. What are you craving?"
    if any(k in msg for k in ['breakfast', 'morning']):
        b_items = [i for i in items if i['category'] == 'Breakfast']
        item_list = "\n".join([f"• {i['name']} - ₹{i['price']}" for i in b_items])
        return f"🌅 Good morning! Here are our delicious breakfast items:\n\n{item_list}\n\nPerfect way to start your day! 😊"
    if any(k in msg for k in ['popular', 'best', 'recommend']):
        return "😋 Our most popular items are **IDLY** (soft & healthy), **DOSA** (crispy golden), and **VADA**! You can't go wrong with these. 💯"
    if any(k in msg for k in ['price', 'cheap', 'budget']):
        cheapest = min(items, key=lambda x: x['price'])
        return f"Our most affordable option is **{cheapest['name']}** at only ₹{cheapest['price']}. great value! 💰"
    
    return "I'm not sure about that, but I can help you find something tasty! Browse our menu or ask about breakfast/snacks. 📋"

# ─────────────────────────────────────────────────────────────────────────────
# PAGE ROUTING
# ─────────────────────────────────────────────────────────────────────────────

if not st.session_state["logged_in"]:
    chef_tag = f'<img src="{CHEF_B64}" style="width:110px;height:110px;border-radius:50%;border:4px solid #FF9933;object-fit:cover;">' if CHEF_B64 else "🍛"
    st.markdown(f'<div class="login-page"><div class="login-card">{chef_tag}<h2>Welcome to South Indian Food App</h2><p class="lc-copy">copyright@Bhadradri Technologies.Inc</p></div></div>', unsafe_allow_html=True)
    _, col2, _ = st.columns([1,1.2,1])
    with col2:
        with st.form("login"):
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.form_submit_button("LOGIN", use_container_width=True):
                if u.strip() and p == "Admin123":
                    st.session_state["logged_in"] = True
                    st.session_state["username"] = u.strip()
                    st.rerun()
                else: st.error("Wrong password (PW: Admin123)")
    st.stop()

# ── LOGGED IN ──

# Top banner
icon_html = f'<img src="{BHADRADRI_B64}" class="banner-icon">' if BHADRADRI_B64 else ""
st.markdown(f'<div class="top-banner">{icon_html}<div class="marquee-box"><p class="banner-text">This project @ designed by Bhadradri Technologies.Inc</p></div></div>', unsafe_allow_html=True)

# Header
logo_html = f'<img src="{LOGIN_FOOD_B64}" style="width:70px;height:70px;border-radius:50%;border:4px solid white;object-fit:cover;">' if LOGIN_FOOD_B64 else ""
sun_html  = f'<img src="{SUNRISE_B64}" style="width:48px;height:48px;vertical-align:middle;margin-left:10px;">' if SUNRISE_B64 else ""
st.markdown(f'<div class="app-header"><div style="display:flex;align-items:center;">{logo_html}<h1 class="header-title">South Indian Food {sun_html}</h1></div><div style="color:white;font-weight:700;">Hello, {st.session_state["username"]}</div></div>', unsafe_allow_html=True)

# Sidebar with Cart
with st.sidebar:
    st.title("🛒 Your Cart")
    cart = st.session_state["cart"]
    if not cart:
        st.info("Your cart is empty. Add items from the menu!")
    else:
        total = 0
        for iid, item in cart.items():
            subtotal = item['price'] * item['qty']
            total += subtotal
            st.markdown(f"""
            <div style="background:#fff8f0; border-left:4px solid #FF9933; border-radius:8px; padding:10px; margin-bottom:10px;">
                <strong>{item['name']}</strong> x {item['qty']} <span style="float:right;">₹{subtotal}</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown(f'<div style="background:linear-gradient(135deg,#FF9933,#FF6600); color:white; border-radius:12px; padding:15px; text-align:center; font-size:1.2rem; font-weight:700;">🧾 Total: ₹{total}</div>', unsafe_allow_html=True)
        
        if st.button("Clear Cart 🗑️"):
            st.session_state["cart"] = {}
            st.rerun()
        
        if st.button("CONFIRM ORDER ✅", type="primary", use_container_width=True):
            st.balloons()
            st.success("Order Placed Successfully!")
            st.session_state["cart"] = {}
            st.rerun()

    st.markdown("---")
    if st.button("Logout 🚪", use_container_width=True):
        st.session_state["logged_in"] = False
        st.rerun()

# ── MENU GRID ──
st.markdown('<h2 style="color:#800020; border-bottom:3px solid #FF9933; padding-bottom:5px;">🍽️ Fresh Menu</h2>', unsafe_allow_html=True)

menu_items = st.session_state["menu_items"]
cols = st.columns(4)
for i, item in enumerate(menu_items):
    with cols[i % 4]:
        img_src = get_food_img(item["name"])
        img_tag = f'<img src="{img_src}" class="card-img">' if img_src else "🍛"
        smoke_effect = SMOKE_SVG if item.get("hot") else ""
        
        card_html = (
            f'<div class="food-card"><div class="img-wrap">{img_tag}{smoke_effect}</div>'
            f'<h3>{item["name"]}</h3>'
            f'<div class="cat-badge">{item["category"]}</div>'
            f'<div class="price-tag">₹{item["price"]}</div></div>'
        )
        st.markdown(card_html, unsafe_allow_html=True)
        
        if st.button(f"Add 🛒", key=f"add_btn_{item['id']}", use_container_width=True):
            add_to_cart(item)

# ── CHATBOT UI ──
# Floating bubble logic
if st.button("Chat Assistant 🤖", type="secondary", icon="💬"):
    st.session_state["chat_open"] = not st.session_state.get("chat_open", False)

if st.session_state.get("chat_open"):
    st.markdown("---")
    st.subheader("Foodie Bot Assistant 🤖")
    
    # Simple chat container
    chat_container = st.container(height=300)
    for message in st.session_state.messages:
        with chat_container.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask me about the menu..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container.chat_message("user"):
            st.markdown(prompt)
        
        response = get_bot_response(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        with chat_container.chat_message("assistant"):
            st.markdown(response)

st.markdown("---")
st.caption("Bhadradri Technologies.Inc © 2025")
