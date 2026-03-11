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
        try:
            ext = path.suffix.lstrip(".").lower()
            ext = "jpeg" if ext in ("jpg", "jpeg") else ext
            encoded = base64.b64encode(path.read_bytes()).decode()
            return f"data:image/{ext};base64,{encoded}"
        except: return ""
    return ""

# Pre-load required assets
BHADRADRI_B64    = img_b64(ASSETS / "bhadradri-icon-small.png")
LOGO_B64         = img_b64(ASSETS / "logo.png")
CHEF_B64         = img_b64(ASSETS / "south-indian-chef.png")
SUNRISE_B64      = img_b64(ASSETS / "sunrise-icon.png")
CHATBOT_ICON_B64 = img_b64(ASSETS / "chatbot-icon.png")
LOGIN_FOOD_B64   = img_b64(ASSETS / "login-food.png")
SHOWCASE_VIDEO   = ASSETS / "showcase-video-1.mp4"

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
    for stock in ["stock-1.png", "stock-2.png", "stock-3.png"]:
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

# ── Smoke SVG ─────────────────────────────────────────────────────────────────
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

/* === MAIN HEADER === */
.app-header {{
    background:linear-gradient(135deg,#FF9933 0%,#FF7700 100%);
    padding:12px 20px; border-radius:16px; margin-bottom:20px;
    box-shadow:0 6px 20px rgba(0,0,0,0.15); display:flex; align-items:center; justify-content:space-between;
}}
.header-left {{ display:flex; align-items:center; gap:15px; }}
.header-logo {{ width:70px; height:70px; border-radius:50%; border:3px solid white; object-fit:cover; }}
.header-title {{ font-family:'Great Vibes', cursive; font-size:4rem; color:#800020; text-shadow:2px 2px 0 #fff; margin:0; font-weight:700; }}
.header-right {{ display:flex; align-items:center; gap:10px; color:white; font-weight:600; font-size:1.1rem; }}

/* === FOOD CARDS === */
.food-card {{
    background:white; border:2px solid #FF9933; border-radius:18px; 
    padding:0 0 12px 0; overflow:hidden; text-align:center;
    box-shadow:0 4px 12px rgba(0,0,0,0.06); transition:0.3s; height:100%; margin-bottom:10px;
}}
.food-card:hover {{ transform:translateY(-4px); border-color:#FF5500; }}
.img-wrap {{ position:relative; width:100%; height:160px; background:#f5f5f5; }}
.card-img {{ width:100%; height:100%; object-fit:cover; }}

.smoke-container {{ position:absolute; bottom:0; left:0; width:100%; height:100%; pointer-events:none; z-index:99; }}
.smoke-svg {{ width:100%; height:100%; filter:blur(4px); }}
.smoke-svg circle {{ fill:rgba(255,255,255,0.85); opacity:0; animation: smokeRise 2.5s infinite ease-out; }}
@keyframes smokeRise {{ 0% {{ transform:translateY(0) scale(1); opacity:0; }} 20% {{ opacity:0.8; }} 100% {{ transform:translateY(-130px) scale(4); opacity:0; }} }}
.p1 {{ animation-delay:0s; }} .p2 {{ animation-delay:0.5s; }} .p3 {{ animation-delay:1s; }} .p4 {{ animation-delay:1.5s; }} .p5 {{ animation-delay:2s; }}

/* === CHATBOT BUBBLE (Matches React exactly) === */
.chatbot-container {{
    position: fixed; bottom: 30px; right: 30px; z-index: 99999;
    display: flex; flex-direction: column; align-items: center; gap: 8px;
}}
.chatbot-tooltip {{
    background: white; padding: 10px 15px; border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.15); font-size: 0.82rem;
    color: #333; width: 200px; text-align: center; position: relative;
    border: 1px solid #eee; animation: fadeIn 0.4s ease-out;
}}
.chatbot-tooltip::after {{
    content: ''; position: absolute; bottom: -8px; right: 25px;
    width: 0; height: 0; border-left: 8px solid transparent;
    border-right: 8px solid transparent; border-top: 8px solid white;
}}
.bot-avatar-box {{ position: relative; cursor: pointer; }}
.bot-img {{
    width: 70px; height: 70px; border-radius: 50%; border: 3px solid white;
    box-shadow: 0 4px 12px rgba(0,0,0,0.25); background: white;
    animation: bounce 2s infinite ease-in-out;
}}
.badge-count {{
    position: absolute; top: -2px; right: -2px;
    background: #138808; color: white; border-radius: 50%;
    width: 22px; height: 22px; display: flex; align-items: center;
    justify-content: center; font-size: 0.7rem; font-weight: 700;
    border: 2px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.3);
}}
@keyframes bounce {{ 0%, 100% {{ transform:translateY(0); }} 50% {{ transform:translateY(-8px); }} }}
@keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: translateY(0); }} }}

/* Payment Card */
.payment-card {{
    background:#fff3e0; padding:25px; border-radius:16px; 
    border:2px solid #FF9933; margin:20px 0;
}}

/* Card text */
.food-card h3 {{ color:#800020; font-size:1.1rem; margin:10px 0 2px; font-weight:700; }}
.price-tag {{ color:#FF6600; font-weight:800; font-size:1.25rem; }}
.cat-badge {{ display:inline-block; background:#FF9933; color:white; font-size:0.75rem; font-weight:700; border-radius:20px; padding:2px 12px; margin-bottom:5px; }}

</style>
""", unsafe_allow_html=True)

# ── Session State Initialization ──────────────────────────────────────────────
if "logged_in" not in st.session_state: st.session_state["logged_in"] = False
if "username" not in st.session_state: st.session_state["username"] = ""
if "cart" not in st.session_state: st.session_state["cart"] = {}
if "admin_mode" not in st.session_state: st.session_state["admin_mode"] = False
if "show_payment" not in st.session_state: st.session_state["show_payment"] = False
if "messages" not in st.session_state:
    now = datetime.now()
    greet = "Good Morning" if now.hour < 12 else "Good Afternoon" if now.hour < 18 else "Good Evening"
    st.session_state["messages"] = [{"role": "assistant", "content": f"{greet}! 👋 I'm your food assistant. What would you like to eat today?"}]

if "menu" not in st.session_state:
    st.session_state["menu"] = [
        {"id":1, "name":"IDLY", "price":10, "category":"Breakfast", "hot":True},
        {"id":2, "name":"DOSA", "price":20, "category":"Breakfast", "hot":True},
        {"id":3, "name":"VADA", "price":30, "category":"Snacks", "hot":True},
        {"id":4, "name":"POORI", "price":40, "category":"Breakfast", "hot":True},
        {"id":5, "name":"TEA", "price":10, "category":"Beverages", "hot":True},
        {"id":6, "name":"COFFEE", "price":15, "category":"Beverages", "hot":True},
    ]

# ── LOGIN PAGE ──
if not st.session_state["logged_in"]:
    chef_tag = f'<img src="{CHEF_B64}" style="width:110px;height:110px;border-radius:50%;border:4px solid #FF9933;object-fit:cover;">' if CHEF_B64 else "🍛"
    st.markdown(f'<div style="background:linear-gradient(135deg,#FF9933 0%,#FFFFFF 50%,#138808 100%); padding:60px 0; border-radius:16px; min-height:80vh;"><div style="background:white; border-radius:24px; padding:45px 35px; max-width:400px; margin:0 auto; box-shadow:0 25px 50px rgba(0,0,0,0.2); text-align:center;">{chef_tag}<h2>Welcome to South Indian Food App</h2><p style="font-size:0.85rem; font-style:italic; font-weight:700; color:#888;">copyright@Bhadradri Technologies.Inc</p></div></div>', unsafe_allow_html=True)
    _, c2, _ = st.columns([1,1.2,1])
    with c2:
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

# ── LOGGED IN UI ──

# Banner
icon_b = f'<img src="{BHADRADRI_B64}" class="banner-icon">' if BHADRADRI_B64 else ""
st.markdown(f'<div class="top-banner">{icon_b}<div class="marquee-box"><p class="banner-text">This project @ designed by Bhadradri Technologies.Inc</p></div></div>', unsafe_allow_html=True)

# Header
logo_h = f'<img src="{LOGIN_FOOD_B64}" class="header-logo">' if LOGIN_FOOD_B64 else ""
sun_h  = f'<img src="{SUNRISE_B64}" style="width:50px;height:50px;vertical-align:middle;margin-left:10px;">' if SUNRISE_B64 else ""
st.markdown(f'<div class="app-header"><div class="header-left">{logo_h}<h1 class="header-title">South Indian Food {sun_h}</h1></div><div class="header-right">Hello, {st.session_state["username"]}</div></div>', unsafe_allow_html=True)

# Buttons
b1, b2, b3, b4 = st.columns([1,1,3,1])
with b1:
    if st.button("🔐 Admin", use_container_width=True): st.session_state["admin_mode"] = not st.session_state["admin_mode"]
with b2:
    show_vid = st.toggle("🎬 Showcase", False)
with b4:
    if st.button("Logout 🚪", use_container_width=True): st.session_state["logged_in"] = False; st.rerun()

# Showcase logic
if show_vid:
    if SHOWCASE_VIDEO.exists(): st.video(str(SHOWCASE_VIDEO))
    else: st.warning("Showcase video not found in assets.")

# Admin logic
if st.session_state["admin_mode"]:
    pw = st.text_input("Admin Password", type="password")
    if pw == "sriram123":
        st.success("Admin Panel Unlocked!")
        with st.form("add_item"):
            n = st.text_input("Item Name")
            p = st.number_input("Price (₹)", 1)
            c = st.selectbox("Category", ["Breakfast", "Snacks", "Lunch", "Beverages"])
            h = st.checkbox("Hot Item", True)
            if st.form_submit_button("Add to Menu"):
                st.session_state["menu"].append({"id": len(st.session_state["menu"])+1, "name":n.upper(), "price":p, "category":c, "hot":h})
                st.rerun()
    elif pw: st.error("Access Denied")

# Menu Grid
st.markdown('<h2 style="color:#800020; border-bottom:3px solid #FF9933; padding-bottom:10px; margin-top:20px;">🍽️ Fresh Menu</h2>', unsafe_allow_html=True)
mcols = st.columns(4)
for i, item in enumerate(st.session_state["menu"]):
    with mcols[i % 4]:
        img_s = get_food_img(item["name"])
        img_html = f'<img src="{img_s}" class="card-img">' if img_s else "🍛"
        smoke = SMOKE_SVG if item.get("hot") else ""
        st.markdown(f'<div class="food-card"><div class="img-wrap">{img_html}{smoke}</div><h3>{item["name"]}</h3><div class="cat-badge">{item["category"]}</div><div class="price-tag">₹{item["price"]}</div></div>', unsafe_allow_html=True)
        if st.button(f"Add 🛒", key=f"add_{item['id']}", use_container_width=True):
            iid = str(item["id"])
            if iid in st.session_state["cart"]: st.session_state["cart"][iid]["qty"] += 1
            else: st.session_state["cart"][iid] = {"name":item["name"], "price":item["price"], "qty": 1}
            st.toast(f"Added {item['name']}! 🛒")

# Sidebar Cart
with st.sidebar:
    st.title("🛒 Your Order")
    if not st.session_state["cart"]: st.info("Cart is empty")
    else:
        tp = 0
        for iid, it in st.session_state["cart"].items():
            s = it['price']*it['qty']
            tp += s
            st.write(f"**{it['name']}** x {it['qty']} - ₹{s}")
        st.markdown(f"### Total: ₹{tp}")
        if st.button("Confirm Order 🍛", type="primary", use_container_width=True):
            st.session_state["show_payment"] = True
            st.rerun()

# Payment Logic
if st.session_state["show_payment"]:
    st.markdown('<div class="payment-card"><h2 style="color:#800020; text-align:center;">🛡️ Payment Gateway</h2>', unsafe_allow_html=True)
    pcol1, pcol2 = st.columns(2)
    with pcol1:
        st.markdown("### 🧾 Summary")
        topay = sum(it['price']*it['qty'] for it in st.session_state["cart"].values())
        st.write(f"Grand Total: **₹{topay}**")
    with pcol2:
        upi_link = f"upi://pay?pa=merchant@upi&pn=SouthIndianDelights&am={topay}&cu=INR"
        st.image(generate_upi_qr(upi_link), width=200, caption="Scan to Pay")
    if st.button("✅ I HAVE PAID", type="primary", use_container_width=True):
        st.balloons(); st.success("Verified!"); st.session_state["cart"] = {}; st.session_state["show_payment"] = False; st.rerun()
    if st.button("❌ Cancel"): st.session_state["show_payment"] = False; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ── FLOATING CHATBOT ──
c_now = datetime.now().hour
txt = "Good Morning" if c_now < 12 else "Good Afternoon" if c_now < 18 else "Good Evening"
count = sum(it["qty"] for it in st.session_state["cart"].values())
badge = f'<div class="badge-count">{count}</div>' if count > 0 else ""
bot_img = f'<img src="{CHATBOT_ICON_B64}" class="bot-img">' if CHATBOT_ICON_B64 else "🤖"

# Combine into ONE line to avoid stray </div> rendering
chat_html = f'<div class="chatbot-container"><div class="chatbot-tooltip">{txt}! 👋 I\'m your food assistant. What would you like to eat today?</div><div class="bot-avatar-box">{bot_img}{badge}</div></div>'
st.markdown(chat_html, unsafe_allow_html=True)

with st.expander("🗨️ Help Chat"):
    for m in st.session_state["messages"]:
        with st.chat_message(m["role"]): st.markdown(m["content"])
    if p := st.chat_input("Ask me something..."):
        st.session_state["messages"].append({"role": "user", "content": p})
        st.session_state["messages"].append({"role": "assistant", "content": "Our DOSA and VADA are freshly made! 🍛"})
        st.rerun()

st.caption("Bhadradri Technologies.Inc © 2025")
