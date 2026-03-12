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
CHEF_B64         = img_b64(ASSETS / "chatbot-icon.png")
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

.app-header {{
    background:linear-gradient(135deg,#FF9933 0%,#FF7700 100%);
    padding:12px 20px; border-radius:16px; margin-bottom:20px;
    box-shadow:0 6px 20px rgba(0,0,0,0.15); display:flex; align-items:center; justify-content:space-between;
}}
.header-logo {{ width:70px; height:70px; border-radius:50%; border:3px solid white; object-fit:cover; }}
.header-title {{ font-family:'Great Vibes', cursive; font-size:3.5rem; color:#800020; margin:0; font-weight:700; }}

.food-card {{
    background:white; border:2px solid #FF9933; border-radius:18px; padding:0 0 12px 0; overflow:hidden; text-align:center;
    box-shadow:0 6px 15px rgba(0,0,0,0.08); transition:0.3s; height:100%; margin-bottom:10px;
}}
.food-card:hover {{ transform:translateY(-4px); border-color:#FF5500; }}
.img-wrap {{ position:relative; width:100%; height:150px; background:#f5f5f5; }}
.card-img {{ width:100%; height:100%; object-fit:cover; }}

/* === THE ALIGNED FLOATING BOT HUB === */
.chatbot-fixed-hub {{
    position: fixed; bottom: 30px; right: 30px; z-index: 100000;
    display: flex; flex-direction: column; align-items: flex-end; gap: 5px;
}}

/* Greeting Tooltip */
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

/* REFACTORED POPOVER: Panel below the image */
div[data-testid="stPopover"] {{
    bottom: 5px; right: 0; position: relative;
}}
div[data-testid="stPopover"] button {{
    background-image: url("{CHEF_B64}") !important;
    background-size: cover !important;
    background-position: center !important;
    background-color: white !important;
    width: 90px !important;
    height: 90px !important;
    border-radius: 50% !important;
    border: 4px solid white !important;
    box-shadow: 0 10px 30px rgba(0,0,0,0.4) !important;
    animation: bounceChef 2s infinite ease-in-out !important;
    color: transparent !important;
}}
div[data-testid="stPopover"] button div {{ display: none !important; }}

/* Alignment of the Chat Panel */
[data-testid="stPopoverContent"] {{
    margin-right: -10px !important;
    border: 2px solid #FF9933 !important;
    border-radius: 20px !important;
    box-shadow: 0 10px 40px rgba(0,0,0,0.2) !important;
}}

@keyframes bounceChef {{ 0%, 100% {{ transform:translateY(0); }} 50% {{ transform:translateY(-10px); }} }}
@keyframes fadeIn {{ from {{ opacity:0; transform:translateY(10px); }} to {{ opacity:1; transform:translateY(0); }} }}

.payment-box {{ background:#fff3e0; padding:30px; border-radius:24px; border:4px solid #FF9933; margin:20px 0; }}
</style>
""", unsafe_allow_html=True)

# ── Session State ─────────────────────────────────────────────────────────────
if "logged_in" not in st.session_state: st.session_state["logged_in"] = False
if "cart" not in st.session_state: st.session_state["cart"] = {}
if "show_payment" not in st.session_state: st.session_state["show_payment"] = False
if "messages" not in st.session_state:
    now = datetime.now()
    greet_text = "Good Morning" if now.hour < 12 else "Good Afternoon" if now.hour < 18 else "Good Evening"
    st.session_state["messages"] = [{"role": "assistant", "content": f"{greet_text}! 👋 I'm your food assistant. What would you like to eat today?"}]

if "menu" not in st.session_state:
    st.session_state["menu"] = [
        {"id":1, "name":"IDLY", "price":10, "category":"Breakfast", "hot":True},
        {"id":2, "name":"DOSA", "price":20, "category":"Breakfast", "hot":True},
        {"id":3, "name":"VADA", "price":30, "category":"Snacks", "hot":True},
        {"id":4, "name":"POORI", "price":40, "category":"Breakfast", "hot":True},
    ]

# ── LOGIN ──
if not st.session_state["logged_in"]:
    st.markdown(f'<div style="text-align:center; padding-top:100px;"><div style="width:120px;height:120px;border-radius:50%;border:4px solid #FF9933;background:white url(\'{CHEF_B64}\') center/cover;margin:0 auto;"></div><h1 style="color:#800020;">Welcome</h1></div>', unsafe_allow_html=True)
    _, login_inner, _ = st.columns([1,1.2,1])
    with login_inner:
        u_in = st.text_input("Username")
        p_in = st.text_input("Password", type="password")
        if st.button("LOGIN", use_container_width=True):
            if p_in == "Admin123":
                st.session_state["logged_in"] = True; st.rerun()
    st.stop()

# ── HEADER ──
logo_img = f'<img src="{LOGIN_FOOD_B64}" class="header-logo">' if LOGIN_FOOD_B64 else ""
st.markdown(f'<div class="app-header">{logo_img}<h1 class="header-title">South Indian Food</h1><div></div></div>', unsafe_allow_html=True)

# ── PAYMENT ──
if st.session_state["show_payment"]:
    st.markdown('<div class="payment-box">', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align:center; color:#800020;">Secure Checkout</h2>', unsafe_allow_html=True)
    current_tot = sum(it['price']*it['qty'] for it in st.session_state["cart"].values())
    st.image(generate_upi_qr(f"upi://pay?pa=m@upi&am={current_tot}"), width=180)
    if st.button("✅ I HAVE PAID", type="primary", use_container_width=True):
        st.balloons(); st.session_state["cart"] = {}; st.session_state["show_payment"] = False; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ── MENU ──
m_cols = st.columns(4)
for i, item in enumerate(st.session_state["menu"]):
    with m_cols[i % 4]:
        img_src = get_food_img(item["name"])
        img_tag = f'<img src="{img_src}" class="card-img">' if img_src else "🍛"
        st.markdown(f'<div class="food-card"><div class="img-wrap">{img_tag}</div><h3>{item["name"]}</h3><div class="price-tag">₹{item["price"]}</div></div>', unsafe_allow_html=True)
        if st.button(f"Add 🛒", key=f"add_{item['id']}", use_container_width=True):
            iid = str(item["id"]); st.session_state["cart"][iid] = st.session_state["cart"].get(iid, {"name":item["name"],"price":item["price"],"qty":0}); st.session_state["cart"][iid]["qty"] += 1; st.toast("Added!")

# ── SIDEBAR ──
with st.sidebar:
    st.title("🛒 Cart")
    if not st.session_state["cart"]: st.info("Empty")
    else:
        for iid, it in st.session_state["cart"].items(): st.write(f"**{it['name']}** x {it['qty']}")
        if st.button("Confirm Order 🍛", type="primary"): st.session_state["show_payment"] = True; st.rerun()

# ── BOT REPLIES ──
def get_bot_response(msg):
    m = msg.lower()
    menu = [it["name"] for it in st.session_state["menu"]]
    if any(k in m for k in ["hi", "hello"]): return "Hello! 👋 I'm **Foodie Bot**. How can I assist you today?"
    if any(k in m for k in ["item", "menu", "list"]): return f"Our delicious items today are: **{', '.join(menu)}**. What would you like to order?"
    if "breakfast" in m: return "🌅 Breakfast Specials: Idly, Dosa, and Poori! Dosa is the top choice! 😊"
    return "I'm here to help you order the best South Indian food! Ask me about the menu or breakfast items. 😊"

# ── THE RE-ALIGNED FLOATING BOT HUB ──
st.markdown('<div class="chatbot-fixed-hub">', unsafe_allow_html=True)
now_hour = datetime.now().hour
txt_greet = "Good Morning" if now_hour < 12 else "Good Afternoon" if now_hour < 18 else "Good Evening"
st.markdown(f'<div class="greeting-bubble">{txt_greet}! 👋 I\'m your food assistant. What would you like to eat today?</div>', unsafe_allow_html=True)

# THE MASCOT POPOVER
with st.popover(" "):
    # Bot Header with Image at top of panel
    st.markdown(f'<div style="text-align:center;"><img src="{CHEF_B64}" style="width:70px;height:70px;border-radius:50%;border:3px solid #FF9933;box-shadow:0 4px 10px rgba(0,0,0,0.1);"><h3 style="color:#800020;margin-top:10px;">Foodie Bot Assistant</h3></div>', unsafe_allow_html=True)
    
    # Scrollable chat box
    chat_container = st.container(height=350, border=False)
    for ms in st.session_state["messages"]:
        with chat_container.chat_message(ms["role"]): st.write(ms["content"])
    
    # Input inside the panel
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Ask a question...", label_visibility="collapsed")
        if st.form_submit_button("Send 📩", use_container_width=True):
            if user_input:
                st.session_state["messages"].append({"role": "user", "content": user_input})
                st.session_state["messages"].append({"role": "assistant", "content": get_bot_response(user_input)})
                st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
st.caption("Designed by Bhadradri Technologies.Inc © 2025")
