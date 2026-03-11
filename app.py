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

# ── Image loader ──────────────────────────────────────────────────────────────
ASSETS = Path("public/assets")

def img_b64(path: Path) -> str:
    if path.exists():
        ext = path.suffix.lstrip(".").lower()
        ext = "jpeg" if ext in ("jpg", "jpeg") else ext
        encoded = base64.b64encode(path.read_bytes()).decode()
        return f"data:image/{ext};base64,{encoded}"
    return ""

# Pre-load all required assets
BHADRADRI_B64  = img_b64(ASSETS / "bhadradri-icon-small.png")
LOGIN_FOOD_B64 = img_b64(ASSETS / "login-food.png")
CHEF_B64       = img_b64(ASSETS / "south-indian-chef.png")
SUNRISE_B64    = img_b64(ASSETS / "sunrise-icon.png")

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
    # Default fallback to stock food images
    for stock in ["stock-1.png", "stock-2.png", "stock-food-1.jpg"]:
        p = ASSETS / stock
        if p.exists():
            return img_b64(p)
    return ""

# ── Compact Animation HTML ────────────────────────────────────────────────────
# Minified to prevent Streamlit from interpreting it as a Markdown code block
SMOKE_TAGS = '<div class="smoke-wrap"><div class="smokey s1"></div><div class="smokey s2"></div><div class="smokey s3"></div><div class="smokey s4"></div><div class="smokey s5"></div></div>'

# ── Global Styles & Keyframes ─────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Poppins:wght@300;400;600;700&display=swap');
html, body, [class*="css"] {{ font-family: 'Poppins', sans-serif; }}

/* === MARQUEE BANNER === */
.top-banner {{
    width:100%; background:blueviolet; padding:8px 12px;
    display:flex; align-items:center; gap:12px;
    border-radius:10px; margin-bottom:15px; overflow:hidden;
    position: relative;
}}
.banner-icon {{
    width:24px; height:24px; object-fit:contain;
    background:white; border-radius:50%; padding:2px; flex-shrink:0;
    z-index: 2;
}}
.marquee-container {{
    flex: 1; overflow: hidden; white-space: nowrap;
}}
.banner-text {{
    display: inline-block; font-size: 0.85rem; color: white;
    font-weight: 600; font-style: italic; margin: 0;
    animation: marqueeScroll 20s linear infinite;
}}
@keyframes marqueeScroll {{
    0%   {{ transform: translateX(100%); }}
    100% {{ transform: translateX(-100%); }}
}}

/* === HEADER === */
.app-header {{
    background:linear-gradient(135deg,#FF9933 0%,#FF7700 100%);
    padding:16px 28px; border-radius:16px;
    display:flex; align-items:center; justify-content:space-between;
    margin-bottom:20px; box-shadow:0 6px 24px rgba(255,102,0,0.3);
}}
.header-title {{
    font-family:'Great Vibes', cursive; font-size:3.5rem; color:#800020;
    text-shadow:2px 2px 0 #fff, 0 4px 15px rgba(0,0,0,0.15); margin:0;
    display:flex; align-items:center; gap:12px;
}}
.header-user {{ color:white; font-size:1.1rem; font-weight:700; text-align:right; }}

/* === LOGIN PAGE === */
.login-page {{
    background:linear-gradient(135deg,#FF9933 0%,#FFFFFF 50%,#138808 100%);
    padding:60px 0; border-radius:16px; min-height: 80vh;
}}
.login-card {{
    background:white; border-radius:24px; padding:45px 35px;
    max-width:400px; margin:0 auto;
    box-shadow:0 25px 50px rgba(0,0,0,0.2); text-align:center;
}}
.login-card h2 {{ color:#FF9933; font-weight:800; font-size:1.6rem; margin:15px 0 5px; }}
.lc-copy {{
    font-size:0.85rem; font-style:italic; font-weight:700; margin-bottom:25px;
    background:linear-gradient(to right,#FF9933,#000080,#138808);
    -webkit-background-clip:text; background-clip:text; color:transparent;
}}

/* === FOOD CARDS === */
.food-card {{
    background:white; border:2px solid #FF9933; border-radius:18px; 
    padding:0 0 15px 0; overflow:hidden; text-align:center;
    box-shadow:0 5px 20px rgba(0,0,0,0.08);
    transition:transform 0.3s; margin-bottom:12px; 
    height: 100%; display: flex; flex-direction: column;
}}
.food-card:hover {{ transform:translateY(-6px); border-color: #FF5500; }}
.img-wrap {{ position:relative; width:100%; height:170px; overflow:hidden; }}
.card-img {{ width:100%; height:100%; object-fit:cover; }}

/* === SMOKE EFFECT === */
.smoke-wrap {{
    position:absolute; bottom:5px; left:50%; transform:translateX(-50%);
    width:100px; height:80px; pointer-events:none; z-index:5;
}}
.smokey {{
    position:absolute; bottom:0; width:35px; height:35px;
    background:radial-gradient(circle, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0) 75%);
    border-radius:50%; opacity:0; filter:blur(5px);
    animation:denseSmoke 2.5s infinite ease-out;
}}
.s1 {{ left:20%; animation-delay:0s; }}
.s2 {{ left:35%; animation-delay:0.5s; }}
.s3 {{ left:50%; animation-delay:1.0s; }}
.s4 {{ left:65%; animation-delay:1.5s; }}
.s5 {{ left:40%; animation-delay:2.0s; }}

@keyframes denseSmoke {{
    0%   {{ transform:translateY(0) scale(1); opacity:0; }}
    15%  {{ opacity:0.9; }}
    100% {{ transform:translateY(-90px) scale(4); opacity:0; }}
}}

/* === CARD CONTENT === */
.food-card h3 {{ color:#800020; font-size:1.1rem; margin:12px 0 5px; font-weight:700; }}
.price-tag {{ color:#FF6600; font-weight:800; font-size:1.3rem; margin:5px 0; }}
.cat-badge {{
    display:inline-block; background:#FF9933; color:white;
    font-size:0.75rem; font-weight:700; border-radius:20px;
    padding:3px 12px; margin-bottom:8px;
}}
</style>
""", unsafe_allow_html=True)

# ── Data & Logic ──────────────────────────────────────────────────────────────
DEFAULT_MENU = [
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

if "logged_in" not in st.session_state: st.session_state["logged_in"] = False
if "username" not in st.session_state: st.session_state["username"] = ""
if "menu_items" not in st.session_state: st.session_state["menu_items"] = list(DEFAULT_MENU)
if "cart" not in st.session_state: st.session_state["cart"] = {}
if "admin_unlocked" not in st.session_state: st.session_state["admin_unlocked"] = False

LOGIN_PW = "Admin123"
ADMIN_PW = "sriram123"

# ─────────────────────────────────────────────────────────────────────────────
# PAGE ROUTING
# ─────────────────────────────────────────────────────────────────────────────

if not st.session_state["logged_in"]:
    chef_tag = f'<img src="{CHEF_B64}" style="width:110px;height:110px;border-radius:50%;border:4px solid #FF9933;object-fit:cover;">' if CHEF_B64 else "🍛"
    st.markdown(f"""
        <div class="login-page"><div class="login-card">
        {chef_tag}
        <h2>Welcome to South Indian Food App</h2>
        <p class="lc-copy">copyright@Bhadradri Technologies.Inc</p>
        <p style="font-weight:700;color:#555;">Login to South Indian Food</p>
        </div></div>""", unsafe_allow_html=True)
    
    _, col2, _ = st.columns([1,1.2,1])
    with col2:
        with st.form("login"):
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.form_submit_button("LOGIN", use_container_width=True):
                if u.strip() and p == LOGIN_PW:
                    st.session_state["logged_in"] = True
                    st.session_state["username"] = u.strip()
                    st.rerun()
                else: st.error("Invalid credentials (PW: Admin123)")
    st.stop()

# ── TOP BANNER ──
icon_html = f'<img src="{BHADRADRI_B64}" class="banner-icon">' if BHADRADRI_B64 else ""
st.markdown(f'<div class="top-banner">{icon_html}<div class="marquee-container"><p class="banner-text">This project @ designed by Bhadradri Technologies.Inc</p></div></div>', unsafe_allow_html=True)

# ── HEADER ──
logo_html = f'<img src="{LOGIN_FOOD_B64}" style="width:70px;height:70px;border-radius:50%;border:4px solid white;object-fit:cover;">' if LOGIN_FOOD_B64 else ""
sun_html  = f'<img src="{SUNRISE_B64}" style="width:48px;height:48px;vertical-align:middle;margin-left:10px;">' if SUNRISE_B64 else ""
st.markdown(f'<div class="app-header"><div style="display:flex;align-items:center;">{logo_html}<h1 class="header-title">South Indian Food {sun_html}</h1></div><div class="header-user">Hello, {st.session_state["username"]}</div></div>', unsafe_allow_html=True)

if st.button("Logout 🚪"):
    st.session_state["logged_in"] = False
    st.rerun()

st.markdown("---")

# ── MAIN CONTENT ──
with st.sidebar:
    st.title("🛒 Your Cart")
    if not st.session_state["cart"]: st.info("Cart is empty")
    else:
        for iid, it in list(st.session_state["cart"].items()):
            st.write(f"**{it['name']}** x {it['qty']} - ₹{it['price']*it['qty']}")
        if st.button("Checkout ✅", type="primary"):
            st.balloons(); st.session_state["cart"] = {}; st.rerun()

st.markdown('<h2 style="color:#800020;">🍽️ Fresh Menu</h2>', unsafe_allow_html=True)

items = st.session_state["menu_items"]
cols = st.columns(4)
for i, item in enumerate(items):
    with cols[i % 4]:
        img_src = get_food_img(item["name"])
        img_html = f'<img src="{img_src}" class="card-img">' if img_src else "🍛"
        smoke_html = SMOKE_TAGS if item.get("hot") else ""
        
        # Minified Card Construction
        card_html = (
            f'<div class="food-card"><div class="img-wrap">{img_html}{smoke_html}</div>'
            f'<h3>{item["name"]}</h3>'
            f'<div class="cat-badge">{item["category"]}</div>'
            f'<div class="price-tag">₹{item["price"]}</div>'
            f'<p style="font-size:0.75rem;color:#777;">{"🔥 Hot" if item["hot"] else "❄️ Cold"}</p></div>'
        )
        st.markdown(card_html, unsafe_allow_html=True)
        
        if st.button(f"Add 🛒", key=f"btn_{item['id']}", use_container_width=True):
            iid = item["id"]
            if iid in st.session_state["cart"]: st.session_state["cart"][iid]["qty"] += 1
            else: st.session_state["cart"][iid] = {"name":item["name"], "price":item["price"], "qty":1}
            st.rerun()
