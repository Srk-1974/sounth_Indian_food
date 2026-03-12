import streamlit as st
import base64
from pathlib import Path
from datetime import datetime
import qrcode
from io import BytesIO

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
        try:
            ext = path.suffix.lstrip(".").lower()
            ext = "jpeg" if ext in ("jpg", "jpeg") else ext
            encoded = base64.b64encode(path.read_bytes()).decode()
            return f"data:image/{ext};base64,{encoded}"
        except: return ""
    return ""

BHADRADRI_B64    = img_b64(ASSETS / "bhadradri-icon-small.png")
# MALE CHEF for Main Windows
MALE_CHEF_B64    = img_b64(ASSETS / "south-indian-chef.png")
# LADY CHEF for Chatbot
LADY_CHEF_B64    = img_b64(ASSETS / "chatbot-icon.png")
SUNRISE_B64      = img_b64(ASSETS / "sunrise-icon.png")
LOGIN_FOOD_B64   = img_b64(ASSETS / "login-food.png")
SHOWCASE_VIDEO   = ASSETS / "showcase-video-1.mp4"

def get_food_img(name: str) -> str:
    key = name.upper()
    path = {
        "IDLY": ASSETS / "idly.png", "DOSA": ASSETS / "dosa.png",
        "VADA": ASSETS / "vada.png", "POORI": ASSETS / "poori.png",
    }.get(key)
    if path and path.exists(): return img_b64(path)
    return ""

def generate_upi_qr(upi_link):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(upi_link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#800020", back_color="white")
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

SMOKE_SVG = '<div class="smoke-container"><svg viewBox="0 0 100 100" class="smoke-svg"><circle class="p1" cx="50" cy="80" r="10" /><circle class="p2" cx="40" cy="85" r="12" /><circle class="p3" cx="60" cy="82" r="11" /><circle class="p4" cx="45" cy="88" r="9" /><circle class="p5" cx="55" cy="84" r="10" /></svg></div>'

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Poppins:wght@300;400;600;700&display=swap');
html, body, [class*="css"] {{ font-family: 'Poppins', sans-serif; }}

.top-banner {{
    width:100%; height:32px; background:blueviolet; padding:0 12px;
    display:flex; align-items:center; gap:10px; border-radius:10px; margin-bottom:12px; overflow:hidden;
}}
.marquee-box {{ flex:1; overflow:hidden; white-space:nowrap; }}
.banner-text {{
    display:inline-block; font-size:0.8rem; color:white; font-weight:500; font-style:italic;
    animation: marqueeScroll 25s linear infinite; margin:0; padding-left:100%;
}}
@keyframes marqueeScroll {{ 0% {{ transform:translateX(0); }} 100% {{ transform:translateX(-100%); }} }}

.app-header {{
    background:linear-gradient(135deg,#FF9933 0%,#FF7700 100%);
    padding:12px 20px; border-radius:16px; margin-bottom:20px;
    box-shadow:0 6px 20px rgba(0,0,0,0.15); display:flex; align-items:center; justify-content:space-between;
}}
.header-logo {{ width:70px; height:70px; border-radius:50%; border:3px solid white; object-fit:cover; }}
.header-title {{ font-family:'Great Vibes', cursive; font-size:3.5rem; color:#800020; margin:0; font-weight:700; }}

/* FOOD CARDS */
.food-card {{
    background:white; border:2px solid #FF9933; border-radius:18px; padding:0 0 12px 0; overflow:hidden; text-align:center;
    box-shadow:0 6px 15px rgba(0,0,0,0.08); transition:0.3s; height:100%; margin-bottom:10px;
}}
.food-card h3 {{ color:#800020; font-size:1.15rem; margin:10px 0 2px; font-weight:700; }}
.img-wrap {{ position:relative; width:100%; height:150px; background:#f5f5f5; }}
.card-img {{ width:100%; height:100%; object-fit:cover; }}
.price-tag {{ color:#FF6600; font-weight:800; font-size:1.35rem; }}

/* === FLOATING CHATBOT HUB (LADY CHEF) === */
.chatbot-fixed-hub {{
    position: fixed; bottom: 30px; right: 30px; z-index: 100000;
    display: flex; flex-direction: column; align-items: flex-end; gap: 5px;
}}
.greeting-bubble {{
    background: white; padding: 10px 15px; border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2); font-size: 0.8rem;
    color: #333; max-width: 200px; text-align: center; border: 1px solid #ddd;
    position: relative; animation: fadeIn 0.5s ease;
}}
.greeting-bubble::after {{
    content: ''; position: absolute; bottom: -8px; right: 35px;
    width: 0; height: 0; border-left: 8px solid transparent;
    border-right: 8px solid transparent; border-top: 8px solid white;
}}

/* POPOVER BUTTON AS LADY CHEF */
div[data-testid="stPopover"] {{ bottom: 5px; right: 0; position: relative; }}
div[data-testid="stPopover"] button {{
    background-image: url("{LADY_CHEF_B64}") !important;
    background-size: cover !important;
    background-position: center !important;
    background-color: white !important;
    width: 90px !important; height: 90px !important;
    border-radius: 50% !important; border: 4px solid white !important;
    box-shadow: 0 10px 30px rgba(0,0,0,0.4) !important;
    animation: bounceChef 2s infinite ease-in-out !important;
    color: transparent !important;
}}
div[data-testid="stPopover"] button div {{ display: none !important; }}

@keyframes bounceChef {{ 0%, 100% {{ transform:translateY(0); }} 50% {{ transform:translateY(-10px); }} }}
@keyframes fadeIn {{ from {{ opacity:0; transform:translateY(10px); }} to {{ opacity:1; transform:translateY(0); }} }}

.admin-panel {{ background: #fdfdfd; padding: 15px; border-radius: 15px; border: 1px solid #eee; margin-bottom: 20px; }}
</style>
""", unsafe_allow_html=True)

# ── Session State ─────────────────────────────────────────────────────────────
if "logged_in" not in st.session_state: st.session_state["logged_in"] = False
if "username" not in st.session_state: st.session_state["username"] = ""
if "cart" not in st.session_state: st.session_state["cart"] = {}
if "admin_mode" not in st.session_state: st.session_state["admin_mode"] = False
if "show_payment" not in st.session_state: st.session_state["show_payment"] = False
if "messages" not in st.session_state:
    now = datetime.now()
    greet_txt = "Good Morning" if now.hour < 12 else "Good Afternoon" if now.hour < 18 else "Good Evening"
    st.session_state["messages"] = [{"role": "assistant", "content": f"{greet_txt}! 👋 I'm your food assistant. What would you like to eat today?"}]

if "menu" not in st.session_state:
    st.session_state["menu"] = [
        {"id":1, "name":"IDLY", "price":10, "category":"Breakfast", "hot":True},
        {"id":2, "name":"DOSA", "price":20, "category":"Breakfast", "hot":True},
        {"id":3, "name":"VADA", "price":30, "category":"Snacks", "hot":True},
        {"id":4, "name":"POORI", "price":40, "category":"Breakfast", "hot":True},
    ]

# ── LOGIN ──
if not st.session_state["logged_in"]:
    # Using MALE CHEF for Login as requested
    chef_login = f'<div style="width:130px;height:130px;border-radius:50%;border:4px solid #FF9933;background:white url(\'{MALE_CHEF_B64}\') center/cover;margin:0 auto;box-shadow:0 10px 20px rgba(0,0,0,0.2);"></div>' if MALE_CHEF_B64 else "👩‍🍳"
    st.markdown(f'<div style="background:linear-gradient(135deg,#FF9933 0%,#FFFFFF 50%,#138808 100%); padding:120px 0; min-height:95vh;"><div style="background:white; border-radius:30px; padding:60px 40px; max-width:450px; margin:0 auto; box-shadow:0 30px 60px rgba(0,0,0,0.3); text-align:center;">{chef_login}<h1 style="color:#800020; margin-top:20px; font-size:2.5rem;">Welcome</h1><p style="font-weight:700; color:#555; font-size:1.1rem;">South Indian Food Order App</p></div></div>', unsafe_allow_html=True)
    _, l_col, _ = st.columns([1,1.2,1])
    with l_col:
        with st.form("login"):
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.form_submit_button("LOGIN", use_container_width=True):
                if p == "Admin123":
                    st.session_state["logged_in"] = True
                    st.session_state["username"] = u.strip() or "User"
                    st.rerun()
                else: st.error("Wrong Credentials!")
    st.stop()

# ── HEADER ──
# Using MALE CHEF for Header
logo_img = f'<img src="{MALE_CHEF_B64}" class="header-logo">' if MALE_CHEF_B64 else ""
st.markdown(f'<div class="app-header"><div style="display:flex;align-items:center;">{logo_img}<h1 class="header-title">South Indian Food</h1></div><div style="color:white; font-weight:700;">Hi, {st.session_state["username"]}</div></div>', unsafe_allow_html=True)

# ── ADMIN & ACTIONS ──
# Restoring missing Admin buttons
with st.container():
    a1, a2, a3, a4 = st.columns(4)
    with a1:
        if st.button("🛠️ Admin Mode", use_container_width=True):
            st.session_state["admin_mode"] = not st.session_state["admin_mode"]
    with a2:
        if st.button("📽️ Showcase", use_container_width=True):
            st.toast("Showcase video coming soon!")
    with a3:
        if st.button("🍱 View Menu", use_container_width=True): pass
    with a4:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state["logged_in"] = False; st.rerun()

if st.session_state["admin_mode"]:
    st.markdown('<div class="admin-panel"><h4>🛠️ Admin Controls</h4><p>Manage items and prices here.</p></div>', unsafe_allow_html=True)

# ── PAYMENT ──
if st.session_state["show_payment"]:
    st.markdown('<div style="background:#fff3e0; padding:30px; border-radius:24px; border:4px solid #FF9933; margin:20px 0;">', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align:center; color:#800020;">🛡️ Secure Checkout</h2>', unsafe_allow_html=True)
    pay_tot = sum(it['price']*it['qty'] for it in st.session_state["cart"].values())
    st.image(generate_upi_qr(f"upi://pay?pa=m@upi&am={pay_tot}"), width=180)
    if st.button("✅ I HAVE PAID", type="primary", use_container_width=True):
        st.balloons(); st.session_state["cart"] = {}; st.session_state["show_payment"] = False; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ── MENU ──
st.markdown('<h2 style="color:#800020; border-bottom:3px solid #FF9933; margin-top:20px; padding-bottom:10px;">🍽️ Fresh Menu</h2>', unsafe_allow_html=True)
m_cols = st.columns(4)
for i, item in enumerate(st.session_state["menu"]):
    with m_cols[i % 4]:
        im_s = get_food_img(item["name"])
        im_t = f'<img src="{im_s}" class="card-img">' if im_s else "🍛"
        st.markdown(f'<div class="food-card"><div class="img-wrap">{im_t}</div><h3>{item["name"]}</h3><div class="price-tag">₹{item["price"]}</div></div>', unsafe_allow_html=True)
        if st.button(f"Add 🛒", key=f"add_{item['id']}", use_container_width=True):
            iid = str(item["id"])
            if iid in st.session_state["cart"]: st.session_state["cart"][iid]["qty"] += 1
            else: st.session_state["cart"][iid] = {"name":item["name"],"price":item["price"],"qty":1}
            st.toast(f"Added {item['name']}!")

# ── SIDEBAR ──
with st.sidebar:
    st.title("🛒 Your Order")
    if not st.session_state["cart"]: st.info("Cart is empty")
    else:
        for iid, it in st.session_state["cart"].items(): st.write(f"**{it['name']}** x {it['qty']}")
        if st.button("Confirm Order 🍛", type="primary", use_container_width=True): st.session_state["show_payment"] = True; st.rerun()

# ── BOT LOGIC ──
def bot_reply(msg):
    m = msg.lower()
    items = [it["name"] for it in st.session_state["menu"]]
    if any(k in m for k in ["hi", "hello"]): return "Hello! 👋 I'm **Foodie Bot**. How can I help you?"
    if any(k in m for k in ["item", "menu", "list"]): return f"Our selection: **{', '.join(items)}**. What would you like?"
    return "I'm here to help you order best South Indian food! 😊"

# ── FLOATING CHATBOT (LADY CHEF) ──
st.markdown('<div class="chatbot-fixed-hub">', unsafe_allow_html=True)
hr = datetime.now().hour
gr_msg = "Good Morning" if hr < 12 else "Good Afternoon" if hr < 18 else "Good Evening"
st.markdown(f'<div class="greeting-bubble">{gr_msg}! 👋 I\'m your food assistant. What would you like to eat today?</div>', unsafe_allow_html=True)

with st.popover(" "):
    # Bot Header with LADY CHEF
    st.markdown(f'<div style="text-align:center;"><img src="{LADY_CHEF_B64}" style="width:70px;height:70px;border-radius:50%;border:3px solid #FF9933;"><h3 style="color:#800020;margin-top:10px;">Foodie Bot</h3></div>', unsafe_allow_html=True)
    c_box = st.container(height=350, border=False)
    for ms in st.session_state["messages"]:
        with c_box.chat_message(ms["role"]): st.write(ms["content"])
    
    with st.form("c_form", clear_on_submit=True):
        u_q = st.text_input("Ask here...", label_visibility="collapsed")
        if st.form_submit_button("Send", use_container_width=True):
            if u_q:
                st.session_state["messages"].append({"role":"user","content":u_q})
                st.session_state["messages"].append({"role":"assistant","content":bot_reply(u_q)})
                st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
st.caption("Designed by Bhadradri Technologies.Inc © 2025")
