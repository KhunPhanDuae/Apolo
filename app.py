import streamlit as st
import random
import time

# Page configuration
st.set_page_config(page_title="Thai Trader RPG Ultimate", page_icon="⚔️", layout="wide")

# --- ADVANCED UI & ANIMATIONS (CSS) ---
st.markdown("""
<style>
    /* တုန်ခါခြင်း လှုပ်ရှားမှု (Screen Shake Animation) */
    @keyframes shake {
        0% { transform: translate(1px, 1px) rotate(0deg); }
        10% { transform: translate(-1px, -2px) rotate(-1deg); }
        20% { transform: translate(-3px, 0px) rotate(1deg); }
        30% { transform: translate(0px, 2px) rotate(0deg); }
        40% { transform: translate(1px, -1px) rotate(1deg); }
        50% { transform: translate(-1px, 2px) rotate(-1deg); }
        60% { transform: translate(-3px, 1px) rotate(0deg); }
        70% { transform: translate(2px, 1px) rotate(-1deg); }
        80% { transform: translate(-1px, -1px) rotate(1deg); }
        90% { transform: translate(2px, 2px) rotate(0deg); }
        100% { transform: translate(1px, -2px) rotate(-1deg); }
    }
    
    /* စာသားများ မှိတ်တုတ်မှိတ်တုတ် ဖြစ်စေမည့် Animation */
    @keyframes glow {
        0% { text-shadow: 0 0 5px #fff, 0 0 10px #ff4b4b; }
        50% { text-shadow: 0 0 20px #fff, 0 0 30px #ff2b2b; }
        100% { text-shadow: 0 0 5px #fff, 0 0 10px #ff4b4b; }
    }

    .shake-effect { animation: shake 0.5s; }
    .glow-text { animation: glow 1s infinite; color: #ff4b4b; font-weight: bold; }
    
    .stat-box {
        background: #111;
        color: #fff;
        padding: 12px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .game-card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
        margin-bottom: 15px;
        transition: 0.3s;
    }
    .game-card:hover { transform: translateY(-3px); }
</style>
""", unsafe_allow_html=True)

# --- SOUND & CONFETTI VISUAL EFFECT SYSTEM ---
def play_sound_and_effect(sound_type, trigger_visual=False):
    sound_urls = {
        "click": "https://assets.mixkit.co/active_storage/sfx/2568/2568-84.wav",
        "hit": "https://assets.mixkit.co/active_storage/sfx/2763/2763-84.wav",
        "win": "https://assets.mixkit.co/active_storage/sfx/1435/1435-84.wav",
        "lose": "https://assets.mixkit.co/active_storage/sfx/2622/2622-84.wav",
        "trade": "https://assets.mixkit.co/active_storage/sfx/2019/2019-84.wav"
    }
    
    # နိုင်တဲ့အခါ ရွှေမိုးငွေမိုးရွာသွန်းမည့် JavaScript အထူးပြကွက်
    confetti_script = """
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
    <script>
        confetti({ particleCount: 150, spread: 80, origin: { y: 0.6 } });
    </script>
    """ if trigger_visual and sound_type == "win" else ""

    if sound_type in sound_urls:
        st.components.v1.html(
            f"""
            {confetti_script}
            <audio autoplay><source src="{sound_urls[sound_type]}" type="audio/wav"></audio>
            """, height=0, width=0
        )

# --- GAME STATE ---
if 'level' not in st.session_state: st.session_state.level = 1
if 'exp' not in st.session_state: st.session_state.exp = 0
if 'coin' not in st.session_state: st.session_state.coin = 600
if 'gold' not in st.session_state: st.session_state.gold = 0
if 'silver' not in st.session_state: st.session_state.silver = 5
if 'hp' not in st.session_state: st.session_state.hp = 100
if 'inventory_bag' not in st.session_state: st.session_state.inventory_bag = {"အိတ်": 1, "ဖိနပ်": 1, "အလှကုန်": 1}
if 'log' not in st.session_state: st.session_state.log = ["🎮 စိတ်လှုပ်ရှားဖွယ် ပြကွက်အသစ်များဖြင့် စတင်ပါပြီ။"]
if 'battle_frame' not in st.session_state: st.session_state.battle_frame = "" # တိုက်ခိုက်မှု အမြင်အာရုံပြကွက်အတွက်

def add_log(text):
    st.session_state.log.insert(0, text)
    if len(st.session_state.log) > 5: st.session_state.log.pop()

# --- MARKET ECONOMY ---
market_trend = random.choice(["📈 ပေါက်စျေး မြင့်တက်နေသည်", "📉 ပေါက်စျေး ကျဆင်းနေသည်", "⚖️ ဈေးကွက် တည်ငြိမ်နေသည်"])
price_modifier = random.uniform(0.6, 1.6) if market_trend != "⚖️ ဈေးကွက် တည်ငြိမ်နေသည်" else 1.0
current_prices = {item: int(base * price_modifier) for item, base in {"အိတ်": 150, "ဖိနပ်": 100, "အလှကုန်": 80}.items()}

# --- GAME UI ---
st.title("⚔️ Thai Trader RPG: Ultimate Edition")
st.subheader(f"📊 စျေးကွက်အနေအထား: {market_trend}")

# --- STATS BAR ---
col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1: st.markdown(f"<div class='stat-box' style='border-bottom: 4px solid #FFD700;'>🌟 အဆင့် (Level)<br><span style='font-size:20px;'>{st.session_state.level}</span></div>", unsafe_allow_html=True)
with col2: st.markdown(f"<div class='stat-box' style='border-bottom: 4px solid #FF4B4B;'>❤️ သက်စောင့် (HP)<br><span style='font-size:20px;'>{st.session_state.hp} / 100</span></div>", unsafe_allow_html=True)
with col3: st.markdown(f"<div class='stat-box' style='border-bottom: 4px solid #00F0FF;'>💵 ပိုက်ဆံ<br><span style='font-size:20px;'>{st.session_state.coin} ฿</span></div>", unsafe_allow_html=True)
with col4: st.markdown(f"<div class='stat-box' style='border-bottom: 4px solid #FFAA00;'>🟡 ရွှေတုံး<br><span style='font-size:20px;'>{st.session_state.gold}</span></div>", unsafe_allow_html=True)
with col5: st.markdown(f"<div class='stat-box' style='border-bottom: 4px solid #C0C0C0;'>⚪ ငွေပြား<br><span style='font-size:20px;'>{st.session_state.silver}</span></div>", unsafe_allow_html=True)
with col6: st.markdown(f"<div class='stat-box' style='border-bottom: 4px solid #00FF00;'>🎒 အိတ်ထဲရှိပစ္စည်း<br><span style='font-size:12px;'>အိတ်:{st.session_state.inventory_bag['အိတ်']} | ဖိနပ်:{st.session_state.inventory_bag['ဖိနပ်']} | အလှကုန်:{st.session_state.inventory_bag['အလှကုန်']}</span></div>", unsafe_allow_html=True)

# --- ANIMATION BATTLE SCREEN (ရင်ခုန်စရာ ပြကွက်ဧရိယာ) ---
if st.session_state.battle_frame:
    st.markdown(st.session_state.battle_frame, unsafe_allow_html=True)
    st.session_state.battle_frame = "" # ပြသပြီးရင် ပြန်ဖျက်မယ်

# --- ACTIONS ---
col_act1, col_act2, col_act3 = st.columns(3)

with col_act1:
    st.markdown("<div class='game-card'><h3>🔍 စျေးကွက်နယ်မြေ ရှာဖွေခြင်း</h3></div>", unsafe_allow_html=True)
    if st.button("🗺️ နယ်မြေသစ် လှည့်လည်ရှာဖွေမည်"):
        play_sound_and_effect("click")
        st.session_state.exp += 15
        loot = random.choice(["coin", "silver", "item", "danger"])
        
        if loot == "danger":
            damage = random.randint(15, 25)
            st.session_state.hp = max(0, st.session_state.hp - damage)
            st.session_state.battle_frame = f"<div class='shake-effect' style='background-color:#ffcccc; padding:15px; border-radius:10px; text-align:center;'><h3 class='glow-text'>⚠️ အန္တရာယ်ကပ်ဘေး! လမ်းတွင်လဲကျပြီး ဒဏ်ရာရခဲ့သည် (-{damage} HP)</h3></div>"
            play_sound_and_effect("lose")
        else:
            st.session_state.coin += 50
            add_log("🔍 ရှာဖွေရေး အောင်မြင်ပြီး ရောင်းကုန်နှင့် ကုန်သွယ်ငွေများ ရရှိခဲ့သည်။")
        st.rerun()

with col_act2:
    st.markdown("<div class='game-card'><h3>⚔️ ရင်ခုန်စရာ စွန့်စားတိုက်ခိုက်ပွဲ</h3></div>", unsafe_allow_html=True)
    if st.button("💥 အဆုံးအဖြတ် တိုက်ပွဲဆင်နွှဲမည်!"):
        play_sound_and_effect("hit")
        win = random.choice([True, False])
        st.session_state.exp += 35
        
        if win:
            gold_gain = random.randint(1, 2)
            coin_gain = random.randint(200, 400)
            st.session_state.gold += gold_gain
            st.session_state.coin += coin_gain
            st.session_state.battle_frame = """
            <div style='background: linear-gradient(to right, #ffe259, #ffa751); padding:20px; border-radius:10px; text-align:center; color:white;'>
                <h2>✨ VICTORY! အောင်ပွဲခံခြင်း ပြကွက် ✨</h2>
                <p>ရန်သူကို အောင်မြင်စွာ နှိမ်နင်းနိုင်ခဲ့သည်။ ရွှေနှင့် ဒင်္ဂါးပြားများ ဝေဝေဆာဆာ ရရှိသည်။</p>
            </div>
            """
            play_sound_and_effect("win", trigger_visual=True)
        else:
            damage = random.randint(30, 50)
            st.session_state.hp = max(0, st.session_state.hp - damage)
            st.session_state.battle_frame = f"""
            <div class='shake-effect' style='background: #330000; padding:20px; border-radius:10px; text-align:center; color:red; border:3px solid red;'>
                <h2 class='glow-text'>💀 DEFEATED! ဒဏ်ရာပြင်းထန်စွာရခြင်းပြကွက် 💀</h2>
                <p>ရန်သူ့တိုက်ကွက်ကြောင့် ပြင်းထန်စွာ လဲကျသွားသည်။ (-{damage} HP)</p>
            </div>
            """
            play_sound_and_effect("lose")
        st.rerun()

with col_act3:
    st.markdown("<div class='game-card'><h3>🏪 ကုန်သည်ကြီးများ အရောင်းအဝယ်</h3></div>", unsafe_allow_html=True)
    st.write(f"💼 **ပေါက်စျေး:** အိတ်({current_prices['အိတ်']}฿) | ဖိနပ်({current_prices['ဖိနပ်']}฿)")
    
    col_b, col_s = st.columns(2)
    with col_b:
        if st.button("🛒 အိတ် ဝယ်မည်"):
            if st.session_state.coin >= current_prices['အိတ်']:
                st.session_state.coin -= current_prices['အိတ်']
                st.session_state.inventory_bag['အိတ်'] += 1
                play_sound_and_effect("trade")
                st.rerun()
    with col_s:
        if st.session_state.inventory_bag['အိတ်'] > 0:
            if st.button("💵 အိတ် ရောင်းမည်"):
                st.session_state.inventory_bag['အိတ်'] -= 1
                st.session_state.coin += current_prices['အိတ်']
                play_sound_and_effect("trade")
                st.rerun()

# --- ⚠️ HEALTH CHECK ---
if st.session_state.hp <= 0:
    st.session_state.hp = 60
    st.session_state.gold = max(0, st.session_state.gold - 1)
    st.session_state.coin = max(50, int(st.session_state.coin * 0.6))
    st.session_state.battle_frame = "<div class='shake-effect' style='background-color:black; color:white; padding:20px; text-align:center;'><h1>💀 လုံးဝလဲကျသွားသဖြင့် ဆေးရုံတွင် ကုသမှုခံယူလိုက်ရသည်။</h1></div>"
    st.rerun()

# --- LOGS ---
st.markdown("---")
st.markdown("### 📜 လုပ်ဆောင်ချက် မှတ်တမ်း")
for l in st.session_state.log:
    st.text(l)
