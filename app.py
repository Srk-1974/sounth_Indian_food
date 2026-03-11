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

# Pre-load Assets
BHADRADRI_B64    = img_b64(ASSETS / "bhadradri-icon-small.png")
LOGO_B64         = img_b64(ASSETS / "logo.png")
CHEF_B64         = img_b64(ASSETS / "south-indian-chef.png")
SUNRISE_B64      = img_b64(ASSETS / "sunrise-icon.png")
CHAT_BOT_B64     = img_b64(ASSETS / "chatbot-icon.png")
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

/* === CHATBOT BUBBLE (Matches React Copy) === */
.chatbot-float {{
    position: fixed; bottom: 30px; right: 30px; z-index: 10000;
    display: flex; flex-direction: column; align-items: center; gap: 8px;
}}
.chat-tooltip {{
    background: white; padding: 12px 18px; border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2); font-size: 0.85rem;
    color: #333; width: 220px; text-align: center; position: relative;
    border: 1px solid #ddd; animation: fadeIn 0.4s ease-out;
}}
.chat-tooltip::after {{
    content: ''; position: absolute; bottom: -8px; right: 25px;
    width: 0; height: 0; border-left: 8px solid transparent;
    border-right: 8px solid transparent; border-top: 8px solid white;
}}
.bot-avatar-wrap {{ position: relative; }}
.bot-img-main {{
    width: 75px; height: 75px; border-radius: 50%; border: 3px solid white;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3); background: white;
    animation: bounceBot 2s infinite ease-in-out;
}}
.cart-badge-bot {{
    position: absolute; top: -2px; right: -2px;
    background: #138808; color: white; border-radius: 50%;
    width: 25px; height: 25px; display: flex; align-items: center;
    justify-content: center; font-size: 0.8rem; font-weight: 700;
    border: 2px solid white; box-shadow: 0 2px 5px rgba(0,0,0,0.3);
}}
@keyframes bounceBot {{ 0%, 100% {{ transform:translateY(0); }} 50% {{ transform:translateY(-10px); }} }}
@keyframes fadeIn {{ from {{ opacity:0; transform:translateY(10px); }} to {{ opacity:1; transform:translateY(0); }} }}

/* Payment Card Overlay Styling */
.payment-overlay {{
    background:#fff3e0; padding:30px; border-radius:24px; 
    border:4px solid #FF9933; margin:20px 0;
    box-shadow: 0 15px 40px rgba(0,0,0,0.15);
}}

/* Food Card Details */
.food-card h3 {{ color:#800020; font-size:1.15rem; margin:10px 0 2px; font-weight:700; }}
.price-tag {{ color:#FF6600; font-weight:800; font-size:1.3rem; }}
.cat-badge {{ display:inline-block; background:#FF9933; color:white; font-size:0.75rem; font-weight:700; border-radius:20px; padding:3px 15px; margin-bottom:5px; }}
</style>
""", unsafe_allow_html=True)

# ── Session State ─────────────────────────────────────────────────────────────
if "logged_in" not in st.session_state: st.session_state["logged_in"] = False
if "username" not in st.session_state: st.session_state["username"] = ""
if "cart" not in st.session_state: st.session_state["cart"] = {}
if "admin_mode" not in st.session_state: st.session_state["admin_mode"] = False
if "show_payment" not in st.session_state: st.session_state["show_payment"] = False
if "chat_open" not in st.session_state: st.session_state["chat_open"] = False
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

# ── APP HEADER & BANNER ──
banner_icon = f'<img src="{BHADRADRI_B64}" class="banner-icon">' if BHADRADRI_B64 else ""
st.markdown(f'<div class="top-banner">{banner_icon}<div class="marquee-box"><p class="banner-text">This project @ designed by Bhadradri Technologies.Inc</p></div></div>', unsafe_allow_html=True)

logo_img = f'<img src="{LOGIN_FOOD_B64}" class="header-logo">' if LOGIN_FOOD_B64 else ""
sun_icon = f'<img src="{SUNRISE_B64}" style="width:55px;height:55px;vertical-align:middle;margin-left:15px;">' if SUNRISE_B64 else ""
st.markdown(f'<div class="app-header"><div style="display:flex;align-items:center;">{logo_img}<h1 class="header-title">South Indian Food {sun_icon}</h1></div><div style="color:white; font-weight:700; font-size:1.2rem;">Hi, {st.session_state["username"]}</div></div>', unsafe_allow_html=True)

# ── PAYMENT GATEWAY (STUCK AT TOP WHEN ACTIVE) ──
if st.session_state["show_payment"]:
    st.markdown('<div class="payment-overlay">', unsafe_allow_html=True)
    st.markdown('<h2 style="color:#800020; text-align:center; border-bottom:3px solid #FF9933; padding-bottom:10px;">🛡️ Secure Checkout</h2>', unsafe_allow_html=True)
    
    pay1, pay2 = st.columns([1.2, 1])
    order_total = sum(it['price']*it['qty'] for it in st.session_state["cart"].values())
    
    with pay1:
        st.markdown("### 📋 Order Summary")
        for iid, item in st.session_state["cart"].items():
            st.markdown(f"• **{item['name']}** x {item['qty']} <span style='float:right;'>₹{item['price']*item['qty']}</span>", unsafe_allow_html=True)
        st.markdown(f"<div style='border-top:2px solid #FF9933; margin-top:10px; padding-top:10px; font-size:1.8rem; font-weight:800; color:#FF6600;'>Total: ₹{order_total}</div>", unsafe_allow_html=True)
        
    with pay2:
        upi_link = f"upi://pay?pa=merchant@upi&pn=SouthIndianDelights&am={order_total}&cu=INR"
        qr_bytes = generate_upi_qr(upi_link)
        st.markdown('<div style="background:white; padding:15px; border-radius:15px; text-align:center; box-shadow:0 4px 10px rgba(0,0,0,0.1);">', unsafe_allow_html=True)
        st.image(qr_bytes, width=200, caption="Scan with GPay / PhonePe / Paytm")
        st.markdown(f"**VPA:** `merchant@upi`</div>", unsafe_allow_html=True)
        
    st.markdown('<br>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("❌ ABORT PAYMENT", use_container_width=True): st.session_state["show_payment"] = False; st.rerun()
    with c2:
        if st.button("✅ I HAVE TRANSFERRED ₹" + str(order_total), type="primary", use_container_width=True):
            st.balloons(); st.success("Transaction Confirmed!"); st.session_state["cart"] = {}; st.session_state["show_payment"] = False; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ── TOP ACTION BUTTONS ──
btn1, btn2, btn3, btn4 = st.columns([1,1,3,1])
with btn1:
    if st.button("🔐 Admin", use_container_width=True): st.session_state["admin_mode"] = not st.session_state["admin_mode"]
with btn2:
    sh_toggle = st.toggle("🎬 Showcase", False)
with btn4:
    if st.button("Logout 🚪", use_container_width=True): st.session_state["logged_in"] = False; st.rerun()

if sh_toggle:
    if SHOWCASE_VIDEO.exists(): st.video(str(SHOWCASE_VIDEO))
    else: st.warning("Showcase video missing.")

if st.session_state["admin_mode"]:
    admin_pw = st.text_input("Enter Admin Password", type="password")
    if admin_pw == "sriram123":
        st.success("Admin Dashboard Active")
        with st.form("admin_add"):
            n = st.text_input("Name"); p = st.number_input("Price", 1); c = st.selectbox("Category", ["Breakfast", "Snacks", "Lunch", "Beverages"]); h = st.checkbox("Hot", True)
            if st.form_submit_button("Add Item"):
                st.session_state["menu"].append({"id": len(st.session_state["menu"])+1, "name":n.upper(), "price":p, "category":c, "hot":h}); st.rerun()

# ── MENU GRID ──
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
    st.title("🛒 Your Selected Items")
    if not st.session_state["cart"]: st.info("Cart is empty. Please select food!")
    else:
        cart_total = 0
        for iid, itm in st.session_state["cart"].items():
            sub = itm['price']*itm['qty']; cart_total += sub; st.write(f"**{itm['name']}** x {itm['qty']} - ₹{sub}")
        st.markdown(f"### Pay: ₹{cart_total}")
        if st.button("Confirm Order 🍛", type="primary", use_container_width=True):
            st.session_state["show_payment"] = True; st.rerun()

# ── HELP CHATBOT logic ──
def get_bot_reply(msg):
    m = msg.lower()
    menu = st.session_state["menu"]
    if any(k in m for k in ["hi", "hello", "hey"]): return "Hello! 👋 I'm your South Indian Food assistant. I can help you with menu items, prices, and recommendations. What's on your mind?"
    if any(k in m for k in ["breakfast", "morning"]): 
        items = [i["name"] for i in menu if i["category"]=="Breakfast"]
        return f"🌅 Our breakfast specials are: {', '.join(items)}. The DOSA is a fan favorite!"
    if any(k in m for k in ["price", "cost", "how much"]): 
        cheapest = min(menu, key=lambda x: x["price"])
        return f"💰 Our prices are very affordable! They range from ₹10 to ₹50. Items like {cheapest['name']} are only ₹{cheapest['price']}."
    if any(k in m for k in ["best", "popular", "recommend"]): return "🌟 I highly recommend the **DOSA** and **POORI**! For snacks, the **VADA** is perfectly crispy outside and soft inside."
    if any(k in m for k in ["bye", "thanks", "thank you"]): return "You're welcome! Enjoy your delicious meal! 😊🍛"
    return "I'm here to help! 🍛 Ask me about breakfast, snacks, popular items, or prices."

# ── FLOATING CHATBOT CONTROLS ──
# We use a single button to toggle the chat since HTML can't trigger Streamlit state
if st.button("🗨️ Open Help Assistant", type="secondary", icon="🤖"):
    st.session_state["chat_open"] = not st.session_state["chat_open"]

# The Floating Visual (Matches local React Copy)
hr = datetime.now().hour
grt = "Good Morning" if hr < 12 else "Good Afternoon" if hr < 18 else "Good Evening"
c_qty = sum(i["qty"] for i in st.session_state["cart"].values())
c_badge = f'<div class="cart-badge-bot">{c_qty}</div>' if c_qty > 0 else ""
bot_img_src = f'<img src="{CHAT_BOT_B64}" class="bot-img-main">' if CHAT_BOT_B64 else "🤖"

# SINGLE LINE HTML to avoid </div> rendering bugs
chat_viz_html = f'<div class="chatbot-float"><div class="chat-tooltip">{grt}! 👋 I\'m your food assistant. What would you like to eat today?</div><div class="bot-avatar-wrap">{bot_img_src}{c_badge}</div></div>'
st.markdown(chat_viz_html, unsafe_allow_html=True)

# THE CHAT INTERFACE (Controlled by st.session_state["chat_open"])
if st.session_state["chat_open"]:
    st.markdown("---")
    st.subheader("🗨️ Food Assistant Chat")
    
    # Custom CSS to make this section look like a floating chat window
    st.markdown("""<style>.chat-window { background: white; border: 2px solid #FF9933; border-radius: 20px; padding: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }</style>""", unsafe_allow_html=True)
    
    chat_container = st.container(height=350, border=True)
    with chat_container:
        for m in st.session_state["messages"]:
            with st.chat_message(m["role"]): st.markdown(m["content"])
    
    if user_input := st.chat_input("Ask me about the food..."):
        st.session_state["messages"].append({"role": "user", "content": user_input})
        with chat_container.chat_message("user"): st.markdown(user_input)
        
        reply = get_bot_reply(user_input)
        st.session_state["messages"].append({"role": "assistant", "content": reply})
        with chat_container.chat_message("assistant"): st.markdown(reply)
        st.rerun()

st.caption("Bhadradri Technologies.Inc © 2025")
