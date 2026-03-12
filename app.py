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

BHADRADRI_B64    = img_b64(ASSETS / "bhadradri-icon-small.png")
CHEF_B64         = img_b64(ASSETS / "south-indian-chef.png")
SUNRISE_B64      = img_b64(ASSETS / "sunrise-icon.png")
LOGIN_FOOD_B64   = img_b64(ASSETS / "login-food.png")
SHOWCASE_VIDEO   = ASSETS / "showcase-video-1.mp4"

def get_food_img(name: str) -> str:
    key = name.upper()
    path = {
        "IDLY": ASSETS / "idly.png", "DOSA": ASSETS / "dosa.png", "DOSHA": ASSETS / "dosa.png",
        "VADA": ASSETS / "vada.png", "MASALA VADA": ASSETS / "masala-vada.png", "POORI": ASSETS / "poori.png",
        "TEA": ASSETS / "tea.png", "COFFEE": ASSETS / "coffee.png", "UPMA": ASSETS / "upma-sambar.jpg",
        "FALUDA": ASSETS / "faluda.jpg", "MANGO JUICE": ASSETS / "mango-juice.jpg", "PANI PURI": ASSETS / "pani-puri.jpg",
        "VEG BIRYANI": ASSETS / "Veg_Biryani.jpeg",
    }.get(key)
    if path and path.exists(): return img_b64(path)
    for stock in ["stock-1.png", "stock-2.png", "stock-3.png"]:
        p = ASSETS / stock
        if p.exists(): return img_b64(p)
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
.banner-icon {{ width:20px; height:20px; object-fit:contain; background:white; border-radius:50%; padding:2px; flex-shrink:0; }}
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
.header-title {{ font-family:'Great Vibes', cursive; font-size:3.8rem; color:#800020; text-shadow:2px 2px 0 #fff; margin:0; font-weight:700; }}

.food-card {{
    background:white; border:2px solid #FF9933; border-radius:18px; 
    padding:0 0 12px 0; overflow:hidden; text-align:center;
    box-shadow:0 10px 25px rgba(0,0,0,0.1); transition:0.3s; height:100%; margin-bottom:10px;
}}
.smoke-container {{ position:absolute; bottom:0; left:0; width:100%; height:100%; pointer-events:none; z-index:99; }}
.smoke-svg {{ width:100%; height:100%; filter:blur(4px); }}
.smoke-svg circle {{ fill:rgba(255,255,255,0.85); opacity:0; animation: smokeRise 2.5s infinite ease-out; }}
@keyframes smokeRise {{ 0% {{ transform:translateY(0) scale(1); opacity:0; }} 20% {{ opacity:0.8; }} 100% {{ transform:translateY(-130px) scale(4); opacity:0; }} }}

.p1 {{ animation-delay:0s; }} .p2 {{ animation-delay:0.5s; }} .p3 {{ animation-delay:1s; }} .p4 {{ animation-delay:1.5s; }} .p5 {{ animation-delay:2s; }}

/* === THE ONLY FLOATING BOT === */
.chatbot-fixed-wrap {{
    position: fixed; bottom: 30px; right: 30px; z-index: 10000;
    display: flex; flex-direction: column; align-items: center;
}}
/* Hide Streamlit Popover Button default look and make it the mascot */
button[data-testid="stBaseButton-secondary"] {{
    background: transparent !important; border: none !important; box-shadow: none !important;
}}
.chef-float-img {{
    width: 85px; height: 85px; border-radius: 50%; border: 3px solid white;
    box-shadow: 0 8px 30px rgba(0,0,0,0.3); background: white;
    animation: bounceChef 2s infinite ease-in-out;
}}
@keyframes bounceChef {{ 0%, 100% {{ transform:translateY(0); }} 50% {{ transform:translateY(-10px); }} }}

.bot-greeting-bubble {{
    background: white; padding: 10px 15px; border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2); font-size: 0.8rem;
    color: #333; max-width: 200px; text-align: center; margin-bottom: 5px;
    position: relative; border: 1px solid #ddd;
}}
.bot-greeting-bubble::after {{
    content: ''; position: absolute; bottom: -8px; right: 25px;
    width: 0; height: 0; border-left: 8px solid transparent;
    border-right: 8px solid transparent; border-top: 8px solid white;
}}

.payment-overlay {{ background:#fff3e0; padding:30px; border-radius:24px; border:4px solid #FF9933; margin:20px 0; box-shadow: 0 15px 40px rgba(0,0,0,0.15); }}
.food-card h3 {{ color:#800020; font-size:1.15rem; margin:10px 0 2px; font-weight:700; }}
.price-tag {{ color:#FF6600; font-weight:800; font-size:1.35rem; }}
.cat-badge {{ display:inline-block; background:#FF9933; color:white; font-size:0.75rem; font-weight:700; border-radius:20px; padding:3px 15px; margin-bottom:5px; }}
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

# ── LOGIN ──
if not st.session_state["logged_in"]:
    chef_t = f'<img src="{CHEF_B64}" style="width:120px;height:120px;border-radius:50%;border:4px solid #FF9933;object-fit:cover;">' if CHEF_B64 else "🍛"
    st.markdown(f'<div style="background:linear-gradient(135deg,#FF9933 0%,#FFFFFF 50%,#138808 100%); padding:100px 0; min-height:95vh;"><div style="background:white; border-radius:30px; padding:60px 40px; max-width:440px; margin:0 auto; box-shadow:0 30px 60px rgba(0,0,0,0.3); text-align:center;">{chef_t}<h1 style="color:#800020; margin-top:20px; font-size:2.5rem;">Welcome</h1><p style="font-weight:700; color:#555; font-size:1.1rem;">South Indian Food Order App</p><p style="font-size:0.8rem; color:#888; margin-top:30px;">copyright@Bhadradri Technologies.Inc</p></div></div>', unsafe_allow_html=True)
    _, login_col, _ = st.columns([1,1.2,1])
    with login_col:
        with st.form("login_form"):
            usr = st.text_input("Username")
            pwd = st.text_input("Password", type="password")
            if st.form_submit_button("LOGIN", use_container_width=True):
                if usr.strip() and pwd == "Admin123":
                    st.session_state["logged_in"] = True
                    st.session_state["username"] = usr.strip()
                    st.rerun()
                else: st.error("Wrong Credentials!")
    st.stop()

# ── HEADER & BANNER ──
banner_icon = f'<img src="{BHADRADRI_B64}" class="banner-icon">' if BHADRADRI_B64 else ""
st.markdown(f'<div class="top-banner">{banner_icon}<div class="marquee-box"><p class="banner-text">This project @ designed by Bhadradri Technologies.Inc</p></div></div>', unsafe_allow_html=True)

logo_img = f'<img src="{LOGIN_FOOD_B64}" class="header-logo">' if LOGIN_FOOD_B64 else ""
sun_icon = f'<img src="{SUNRISE_B64}" style="width:55px;height:55px;vertical-align:middle;margin-left:15px;">' if SUNRISE_B64 else ""
st.markdown(f'<div class="app-header"><div style="display:flex;align-items:center;">{logo_img}<h1 class="header-title">South Indian Food {sun_icon}</h1></div><div style="color:white; font-weight:700; font-size:1.2rem;">Hi, {st.session_state["username"]}</div></div>', unsafe_allow_html=True)

# ── PAYMENT GATEWAY ──
if st.session_state["show_payment"]:
    st.markdown('<div class="payment-overlay">', unsafe_allow_html=True)
    st.markdown('<h2 style="color:#800020; text-align:center; border-bottom:3px solid #FF9933; padding-bottom:10px;">🛡️ Secure Checkout</h2>', unsafe_allow_html=True)
    p1, p2 = st.columns([1.2, 1])
    order_total = sum(it['price']*it['qty'] for it in st.session_state["cart"].values())
    with p1:
        st.markdown("### 📋 Order Summary")
        for iid, item in st.session_state["cart"].items():
            st.markdown(f"• **{item['name']}** x {item['qty']} <span style='float:right;'>₹{item['price']*item['qty']}</span>", unsafe_allow_html=True)
        st.markdown(f"<div style='border-top:2px solid #FF9933; margin-top:10px; padding-top:10px; font-size:1.8rem; font-weight:800; color:#FF6600;'>Total: ₹{order_total}</div>", unsafe_allow_html=True)
    with p2:
        qr_bytes = generate_upi_qr(f"upi://pay?pa=merchant@upi&pn=Food&am={order_total}&cu=INR")
        st.markdown('<div style="background:white; padding:15px; border-radius:15px; text-align:center;">', unsafe_allow_html=True)
        st.image(qr_bytes, width=200, caption="Scan to Pay")
        st.markdown(f"**VPA:** `merchant@upi`</div>", unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    cl1, cl2 = st.columns(2)
    with cl1:
        if st.button("❌ CANCEL", use_container_width=True): st.session_state["show_payment"] = False; st.rerun()
    with cl2:
        if st.button("✅ I HAVE PAID", type="primary", use_container_width=True):
            st.balloons(); st.success("Verified!"); st.session_state["cart"] = {}; st.session_state["show_payment"] = False; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ── ACTIONS ──
btn1, btn2, btn3, btn4 = st.columns([1,1,3,1])
with btn1:
    if st.button("🔐 Admin", use_container_width=True): st.session_state["admin_mode"] = not st.session_state["admin_mode"]
with btn2:
    sh_toggle = st.toggle("🎬 Showcase", False)
with btn4:
    if st.button("Logout 🚪", use_container_width=True): st.session_state["logged_in"] = False; st.rerun()

if sh_toggle:
    if SHOWCASE_VIDEO.exists(): st.video(str(SHOWCASE_VIDEO))
    else: st.warning("Video missing")

if st.session_state["admin_mode"]:
    adm_pw = st.text_input("Admin Password", type="password")
    if adm_pw == "sriram123":
        with st.form("add_food"):
            n = st.text_input("Name"); p = st.number_input("Price", 1); c = st.selectbox("Category", ["Breakfast", "Snacks", "Lunch", "Beverages"]); h = st.checkbox("Hot", True)
            if st.form_submit_button("Add Item"):
                st.session_state["menu"].append({"id": len(st.session_state["menu"])+1, "name":n.upper(), "price":p, "category":c, "hot":h}); st.rerun()

# ── MENU ──
st.markdown('<h2 style="color:#800020; border-bottom:3px solid #FF9933; margin-top:20px; padding-bottom:10px;">🍽️ Delicious Menu</h2>', unsafe_allow_html=True)
mcols = st.columns(4)
for i, item in enumerate(st.session_state["menu"]):
    with mcols[i % 4]:
        img_src = get_food_img(item["name"])
        img_tag = f'<img src="{img_src}" class="card-img">' if img_src else "🍛"
        smoke_eff = SMOKE_SVG if item.get("hot") else ""
        st.markdown(f'<div class="food-card"><div class="img-wrap">{img_tag}{smoke_eff}</div><h3>{item["name"]}</h3><div class="cat-badge">{item["category"]}</div><div class="price-tag">₹{item["price"]}</div></div>', unsafe_allow_html=True)
        if st.button(f"Add 🛒", key=f"add_{item['id']}", use_container_width=True):
            iid = str(item["id"])
            if iid in st.session_state["cart"]: st.session_state["cart"][iid]["qty"] += 1
            else: st.session_state["cart"][iid] = {"name":item["name"], "price":item["price"], "qty": 1}
            st.toast(f"Added {item['name']}! 🛒")

# ── SIDEBAR CART ──
with st.sidebar:
    st.title("🛒 Your Order")
    if not st.session_state["cart"]: st.info("Cart is empty")
    else:
        tot = 0
        for iid, it in st.session_state["cart"].items():
            sub = it['price']*it['qty']; tot += sub; st.write(f"**{it['name']}** x {it['qty']} - ₹{sub}")
        st.markdown(f"### Pay: ₹{tot}")
        if st.button("Confirm Order 🍛", type="primary", use_container_width=True):
            st.session_state["show_payment"] = True; st.rerun()

# ── BOT LOGIC ──
def get_bot_reply(msg):
    m = msg.lower()
    menu = st.session_state["menu"]
    if any(k in m for k in ["hi", "hello", "hey"]): return "Hello! 👋 I'm your food assistant. How can I help you?"
    if any(k in m for k in ["breakfast", "morning"]): 
        items = [i["name"] for i in menu if i["category"]=="Breakfast"]
        return f"🌅 Morning! Specials: {', '.join(items)}. Dosa is the best! 😊"
    if any(k in m for k in ["price", "cost"]): return "💰 Prices: ₹10 to ₹50. Very affordable!"
    if any(k in m for k in ["recommend", "best"]): return "🌟 You must try our Dosa and Idly!"
    return "I'm here to help! 🍛 Ask me about the menu, prices, or recommendations."

# ── THE ONLY FLOATING BOT (Popover Implementation) ──
# This combines the float, the Mascot, and the chat into ONE system.
st.markdown('<div class="chatbot-fixed-wrap">', unsafe_allow_html=True)

# The static greeting bubble
now_h = datetime.now().hour
txt_grt = "Good Morning" if now_h < 12 else "Good Afternoon" if now_h < 18 else "Good Evening"
st.markdown(f'<div class="bot-greeting-bubble">{txt_grt}! 👋 I\'m your food assistant. What would you like to eat today?</div>', unsafe_allow_html=True)

# The Mascot as a Popover Button
chef_img_html = f'<img src="{CHEF_B64}" class="chef-float-img">' if CHEF_B64 else "👩‍🍳"
with st.popover(chef_img_html):
    st.markdown('<h3 style="color:#800020; text-align:center;">👩‍🍳 Help Bot</h3>', unsafe_allow_html=True)
    
    # Message History inside popover
    for ms in st.session_state["messages"]:
        with st.chat_message(ms["role"]): st.markdown(ms["content"])
    
    # Chat Logic inside popover
    if prompt := st.chat_input("Ask a question..."):
        st.session_state["messages"].append({"role": "user", "content": prompt})
        # Logic is processed after rerun by session state
        reply = get_bot_reply(prompt)
        st.session_state["messages"].append({"role": "assistant", "content": reply})
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

st.caption("Bhadradri Technologies.Inc © 2025")
