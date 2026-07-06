import streamlit as st
import random

# Page configuration for a true gaming feel
st.set_page_config(page_title="Cyber Trader RPG", page_icon="💰", layout="wide")

# --- PREMIUM DARK MODE & NEON UI (CSS) ---
st.markdown("""
<style>
    /* တစ်ဝက်ဘ်ဆိုက်လုံးကို Dark Mode ပြောင်းခြင်း */
    .stApp {
        background-color: #0B0C10;
        color: #C5C6C7;
    }
    
    /* စာသားခေါင်းစဉ်ကြီးများ */
    h1, h2, h3, h4 {
        color: #66FCF1 !important;
        font-family: 'Courier New', Courier, monospace;
        text-shadow: 0 0 10px rgba(102, 252, 241, 0.3);
    }
    
    /* Stat Boxes များကို ပိုမိုစမတ်ကျစေရန် */
    .stat-box {
        background: #1F2833;
        color: #fff;
        padding: 12px;
        border-radius: 12px;
        text-align: center;
        font-weight: bold;
        border: 1px solid #45A29E;
        box-shadow: 0 4px 15px rgba(102, 252, 241, 0.1);
    }
    
    /* ကစားကွင်းကတ်ပြားများကို Neon ပုံစံပြောင်းခြင်း */
    .game-card {
        background-color: #1F2833;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #45A29E;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
        margin-bottom: 15px;
    }
    
    /* ခလုတ်များကို လှပဆွဲမက်ဖွယ် ပြောင်းလဲခြင်း */
    .stButton>button {
        background: linear-gradient(135deg, #45A29E 0%, #1F2833 100%);
        color: #66FCF1 !important;
        border: 1px solid #66FCF1 !important;
        border-radius: 10px;
        padding: 0.6rem 1.2rem;
        font-weight: bold;
        width: 100%;
        transition: 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #66FCF1 0%, #45A29E 100%);
        color: #0B0C10 !important;
        box-shadow: 0 0 15px #66FCF1;
        transform: scale(1.02);
    }
    
    /* တုန်ခါခြင်း လှုပ်ရှားမှု */
    @keyframes shake {
        0% { transform: translate(1px, 1px) rotate(0deg); }
        20% { transform: translate(-3px, 0px) rotate(1deg); }
        40% { transform: translate(1px, -1px) rotate(1deg); }
        60% { transform: translate(-3px, 1px) rotate(0deg); }
        80% { transform: translate(-1px, -1px) rotate(1deg); }
        100% { transform: translate(1px, -2px) rotate(-1deg); }
    }
    .shake-effect { animation: shake 0.4s; }
</style>
""", unsafe_allow_html=True)

# --- SOUND & EFFECT TRIGGER ---
def play_effect(sound_type, trigger_confetti=False):
    sound_urls = {
        "click": "https://assets.mixkit.co/active_storage/sfx/2568/2568-84.wav",
        "hit": "https://assets.mixkit.co/active_storage/sfx/2763/2763-84.wav",
        "win": "https://assets.mixkit.co/active_storage/sfx/1435/1435-84.wav",
        "lose": "https://assets.mixkit.co/active_storage/sfx/2622/2622-84.wav",
        "trade": "https://assets.mixkit.co/active_storage/sfx/2019/2019-84.wav"
    }
    confetti = "<script src='https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js'></script><script>confetti({particleCount:120, spread:70, colors:['#66FCF1','#45A29E','#ffffff']});</script>" if trigger_confetti else ""
    if sound_type in sound_urls:
        st.components.v1.html(f"{confetti}<audio autoplay><source src='{sound_urls[sound_type]}' type='audio/wav'></audio>", height=0, width=0)

# --- GAME SYSTEM STATE ---
if 'level' not in st.session_state: st.session_state.level = 1
if 'exp' not in st.session_state: st.session_state.exp = 0
if 'coin' not in st.session_state: st.session_state.coin = 1000
if 'gold' not in st.session_state: st.session_state.gold = 1
if 'silver' not in st.session_state: st.session_state.silver = 10
if 'hp' not in st.session_state: st.session_state.hp = 100
if 'inventory_bag' not in st.session_state: 
    st.session_state.inventory_bag = {"အိတ်": 1, "ဖိနပ်": 1, "အလှကုန်": 1, "ဖုန်း/အီလက်ထရွန်နစ်": 0, "ရွှေထည်ရတနာ": 0, "ထိုင်းစားသောက်ကုန်": 2}
if 'log' not in st.session_state: st.session_state.log = ["🛸 Premium Cyberpunk စျေးကွက်ထဲသို့ ရောက်ရှိလာပါပြီ။"]
if 'battle_frame' not in st.session_state: st.session_state.battle_frame = ""

def add_log(text):
    st.session_state.log.insert(0, text)
    if len(st.session_state.log) > 4: st.session_state.log.pop()

def lose_exp(amount):
    st.session_state.exp -= amount
    if st.session_state.exp < 0:
        if st.session_state.level > 1:
            st.session_state.level -= 1
            st.session_state.exp = 70
            add_log(f"📉 လုပ်ငန်းနာမည်ပျက်၍ အဆင့် Level {st.session_state.level} သို့ ကျဆင်းသွားသည်။")
        else: st.session_state.exp = 0

def gain_exp(amount):
    st.session_state.exp += amount
    if st.session_state.exp >= (st.session_state.level * 100):
        st.session_state.level += 1
        st.session_state.exp = 0
        add_log(f"✨ ရာထူးတက်လှမ်းမှု- သင်သည် အဆင့် Level {st.session_state.level} ကုန်သည်ကြီး ဖြစ်လာပြီ။")
        play_effect("win", trigger_confetti=True)

# --- MARKET ECONOMY ---
base_prices = {"အိတ်": 150, "ဖိနပ်": 100, "အလှကုန်": 80, "ဖုန်း/အီလက်ထရွန်နစ်": 800, "ရွှေထည်ရတနာ": 1500, "ထိုင်းစားသောက်ကုန်": 40}
market_trend = random.choice(["💥 စျေးကွက်ပျက်နေသည်", "📈 ကုန်သွယ်မှု အထူးကောင်းမွန်နေသည်", "⚖️ စျေးကွက် တည်ငြိမ်နေသည်"])
price_modifier = random.uniform(0.4, 0.7) if market_trend == "💥 စျေးကွက်ပျက်နေသည်" else random.uniform(1.3, 1.9) if market_trend == "📈 ကုန်သွယ်မှု အထူးကောင်းမွန်နေသည်" else 1.0
current_prices = {item: int(base * price_modifier) for item, base in base_prices.items()}

# --- HEADER ---
st.title("⚡ CYBER TRADER RPG")
st.markdown(f"🌌 **ယနေ့ စျေးကွက်လှိုင်းနှုန်း:** <span style='color:#66FCF1; font-weight:bold;'>{market_trend}</span>", unsafe_allow_html=True)
st.write("---")

# --- STATS BAR ---
col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1: st.markdown(f"<div class='stat-box' style='color:#66FCF1;'>🌟 LEVEL<br><span style='font-size:20px;'>{st.session_state.level}</span></div>", unsafe_allow_html=True)
with col2: st.markdown(f"<div class='stat-box' style='color:#FF4B4B;'>❤️ HP HEALTH<br><span style='font-size:20px;'>{st.session_state.hp}%</span></div>", unsafe_allow_html=True)
with col3: st.markdown(f"<div class='stat-box' style='color:#00F0FF;'>💵 COIN (ဘတ်)<br><span style='font-size:20px;'>{st.session_state.coin} ฿</span></div>", unsafe_allow_html=True)
with col4: st.markdown(f"<div class='stat-box' style='color:#FFD700;'>🟡 GOLD BAR<br><span style='font-size:20px;'>{st.session_state.gold}</span></div>", unsafe_allow_html=True)
with col5: st.markdown(f"<div class='stat-box' style='color:#C0C0C0;'>⚪ SILVER<br><span style='font-size:20px;'>{st.session_state.silver}</span></div>", unsafe_allow_html=True)
with col6: 
    inv_text = " | ".join([f"{k}:{v}" for k, v in st.session_state.inventory_bag.items() if v > 0])
    st.markdown(f"<div class='stat-box' style='color:#00FF00; font-size:11px;'>🎒 Warehouse Storage<br><span>{inv_text if inv_text else 'ဗလာဖြစ်နေသည်'}</span></div>", unsafe_allow_html=True)

st.write("")

if st.session_state.battle_frame:
    st.markdown(st.session_state.battle_frame, unsafe_allow_html=True)
    st.session_state.battle_frame = ""

# --- GAME SCREEN COLUMNS ---
col_act1, col_act2, col_act3 = st.columns(3)

with col_act1:
    st.markdown("<div class='game-card'><h3>📡 စူးစမ်းရှာဖွေခန်း (Scout)</h3><p>နယ်မြေသစ်များကို Router စနစ်ဖြင့် လှမ်းဖတ်ပြီး ကုန်ပစ္စည်းရှာဖွေမည်။</p></div>", unsafe_allow_html=True)
    if st.button("🛰️ စျေးကွက်နယ်မြေသို့ လှမ်းဖတ်ရန်"):
        play_effect("click")
        loot = random.choice(["good", "bad", "nothing"])
        if loot == "good":
            gain_exp(20)
            st.session_state.coin += 120
            add_log("📡 ရှာဖွေရေး အောင်မြင်ပြီး ငွေဒင်္ဂါး ၁၂၀ ฿ အမြတ်ရခဲ့သည်။")
        elif loot == "bad":
            lose_exp(25)
            damage = random.randint(12, 22)
            st.session_state.hp = max(0, st.session_state.hp - damage)
            st.session_state.battle_frame = f"<div class='shake-effect' style='background:#4a1515; padding:12px; border-radius:10px; border:1px solid red; text-align:center;'>🚨 သတိပေးချက်- စျေးကွက်ဆိုက်ဘာတိုက်ခိုက်မှုခံရသဖြင့် HP {damage} လျော့ကျသွားသည်။</div>"
            play_effect("lose")
        else:
            add_log("📡 စူးစမ်းခဲ့သော်လည်း ယခုအလှည့်တွင် ဘာမှမတွေ့ရှိပါ။")
        st.rerun()

with col_act2:
    st.markdown("<div class='game-card'><h3>⚔️ တိုက်ပွဲနယ်မြေ (Combat Zone)</h3><p>ပြိုင်ဘက်ကုမ္ပဏီများနှင့် ထိပ်တိုက်ရင်ဆိုင်ပြီး စျေးကွက်ဝေစု လုယူမည်။</p></div>", unsafe_allow_html=True)
    if st.button("💥 စျေးကွက်လုပွဲ ထိပ်တိုက်ဆင်နွှဲမည်!"):
        play_effect("hit")
        win = random.choice([True, False])
        if win:
            gain_exp(45)
            st.session_state.coin += 350
            st.session_state.battle_frame = "<div style='background: linear-gradient(to right, #114357, #f29492); padding:15px; border-radius:10px; text-align:center;'>✨ CRITICAL WIN! စျေးကွက်စီးပွားရေးစစ်ပွဲတွင် အနိုင်ရရှိသည်။ ✨</div>"
            play_effect("win", trigger_confetti=True)
        else:
            lose_exp(45)
            damage = random.randint(25, 45)
            st.session_state.hp = max(0, st.session_state.hp - damage)
            st.session_state.battle_frame = f"<div class='shake-effect' style='background:#2a0808; padding:15px; border-radius:10px; text-align:center; border:2px solid #ff0000;'>💀 DEFEATED! ပြိုင်ဘက်များ၏ စီးပွားရေးထိုးနှက်ချက် ခံလိုက်ရသည်။ (-{damage} HP)</div>"
            play_effect("lose")
        st.rerun()
        
    if st.session_state.hp < 100:
        if st.button("💉 Nano-Heal ဖြင့် HP ပြန်ဖြည့်မည် (-၁၂၀ ฿)"):
            if st.session_state.coin >= 120:
                st.session_state.coin -= 120
                st.session_state.hp = min(100, st.session_state.hp + 55)
                add_log("💉 နာနိုဆေးထိုးလိုက်သဖြင့် ဒဏ်ရာများ ချက်ချင်းသက်သာလာသည်။ (+၅၅% HP)")
            st.rerun()

with col_act3:
    st.markdown("<div class='game-card'><h3>🏪 ကုန်သွယ်ရေးဂိတ် (Cyber Market)</h3><p>ပစ္စည်းများကို စျေးကွက်ပေါက်စျေးအတိုင်း အရောင်းအဝယ်ပြုလုပ်ရန်။</p></div>", unsafe_allow_html=True)
    selected_item = st.selectbox("အရောင်းအဝယ်လုပ်မည့် ကုန်ပစ္စည်း:", list(current_prices.keys()))
    price = current_prices[selected_item]
    st.markdown(f"💰 **ယခုစျေးနှုန်း:** <span style='color:#66FCF1; font-weight:bold;'>{price} ฿</span> | *(မူရင်းရင်းနှီးစျေး: {base_prices[selected_item]} ฿)*", unsafe_allow_html=True)
    
    cb, cs = st.columns(2)
    with cb:
        if st.button(f"🛒 ဝယ်ယူမည်"):
            if st.session_state.coin >= price:
                st.session_state.coin -= price
                st.session_state.inventory_bag[selected_item] += 1
                add_log(f"🛒 {selected_item} ကို အဝယ်သွင်းလိုက်သည်။")
                play_effect("trade")
            st.rerun()
    with cs:
        if st.session_state.inventory_bag[selected_item] > 0:
            if st.button(f"💵 ပြန်ရောင်းမည်"):
                st.session_state.inventory_bag[selected_item] -= 1
                st.session_state.coin += price
                diff = price - base_prices[selected_item]
                add_log(f"📈 {selected_item} ကို ရောင်းချပြီး အသားတင်အမြတ်/အရှုံး ({diff} ฿) ရရှိသည်။")
                play_effect("trade")
                st.rerun()

# --- HEALTH CRITICAL OVERRIDE ---
if st.session_state.hp <= 0:
    st.session_state.hp = 50
    st.session_state.coin = max(50, int(st.session_state.coin * 0.5))
    lose_exp(80)
    st.session_state.battle_frame = "<div class='shake-effect' style='background:black; color:red; padding:15px; text-align:center; border:2px solid red;'>🚨 SYSTEM REBOOT: လုပ်ငန်းရှင် လဲကျသွားသဖြင့် ဒေတာနှင့် စည်းစိမ်များ ပြန်လည်စတင်သည်။ 🚨</div>"
    st.rerun()

# --- LOGS SCREEN ---
st.markdown("---")
st.markdown("### 📜 System Logs / ကုန်သွယ်မှုမှတ်တမ်း")
for l in st.session_state.log:
    st.text(l)
