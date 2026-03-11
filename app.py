import streamlit as st
import base64
from pathlib import Path
from datetime import datetime
import qrcode
from io import BytesIO
from PIL import Image

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

# Pre-load ALL assets as Base64 for instant loading
BHADRADRI_B64    = img_b64(ASSETS / "bhadradri-icon-small.png")
LOGO_B64         = img_b64(ASSETS / "logo.png")
CHEF_B64         = img_b64(ASSETS / "south-indian-chef.png")
SUNRISE_B64      = img_b64(ASSETS / "sunrise-icon.png")
CHATBOT_ICON_B64 = img_b64(ASSETS / "chatbot-icon.png")

# Food image mapping
FOOD_IMAGES = {
    "IDLY": ASSETS / "idly.png", "DOSA": ASSETS / "dosa.png", "DOSHA": ASSETS / "dosa.png",
    "VADA": ASSETS / "vada.png", "MASALA VADA": ASSETS / "masala-vada.png", "POORI": ASSETS / "poori.png",
    "TEA": ASSETS / "tea.png", "COFFEE": ASSETS / "coffee.png", "UPMA": ASSETS / "upma-sambar.jpg",
    "FALUDA": ASSETS / "faluda.jpg", "MANGO JUICE": ASSETS / "mango-juice.jpg", "PANI PURI": ASSETS / "pani-puri.jpg",
    "VEG BIRYANI": ASSETS / "Veg_Biryani.jpeg",
}

def get_food_img(name: str) -> str:
    key = name.upper()
    path = FOOD_IMAGES.get(key)
    if path and path.exists(): return img_b64(path)
    for stock in ["stock-1.png", "stock-2.png"]:
        p = ASSETS / stock
        if p.exists(): return img_b64(p)
    return ""

# ── QR Code Generator ─────────────────────────────────────────────────────────
def generate_upi_qr(upi_link):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(upi_link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#800020", back_color="white")
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

# ── SVG Smoke Animation ───────────────────────────────────────────────────────
SMOKE_SVG = '<div class="smoke-container"><svg viewBox="0 0 100 100" class="smoke-svg"><circle class="p1" cx="50" cy="80" r="10" /><circle class="p2" cx="40" cy="85" r="12" /><circle class="p3" cx="60" cy="82" r="11" /><circle class="p4" cx="45" cy="88" r="9" /><circle class="p5" cx="55" cy="84" r="10" /></svg></div>'

# ── Global Styles ─────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Poppins:wght@300;400;600;700&display=swap');
html, body, [class*="css"] {{ font-family: 'Poppins', sans-serif; }}

/* === MARQUEE BANNER === */
.top-banner {{
    width:100%; height:32px; background:blueviolet; padding:0 12px;
    display:flex; align-items:center; gap:10px; border-radius:10px; margin-bottom:12px; overflow:hidden;
}}
.banner-icon {{ width:20px; height:20px; object-fit:contain; background:white; border-radius:50%; padding:2px; flex-shrink:0; }}
.marquee-box {{ flex:1; overflow:hidden; white-space:nowrap; }}
.banner-text {{
    display:inline-block; font-size:0.8rem; color:white; font-weight:500; font-style:italic;
    animation: marqueeScroll 25s linear infinite; margin:0;
}}
@keyframes marqueeScroll {{ 0% {{ transform:translateX(100%); }} 100% {{ transform:translateX(-100%); }} }}

/* === MAIN HEADER (Matches local screenshot) === */
.app-header {{
    background:linear-gradient(135deg,#FF9933 0%,#FF7700 100%);
    padding:12px 20px; border-radius:16px; margin-bottom:20px;
    box-shadow:0 6px 20px rgba(0,0,0,0.15); display:flex; align-items:center; justify-content:space-between;
}}
.header-left {{ display:flex; align-items:center; gap:12px; }}
.header-logo {{ width:65px; height:65px; border-radius:50%; border:3px solid white; object-fit:cover; }}
.header-title {{ font-family:'Great Vibes', cursive; font-size:3.2rem; color:#800020; text-shadow:2px 2px 0 #fff; margin:0; }}
.header-right {{ display:flex; align-items:center; gap:10px; }}
.user-greeting {{ color:white; font-size:1rem; font-weight:600; text-align:right; margin-right:8px; line-height:1.2; }}

/* === FOOD CARDS === */
.food-card {{
    background:white; border:2px solid #FF9933; border-radius:18px; 
    padding:0 0 12px 0; overflow:hidden; text-align:center;
    box-shadow:0 4px 12px rgba(0,0,0,0.06); transition:0.3s; height:100%; margin-bottom:10px;
}}
.food-card:hover {{ transform:translateY(-4px); border-color:#FF5500; }}
.img-wrap {{ position:relative; width:100%; height:160px; background:#f5f5f5; }}
.card-img {{ width:100%; height:100%; object-fit:cover; }}

/* SVG Rise Animation */
.smoke-container {{ position:absolute; bottom:0; left:0; width:100%; height:100%; pointer-events:none; z-index:99; }}
.smoke-svg {{ width:100%; height:100%; filter:blur(4px); }}
.smoke-svg circle {{ fill:rgba(255,255,255,0.85); opacity:0; animation: smokeRise 2.5s infinite ease-out; }}
.p1 {{ animation-delay:0s; }} .p2 {{ animation-delay:0.5s; }} .p3 {{ animation-delay:1s; }} .p4 {{ animation-delay:1.5s; }} .p5 {{ animation-delay:2s; }}
@keyframes smokeRise {{ 0% {{ transform:translateY(0) scale(1); opacity:0; }} 20% {{ opacity:0.8; }} 100% {{ transform:translateY(-130px) scale(4); opacity:0; }} }}

/* === FLOATING CHATBOT (Bottom Right) === */
.chat-bubble {{
    position: fixed; bottom: 30px; right: 30px; z-index: 9999;
    display: flex; align-items: center; gap: 12px; cursor: pointer;
}}
.chat-tooltip {{
    background: white; padding: 10px 15px; border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.15); font-size: 0.85rem;
    font-weight: 500; max-width: 180px; position: relative;
}}
.chat-tooltip::after {{
    content: ''; position: absolute; right: -8px; top: 50%; 
    transform: translateY(-50%); border-width: 8px 0 8px 8px;
    border-style: solid; border-color: transparent transparent transparent white;
}}
.bot-avatar {{
    width: 65px; height: 65px; border-radius: 50%; border: 2px solid white;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2); background: white;
    animation: bounce 2s infinite ease-in-out;
}}
@keyframes bounce {{ 0%, 100% {{ transform:translateY(0); }} 50% {{ transform:translateY(-8px); }} }}

/* Card Typography */
.food-card h3 {{ color:#800020; font-size:1.1rem; margin:10px 0 3px; font-weight:700; }}
.price-tag {{ color:#FF6600; font-weight:800; font-size:1.2rem; }}
.cat-badge {{ display:inline-block; background:#FF9933; color:white; font-size:0.7rem; font-weight:700; border-radius:12px; padding:2px 10px; margin-bottom:5px; }}
</style>
""", unsafe_allow_html=True)

# ── Session State Logic ───────────────────────────────────────────────────────
if "logged_in" not in st.session_state: st.session_state["logged_in"] = False
if "username" not in st.session_state: st.session_state["username"] = ""
if "cart" not in st.session_state: st.session_state["cart"] = {}
if "admin_mode" not in st.session_state: st.session_state["admin_mode"] = False
if "chat_open" not in st.session_state: st.session_state["chat_open"] = False
if "show_payment" not in st.session_state: st.session_state["show_payment"] = False
if "messages" not in st.session_state: 
    h = datetime.now().hour
    g = "Good Morning" if h < 12 else "Good Afternoon" if h < 18 else "Good Evening"
    st.session_state["messages"] = [{"role": "bot", "content": f"{g}! 👋 I'm your food assistant. What would you like to eat today?"}]

if "menu" not in st.session_state:
    st.session_state["menu"] = [
        {"id":1, "name":"IDLY", "price":10, "category":"Breakfast", "hot":True},
        {"id":2, "name":"DOSA", "price":20, "category":"Breakfast", "hot":True},
        {"id":3, "name":"VADA", "price":30, "category":"Snacks", "hot":True},
        {"id":4, "name":"POORI", "price":40, "category":"Breakfast", "hot":True},
        {"id":5, "name":"TEA", "price":10, "category":"Beverages", "hot":True},
        {"id":6, "name":"COFFEE", "price":15, "category":"Beverages", "hot":True},
    ]

# ── Page Rendering ────────────────────────────────────────────────────────────

if not st.session_state["logged_in"]:
    # Login Page (Indian Flag Gradient)
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

# ── MAIN APP UI ───────────────────────────────────────────────────────────────

# Banner
icon_h = f'<img src="{BHADRADRI_B64}" class="banner-icon">' if BHADRADRI_B64 else ""
st.markdown(f'<div class="top-banner">{icon_h}<div class="marquee-box"><p class="banner-text">This project @ designed by Bhadradri Technologies.Inc</p></div></div>', unsafe_allow_html=True)

# Header (Matches Screenshot)
logo_h = f'<img src="{LOGO_B64}" class="header-logo">' if LOGO_B64 else ""
sun_h  = f'<img src="{SUNRISE_B64}" style="width:40px;height:40px;vertical-align:middle;">' if SUNRISE_B64 else ""
st.markdown(f"""
<div class="app-header">
    <div class="header-left">
        {logo_h}
        <h1 class="header-title">South Indian Food {sun_h}</h1>
    </div>
    <div class="header-right">
        <div class="user-greeting">Hello,<br>{st.session_state["username"]}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Header Quick Action Buttons
c1, c2, c3, c4 = st.columns([1,1,3,1])
with c1:
    if st.button("🔐 Admin", use_container_width=True): st.session_state["admin_mode"] = not st.session_state["admin_mode"]
with c2:
    if st.button("🎬 Showcase", use_container_width=True): st.info("Showcase video feature coming soon!")
with c4:
    if st.button("Logout 🚪", use_container_width=True): 
        st.session_state["logged_in"] = False
        st.rerun()

# ── Admin Panel (Hidden Behind Password) ──
if st.session_state["admin_mode"]:
    st.markdown("### 🛠️ Admin Dashboard")
    ap = st.text_input("Enter Admin Password", type="password")
    if ap == "sriram123":
        st.success("Admin Access Unlocked!")
        with st.expander("➕ Add New Menu Item"):
            with st.form("add_item"):
                n = st.text_input("Item Name")
                p = st.number_input("Price (₹)", min_value=1)
                c = st.selectbox("Category", ["Breakfast", "Snacks", "Lunch", "Beverages"])
                h = st.checkbox("🔥 Hot Item", value=True)
                if st.form_submit_button("Add to Menu"):
                    st.session_state["menu"].append({"id": len(st.session_state["menu"])+1, "name":n.upper(), "price":p, "category":c, "hot":h})
                    st.rerun()
    elif ap: st.error("Incorrect Admin Password!")

# ── Menu Grid ──
st.markdown('<h2 style="color:#800020; border-bottom:3px solid #FF9933; padding-bottom:5px;">🍽️ Fresh Menu</h2>', unsafe_allow_html=True)

cols = st.columns(4)
for i, item in enumerate(st.session_state["menu"]):
    with cols[i % 4]:
        img_src = get_food_img(item["name"])
        img_tag = f'<img src="{img_src}" class="card-img">' if img_src else "🍛"
        smoke_tag = SMOKE_SVG if item.get("hot") else ""
        st.markdown(f'<div class="food-card"><div class="img-wrap">{img_tag}{smoke_tag}</div><h3>{item["name"]}</h3><div class="cat-badge">{item["category"]}</div><div class="price-tag">₹{item["price"]}</div></div>', unsafe_allow_html=True)
        if st.button(f"Add 🛒", key=f"a_{i}", use_container_width=True):
            iid = str(item["id"])
            if iid in st.session_state["cart"]: st.session_state["cart"][iid]["qty"] += 1
            else: st.session_state["cart"][iid] = {"name":item["name"], "price":item["price"], "qty":1}
            st.toast(f"Added {item['name']}! 🛒")

# ── Sidebar Cart ──
with st.sidebar:
    st.title("🛒 Your Order")
    if not st.session_state["cart"]: st.info("Empty cart")
    else:
        total = 0
        for iid, it in st.session_state["cart"].items():
            sub = it['price']*it['qty']
            total += sub
            st.write(f"**{it['name']}** x {it['qty']} - ₹{sub}")
        st.markdown(f"### Total: ₹{total}")
        if st.button("Confirm Order 🍛", type="primary", use_container_width=True):
            st.session_state["show_payment"] = True
            st.rerun()

# ── PAYMENT MODAL (Overlay) ──
if st.session_state["show_payment"]:
    st.markdown("---")
    st.markdown('<div style="background:#fff3e0; padding:25px; border-radius:16px; border:2px solid #FF9933; margin-top:20px;">', unsafe_allow_html=True)
    st.markdown('<h2 style="color:#800020; text-align:center; margin-bottom:20px;">🛡️ Payment Gateway</h2>', unsafe_allow_html=True)
    
    pay_col1, pay_col2 = st.columns([1.2, 1])
    
    with pay_col1:
        st.markdown("### 🧾 Order Summary")
        total_p = 0
        for iid, item in st.session_state["cart"].items():
            sub = item['price'] * item['qty']
            total_p += sub
            st.markdown(f"• **{item['name']}** x {item['qty']} <span style='float:right;'>₹{sub}</span>", unsafe_allow_html=True)
        st.markdown(f"<div style='border-top:2px solid #FF9933; margin-top:10px; padding-top:10px; font-size:1.5rem; font-weight:800; color:#FF6600;'>Total: ₹{total_p}</div>", unsafe_allow_html=True)
        
    with pay_col2:
        st.markdown('<div style="background:white; padding:15px; border-radius:12px; text-align:center;">', unsafe_allow_html=True)
        st.markdown("### 🏧 Pay via UPI")
        upi_vpa = "merchant@upi"
        upi_link = f"upi://pay?pa={upi_vpa}&pn=SouthIndianDelights&am={total_p}&cu=INR"
        qr_img = generate_upi_qr(upi_link)
        st.image(qr_img, width=220, caption="Scan with GPay, PhonePe, or Paytm")
        st.markdown(f"**Merchant:** `SouthIndianDelights`")
        st.markdown(f"**UPI ID:** `{upi_vpa}`")
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.markdown("---")
    b1, b2 = st.columns(2)
    with b1:
        if st.button("❌ Cancel Payment", use_container_width=True):
            st.session_state["show_payment"] = False
            st.rerun()
    with b2:
        if st.button("✅ I HAVE PAID", type="primary", use_container_width=True):
            st.balloons()
            st.success("💰 Payment Confirmed! Your order is being prepared.")
            st.session_state["cart"] = {}
            st.session_state["show_payment"] = False
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ── FLOATING CHATBOT (Purely Visual Bubble with Active Chat) ──
h_now = datetime.now().hour
greet = "Good Morning" if h_now < 12 else "Good Afternoon" if h_now < 18 else "Good Evening"

bot_icon_h = f'<img src="{CHATBOT_ICON_B64}" class="bot-avatar">' if CHATBOT_ICON_B64 else "🤖"
st.markdown(f"""
<div class="chat-bubble">
    <div class="chat-tooltip">{greet}! 👋 I'm your food assistant. What would you like to eat today?</div>
    {bot_icon_h}
</div>
""", unsafe_allow_html=True)

# Actual Chat Interface (Triggered by button)
with st.expander("🗨️ Chat with Foodie Bot"):
    for m in st.session_state["messages"]:
        with st.chat_message(m["role"]): st.markdown(m["content"])
    if p := st.chat_input("Ask me about the menu..."):
        st.session_state["messages"].append({"role": "user", "content": p})
        st.rerun()

st.caption("Bhadradri Technologies.Inc © 2025")
