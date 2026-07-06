import streamlit as st
import random
import pandas as pd

# Page configuration
st.set_page_config(page_title="Cyber Live Market Tycoon Pro", page_icon="📈", layout="wide")

# --- Streamlit Auto Refresh (၂ စက္ကန့်တိုင်း အော်တိုပတ်ဝန်းကျင် လည်ပတ်ရန်) ---
st.logo("https://assets.mixkit.co/active_storage/sfx/2019/2019-84.wav") # dummy load
st.fragment(run_every="2s")

# --- PREMIUM CYBER DARK STYLE ---
st.markdown("""
<style>
    .stApp { background-color: #0B0C10; color: #C5C6C7; }
    h1, h2, h3, h4 { color: #66FCF1 !important; font-family: 'Courier New', monospace; }
    .stat-box {
        background: #1F2833; color: #fff; padding: 10px; border-radius: 10px;
        text-align: center; font-weight: bold; border: 1px solid #45A29E;
    }
    .game-card {
        background-color: #1F2833; padding: 15px; border-radius: 12px;
        border: 1px solid #45A29E; margin-bottom: 10px;
    }
    .stButton>button {
        background: linear-gradient(135deg, #45A29E 0%, #1F2833 100%);
        color: #66FCF1 !important; border: 1px solid #66FCF1 !important;
        border-radius: 8px; font-weight: bold; width: 100%;
    }
    .stButton>button:hover { box-shadow: 0 0 10px #66FCF1; }
</style>
""", unsafe_allow_html=True)

# --- SOUND EFFECT PLAYER ---
def play_sound(sound_type):
    sound_urls = {
        "click": "https://assets.mixkit.co/active_storage/sfx/2568/2568-84.wav",
        "trade": "https://assets.mixkit.co/active_storage/sfx/2019/2019-84.wav",
        "win": "https://assets.mixkit.co/active_storage/sfx/1435/1435-84.wav",
        "lose": "https://assets.mixkit.co/active_storage/sfx/2622/2622-84.wav"
    }
    if sound_type in sound_urls:
        st.components.v1.html(f"""<audio autoplay><source src="{sound_urls[sound_type]}" type="audio/wav"></audio>""", height=0, width=0)

# --- 🛠️ FIX 1: DATA PERSISTENCE (ပျောက်ကွယ်သွားခြင်းမရှိအောင် ထိန်းသိမ်းခြင်း) ---
if 'player_coin' not in st.session_state: st.session_state.player_coin = 1000
if 'player_level' not in st.session_state: st.session_state.player_level = 1
if 'player_xp' not in st.session_state: st.session_state.player_xp = 0
if 'gold' not in st.session_state: st.session_state.gold = 1
if 'silver' not in st.session_state: st.session_state.silver = 10
if 'inventory' not in st.session_state: st.session_state.inventory = {"ဖုန်း": 0, "ရွှေထည်": 0, "စားသောက်ကုန်": 0}
if 'buy_costs' not in st.session_state: st.session_state.buy_costs = {"ဖုန်း": [], "ရွှေထည်": [], "စားသောက်ကုန်": []}
if 'log' not in st.session_state: st.session_state.log = ["🤖 စနစ်များအားလုံး တိကျသေချာစွာ စတင်လိုက်ပါပြီ။"]

# ပြိုင်ဘက် ၃၀ ဦး အချက်အလက် မပျောက်ပျက်အောင် ထိန်းသိမ်းခြင်း
if 'competitors' not in st.session_state:
    names = [
        "Somchai", "Thana", "Anong", "Kitti", "Malai", "Narong", "Pravat", "Somsak", "Viroj", "Chai",
        "Arun", "Boon-Mee", "Can", "Daeng", "Erawan", "Kamal", "Lawan", "Mee", "Noi", "Pim",
        "Rung", "Sakda", "Siri", "Suchart", "Sunan", "Surachai", "Teerachai", "Ubon", "Wanchai", "Yod"
    ]
    st.session_state.competitors = {name: random.randint(800, 1500) for name in names}

# --- 🛠️ FIX 2: TIME-BASED AUTO MARKET PRICES ---
# စျေးနှုန်းများ ခလုတ်နှိပ်တိုင်း မပြောင်းဘဲ၊ အချိန်အလိုက် တဖြည်းဖြည်းသာ ပြောင်းလဲစေရန်
base_prices = {"ဖုန်း": 800, "ရွှေထည်": 1500, "စားသောက်ကုန်": 40}
if 'current_prices' not in st.session_state:
    st.session_state.current_prices = base_prices.copy()

# ၃၀ ရာခိုင်နှုန်းသော အခွင့်အရေးဖြင့်သာ စျေးကွက်ကို အလိုအလျောက် ပြောင်းလဲစေခြင်း (အလွန်အကျွံ မဖြစ်စေရန်)
if random.random() < 0.3:
    for item in base_prices.keys():
        modifier = random.uniform(0.6, 1.7)
        st.session_state.current_prices[item] = int(base_prices[item] * modifier)
    # ပြိုင်ဘက်များလည်း အလိုအလျောက် အရောင်းအဝယ်လုပ်ပြီး အမှတ်ပြောင်းခြင်း
    for comp in st.session_state.competitors:
        st.session_state.competitors[comp] += random.randint(-40, 60)
        if st.session_state.competitors[comp] < 100: st.session_state.competitors[comp] = 100

# --- LEVEL & RANK SYSTEM တွက်ချက်ခြင်း ---
all_traders = {"သင် (Player)": st.session_state.player_coin}
for name, cash in st.session_state.competitors.items():
    all_traders[name] = cash

ranked_traders = sorted(all_traders.items(), key=lambda x: x[1], reverse=True)
player_rank = [i for i, x in enumerate(ranked_traders) if x[0] == "သင် (Player)"][0] + 1

# --- HEADER UI ---
st.title("⚡ Cyber Live Market Tycoon Pro")
st.write("---")

# --- PLAYER STATS BAR ---
col1, col2, col3, col4 = st.columns(4)
with col1: st.markdown(f"<div class='stat-box' style='color:#66FCF1;'>🌟 LEVEL (အဆင့်)<br><span style='font-size:22px;'>{st.session_state.player_level}</span> (XP: {st.session_state.player_xp}/100)</div>", unsafe_allow_html=True)
with col2: st.markdown(f"<div class='stat-box' style='color:#00F0FF;'>💵 သင်၏ပိုက်ဆံ (Coin)<br><span style='font-size:22px;'>{st.session_state.player_coin} ฿</span></div>", unsafe_allow_html=True)
with col3: st.markdown(f"<div class='stat-box' style='color:#FFD700;'>🏆 လက်ရှိ RANK (အဆင့်စာရင်း)<br><span style='font-size:22px;'>#{player_rank} / 31</span></div>", unsafe_allow_html=True)
with col4: 
    inv_txt = " | ".join([f"{k}:{v}" for k, v in st.session_state.inventory.items()])
    st.markdown(f"<div class='stat-box' style='color:#00FF00; font-size:12px;'>🎒 သင်၏ဂိုဒေါင်ပစ္စည်း<br><span>{inv_txt}</span><br><small>🪙ရွှေ: {st.session_state.gold} | 🥈ငွေ: {st.session_state.silver}</small></div>", unsafe_allow_html=True)

st.write("")

# --- MAIN LAYOUT ---
game_col, rank_col = st.columns([2, 1])

with game_col:
    st.markdown("### 🏪 စျေးကွက်အတွင်း ကုန်သွယ်မှုပြုလုပ်ရန်")
    
    for item, price in st.session_state.current_prices.items():
        # အဝယ်ပျမ်းမျှစျေးတွက်ချက်ခြင်း
        costs = st.session_state.buy_costs[item]
        avg_text = f"{int(sum(costs)/len(costs))} ฿" if costs else "မရှိသေးပါ"
        
        with st.container():
            st.markdown(f"""
            <div class='game-card'>
                <span style='font-size:18px; font-weight:bold;'>📦 {item}</span> — 
                ယခုပေါက်စျေး: <span style='color:#66FCF1; font-weight:bold;'>{price} ฿</span> | 
                <span style='font-size:13px; color:#aaa;'>သင့်အဝယ်ရင်းနှီးစျေး (Avg Buy): {avg_text}</span>
            </div>
            """, unsafe_allow_html=True)
            
            btn_buy, btn_sell = st.columns(2)
            with btn_buy:
                if st.button(f"🛒 ဝယ်ယူမည် ({item})", key=f"buy_{item}"):
                    if st.session_state.player_coin >= price:
                        st.session_state.player_coin -= price
                        st.session_state.inventory[item] += 1
                        st.session_state.buy_costs[item].append(price) # ဝယ်စျေးကို မှတ်ထားမယ်
                        
                        # အဆင့်တက်ရန် အမှတ် (XP) ပေးခြင်း
                        st.session_state.player_xp += 15
                        if st.session_state.player_xp >= 100:
                            st.session_state.player_level += 1
                            st.session_state.player_xp = 0
                            
                        st.session_state.log.insert(0, f"🛒 ဝယ်ယူမှုအောင်မြင်သည်- {item} ကို {price} ฿ ဖြင့် ဝယ်လိုက်သည်။")
                        play_sound("trade")
                        st.rerun()
            with btn_sell:
                if st.button(f"💵 ရောင်းချမည် ({item})", key=f"sell_{item}"):
                    if st.session_state.inventory[item] > 0:
                        st.session_state.inventory[item] -= 1
                        st.session_state.player_coin += price
                        
                        # ရင်းနှီးစျေးနဲ့ နှိုင်းယှဉ်ပြီး အမြတ်/အရှုံး တိကျစွာပြသခြင်း
                        saved_cost = st.session_state.buy_costs[item].pop(0) if st.session_state.buy_costs[item] else base_prices[item]
                        diff = price - saved_cost
                        
                        if diff >= 0:
                            st.session_state.player_xp += 20  # အမြတ်ရရင် XP တက်မယ်
                            st.session_state.silver += 1     # ငွေပြားဆုလာဘ်ရမယ်
                            status_msg = f"📈 အမြတ်ရရှိသည်! {item} မှ အသားတင်အမြတ် (+{diff} ฿) နှင့် ငွေပြား ၁ ပြား ရရှိသည်။"
                        else:
                            st.session_state.player_xp = max(0, st.session_state.player_xp - 15) # အရှုံးပေါ်ရင် XP ကျမယ်
                            status_msg = f"📉 အရှုံးပေါ်သည်! {item} ကို ရင်းနှီးစျေးအောက် စျေးလျှော့ရောင်းလိုက်ရသည်။ (အရှုံး: {-diff} ฿)"
                            
                        if st.session_state.player_xp >= 100:
                            st.session_state.player_level += 1
                            st.session_state.player_xp = 0
                            
                        st.session_state.log.insert(0, status_msg)
                        play_sound("trade")
                        st.rerun()
            st.write("")

    # --- LIVE LOGS ---
    st.markdown("### 📜 ကုန်သွယ်မှုနှင့် စာရင်းအင်း မှတ်တမ်း")
    for l in st.session_state.log[:4]:
        st.caption(l)

with rank_col:
    st.markdown("### 🏆 ကုန်သည် Rank စာရင်း (Top 10)")
    rank_df = pd.DataFrame(ranked_traders, columns=["ကုန်သည်အမည်", "ပိုင်ဆိုင်မှု (Coin)"])
    rank_df.index = rank_df.index + 1
    st.dataframe(rank_df.head(10), use_container_width=True)
    st.markdown(f"**သင့်အဆင့်:** Rank `#{player_rank}` တွင် တည်ငြိမ်စွာ ရှိနေသည်။")
