import streamlit as st
import random

# Page configuration
st.set_page_config(page_title="Thai Trader RPG: Tycoon Edition", page_icon="📈", layout="wide")

# --- ADVANCED UI & SHAKE ANIMATIONS ---
st.markdown("""
<style>
    @keyframes shake {
        0% { transform: translate(1px, 1px) rotate(0deg); }
        10% { transform: translate(-1px, -2px) rotate(-1deg); }
        20% { transform: translate(-3px, 0px) rotate(1deg); }
        30% { transform: translate(0px, 2px) rotate(0deg); }
        40% { transform: translate(1px, -1px) rotate(1deg); }
        50% { transform: translate(-1px, 2px) rotate(-1deg); }
        60% { transform: translate(-3px, 1px) rotate(0deg); }
        70% { transform: translate(2px, 1px) rotate(-1deg); }
        100% { transform: translate(1px, -2px) rotate(-1deg); }
    }
    .shake-effect { animation: shake 0.4s; }
    .stat-box {
        background: #1A1A24;
        color: #fff;
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        font-weight: bold;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    .game-card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        margin-bottom: 12px;
        border-left: 5px solid #FF4B4B;
    }
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
    confetti = "<script src='https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js'></script><script>confetti({particleCount:100, spread:60});</script>" if trigger_confetti else ""
    if sound_type in sound_urls:
        st.components.v1.html(f"{confetti}<audio autoplay><source src='{sound_urls[sound_type]}' type='audio/wav'></audio>", height=0, width=0)

# --- INITIALIZE SESSION STATE ---
if 'level' not in st.session_state: st.session_state.level = 1
if 'exp' not in st.session_state: st.session_state.exp = 0
if 'coin' not in st.session_state: st.session_state.coin = 1000
if 'gold' not in st.session_state: st.session_state.gold = 1
if 'silver' not in st.session_state: st.session_state.silver = 10
if 'hp' not in st.session_state: st.session_state.hp = 100
if 'inventory_bag' not in st.session_state: 
    st.session_state.inventory_bag = {"အိတ်": 1, "ဖိနပ်": 1, "အလှကုန်": 1, "ဖုန်း/အီလက်ထရွန်နစ်": 0, "ရွှေထည်ရတနာ": 0, "ထိုင်းစားသောက်ကုန်": 2}
if 'log' not in st.session_state: st.session_state.log = ["🚀 စီးပွားရေးလုပ်ငန်းရှင်ကြီးများရဲ့ အဆင့်မြင့်ကမ္ဘာမှ ကြိုဆိုပါတယ်။"]
if 'battle_frame' not in st.session_state: st.session_state.battle_frame = ""

def add_log(text):
    st.session_state.log.insert(0, text)
    if len(st.session_state.log) > 5: st.session_state.log.pop()

# စနစ်သစ်- XP/Level ကျဆင်းနိုင်ခြေ တွက်ချက်မှုပုံစံ
def lose_exp(amount):
    st.session_state.exp -= amount
    if st.session_state.exp < 0:
        if st.session_state.level > 1:
            st.session_state.level -= 1
            st.session_state.exp = 80  # အဆင့်ကျသွားရင် XP ကို ပြန်ညှိပေးတယ်
            add_log(f"📉 သတင်းဆိုး- သင့်လုပ်ငန်းဂုဏ်သတင်း ကျဆင်းသွားသဖြင့် အဆင့် Level {st.session_state.level} သို့ ကျသွားပါပြီ။")
        else:
            st.session_state.exp = 0

def gain_exp(amount):
    st.session_state.exp += amount
    exp_needed = st.session_state.level * 100
    if st.session_state.exp >= exp_needed:
        st.session_state.level += 1
        st.session_state.exp = 0
        add_log(f"🎉 ဂုဏ်ယူပါသည်! သင့်လုပ်ငန်း အောင်မြင်မှုကြောင့် အဆင့် Level {st.session_state.level} သို့ တက်လှမ်းသွားပါပြီ။")
        play_effect("win", trigger_confetti=True)

# --- DYNAMIC MARKET ECONOMY ---
base_prices = {"အိတ်": 150, "ဖိနပ်": 100, "အလှကုန်": 80, "ဖုန်း/အီလက်ထရွန်နစ်": 800, "ရွှေထည်ရတနာ": 1500, "ထိုင်းစားသောက်ကုန်": 40}
market_trend = random.choice(["💥 စီးပွားရေးအကျပ်အတည်း (စျေးကွက်ပျက်နေသည်)", "📈 ကုန်သွယ်မှု ကောင်းမွန်နေသည်", "⚖️ စျေးကွက် ပုံမှန်အတိုင်းရှိသည်"])

if market_trend == "💥 စီးပွားရေးအကျပ်အတည်း (စျေးကွက်ပျက်နေသည်)":
    price_modifier = random.uniform(0.4, 0.8)
elif market_trend == "📈 ကုန်သွယ်မှု ကောင်းမွန်နေသည်":
    price_modifier = random.uniform(1.2, 1.8)
else:
    price_modifier = 1.0

current_prices = {item: int(base * price_modifier) for item, base in base_prices.items()}

# --- HEADER ---
st.title("📈 Thai Trader RPG: Tycoon & Market Simulation")
st.subheader(f"📊 ယနေ့ စျေးကွက်အခြေအနေ: {market_trend}")

# --- STATS BAR ---
col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1: st.markdown(f"<div class='stat-box' style='border-bottom: 4px solid #FFD700;'>🌟 အဆင့် (Level)<br><span style='font-size:18px;'>{st.session_state.level}</span> (XP: {st.session_state.exp})</div>", unsafe_allow_html=True)
with col2: st.markdown(f"<div class='stat-box' style='border-bottom: 4px solid #FF4B4B;'>❤️ သက်စောင့် (HP)<br><span style='font-size:18px;'>{st.session_state.hp} / 100</span></div>", unsafe_allow_html=True)
with col3: st.markdown(f"<div class='stat-box' style='border-bottom: 4px solid #00F0FF;'>💵 Coin (ပိုက်ဆံ)<br><span style='font-size:18px;'>{st.session_state.coin} ฿</span></div>", unsafe_allow_html=True)
with col4: st.markdown(f"<div class='stat-box' style='border-bottom: 4px solid #FFAA00;'>🟡 ရွှေတုံး<br><span style='font-size:18px;'>{st.session_state.gold}</span></div>", unsafe_allow_html=True)
with col5: st.markdown(f"<div class='stat-box' style='border-bottom: 4px solid #C0C0C0;'>⚪ ငွေပြား<br><span style='font-size:18px;'>{st.session_state.silver}</span></div>", unsafe_allow_html=True)
with col6: 
    inv_text = " | ".join([f"{k}:{v}" for k, v in st.session_state.inventory_bag.items() if v > 0])
    st.markdown(f"<div class='stat-box' style='border-bottom: 4px solid #00FF00;'>🎒 ဂိုဒေါင်တွင်း ရောင်းကုန်များ<br><span style='font-size:11px;'>{inv_text if inv_text else 'ဂိုဒေါင်ဗလာဖြစ်နေသည်'}</span></div>", unsafe_allow_html=True)

if st.session_state.battle_frame:
    st.markdown(st.session_state.battle_frame, unsafe_allow_html=True)
    st.session_state.battle_frame = ""

# --- ACTIONS ---
col_act1, col_act2, col_act3 = st.columns(3)

with col_act1:
    st.markdown("<div class='game-card'><h3>🔍 စျေးကွက်ထဲ ရှာဖွေ/စူးစမ်းခြင်း</h3><p>အဆင့် (Level) တက်နိုင်သလို ကျဆင်းမည့် အန္တရာယ်လည်းရှိသည်</p></div>", unsafe_allow_html=True)
    if st.button("🗺️ စျေးကွက်အတွင်း စူးစမ်းရှာဖွေမည်"):
        play_effect("click")
        loot = random.choice(["good", "bad", "nothing"])
        if loot == "good":
            gain_exp(20)
            st.session_state.coin += 100
            add_log("🔍 စျေးကွက်ထဲတွင် စီးပွားရေးအခွင့်အလမ်းသစ်တွေ့သဖြင့် ပိုက်ဆံ ၁၀၀ ฿ ရရှိသည်။")
        elif loot == "bad":
            lose_exp(30) # အဆင့်ကျနိုင်ခြေ
            damage = random.randint(10, 20)
            st.session_state.hp = max(0, st.session_state.hp - damage)
            st.session_state.battle_frame = f"<div class='shake-effect' style='background:#ffcccc; padding:10px; border-radius:8px; text-align:center;'>🤕 ကုန်ပစ္စည်းအတု မိသဖြင့် နာမည်ပျက်ပြီး အဆင့် (XP) နှင့် HP ကျဆင်းသွားသည်။</div>"
            play_effect("lose")
        else:
            add_log("🔍 ယနေ့ စျေးကွက်သည် အေးဆေးငြိမ်သက်နေသည်။")
        st.rerun()

with col_act2:
    st.markdown("<div class='game-card'><h3>⚔️ စွန့်စားခန်းနှင့် လုပ်ငန်းလုယက်ပွဲ</h3><p>နိုင်လျှင် အမြတ်ကြီးသော်လည်း ရှုံးလျှင် အဆင့်အတန်းပါ ကျသွားနိုင်သည်</p></div>", unsafe_allow_html=True)
    if st.button("💥 ပြိုင်ဘက်များနှင့် စျေးကွက်လုပွဲဆင်နွှဲမည်!"):
        play_effect("hit")
        win = random.choice([True, False])
        if win:
            gain_exp(40)
            st.session_state.coin += 300
            st.session_state.battle_frame = "<div style='background:linear-gradient(to right, #45a247, #283c86); padding:15px; border-radius:8px; color:white; text-align:center;'>✨ အောင်မြင်မှု! စျေးကွက်ဝေစုကို လုယူနိုင်ခဲ့ပြီး အမြတ်အစွန်းများ ရရှိသည်။ ✨</div>"
            play_effect("win", trigger_confetti=True)
        else:
            lose_exp(50) # ရှုံးလျှင် အဆင့်ကျနိုင်သည်
            damage = random.randint(25, 40)
            st.session_state.hp = max(0, st.session_state.hp - damage)
            st.session_state.battle_frame = f"<div class='shake-effect' style='background:#330000; color:red; padding:15px; border-radius:8px; text-align:center;'>💀 ရှုံးနိမ့်မှု! ပြိုင်ဘက်များ၏ ဒဏ်ကြောင့် လုပ်ငန်းဂုဏ်သတင်းနှင့် HP ဆုံးရှုံးသည်။ (-{damage} HP)</div>"
            play_effect("lose")
        st.rerun()
        
    if st.session_state.hp < 100:
        if st.button("❤️ လုပ်ငန်းနားပြီး ကျန်းမာရေးပြန်လည်ပြုစုမည် (-၁၀၀ ฿)"):
            if st.session_state.coin >= 100:
                st.session_state.coin -= 100
                st.session_state.hp = min(100, st.session_state.hp + 50)
                add_log("❤️ အနားယူလိုက်သဖြင့် HP ၅၀ ပြန်လည်ပြည့်တင်းလာသည်။")
            st.rerun()

with col_act3:
    st.markdown("<div class='game-card'><h3>🏪 ကုန်စုံဆိုင်ကြီး (ပစ္စည်းမျိုးစုံ)</h3><p>စျေးကျချိန်တွင်ဝယ်ပြီး စျေးတက်ချိန်တွင် အမြတ်ထုတ်ပါ</p></div>", unsafe_allow_html=True)
    
    selected_item = st.selectbox("ကုန်ပစ္စည်း ရွေးချယ်ပါ:", list(current_prices.keys()))
    price = current_prices[selected_item]
    st.write(f"💵 **ယခုပေါက်စျေး:** `{price} ฿` | (မူရင်းစျေး: {base_prices[selected_item]} ฿)")
    
    col_b, col_s = st.columns(2)
    with col_b:
        if st.button(f"🛒 {selected_item} ကို ဝယ်ယူမည်"):
            if st.session_state.coin >= price:
                st.session_state.coin -= price
                st.session_state.inventory_bag[selected_item] += 1
                add_log(f"🛒 {selected_item} ကို စျေး {price} ฿ ဖြင့် အဝယ်သွင်းလိုက်သည်။")
                play_effect("trade")
            else:
                add_log("❌ ပိုက်ဆံမလောက်ပါ။")
            st.rerun()
            
    with col_s:
        if st.session_state.inventory_bag[selected_item] > 0:
            if st.button(f"💵 {selected_item} ကို ပြန်ရောင်းမည်"):
                st.session_state.inventory_bag[selected_item] -= 1
                st.session_state.coin += price
                profit_loss = price - base_prices[selected_item]
                if profit_loss > 0:
                    add_log(f"📈 {selected_item} ကို ရောင်းချပြီး အမြတ် {profit_loss} ฿ ရရှိခဲ့သည်။")
                else:
                    add_log(f"📉 စျေးကွက်မကောင်းသဖြင့် {selected_item} ကို အရှုံး {-profit_loss} ฿ ဖြင့် ရောင်းလိုက်ရသည်။")
                play_effect("trade")
                st.rerun()

# --- HEALTH BANKRUPTCY CHECK ---
if st.session_state.hp <= 0:
    st.session_state.hp = 50
    st.session_state.coin = max(100, int(st.session_state.coin * 0.5))
    lose_exp(100) # လဲကျရင် အဆင့်အများကြီးကျမယ်
    st.session_state.battle_frame = "<div class='shake-effect' style='background:black; color:white; padding:15px; text-align:center;'>🚨 လုပ်ငန်းရှင်ကြီး လဲကျသွားသဖြင့် ဆေးကုသစရိတ်ကြောင့် အဆင့်ရော စည်းစိမ်ပါ အများကြီး လျော့ကျသွားသည်။ 🚨</div>"
    st.rerun()

# --- LOGS ---
st.markdown("---")
st.markdown("### 📜 လုပ်ဆောင်ချက်နှင့် စီးပွားရေးဖြစ်ရပ်မှတ်တမ်း")
for l in st.session_state.log:
    st.text(l)
