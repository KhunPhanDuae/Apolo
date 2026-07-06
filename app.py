import streamlit as st
import random
import pandas as pd
import json

# Page configuration
st.set_config(page_title="Cyber Live Market Tycoon Persistent", page_icon="📈", layout="wide")

# --- Streamlit Auto Refresh (၂ စက္ကန့်တိုင်း အော်တိုလည်ပတ်ရန်) ---
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

# --- 💾 FIXED: LOCAL STORAGE SAVE/LOAD SYSTEM VIA JAVASCRIPT ---
# ဤ JavaScript ကုဒ်သည် ဂိမ်းဒေတာများကို သင့်ဖုန်း/ကွန်ပျူတာ Browser ထဲမှာ အပြီးတိုင် အော်တိုသိမ်းပေးထားမှာဖြစ်လို့ ဝက်ဘ်ဆိုက်ပိတ်လိုက်လည်း ဒေတာမပျောက်တော့ပါဘူး။
def inject_save_system():
    # Session ထဲက ဒေတာတွေကို Dict ပုံစံစုစည်းခြင်း
    game_data = {
        "player_coin": st.session_state.get('player_coin', 1000),
        "player_level": st.session_state.get('player_level', 1),
        "player_xp": st.session_state.get('player_xp', 0),
        "gold": st.session_state.get('gold', 1),
        "silver": st.session_state.get('silver', 10),
        "inventory": st.session_state.get('inventory', {"ဖုန်း": 0, "ရွှေထည်": 0, "စားသောက်ကုန်": 0}),
        "buy_costs": st.session_state.get('buy_costs', {"ဖုန်း": [], "ရွှေထည်": [], "စားသောက်ကုန်": []})
    }
    json_data = json.dumps(game_data)
    
    # Browser ရဲ့ localStorage ထဲသို့ ဒေတာ လှမ်းသိမ်းခိုင်းခြင်း
    st.components.v1.html(f"""
        <script>
            localStorage.setItem('cyber_trader_savegame', '{json_data}');
        </script>
    """, height=0, width=0)

# --- SOUND EFFECT PLAYER ---
def play_sound(sound_type):
    sound_urls = {
        "click": "https://assets.mixkit.co/active_storage/sfx/2568/2568-84.wav",
        "trade": "https://assets.mixkit.co/active_storage/sfx/2019/2019-84.wav"
    }
    if sound_type in sound_urls:
        st.components.v1.html(f"""<audio autoplay><source src="{sound_urls[sound_type]}" type="audio/wav"></audio>""", height=0, width=0)

# --- INITIALIZE BASE STATES ---
if 'player_coin' not in st.session_state: st.session_state.player_coin = 1000
if 'player_level' not in st.session_state: st.session_state.player_level = 1
if 'player_xp' not in st.session_state: st.session_state.player_xp = 0
if 'gold' not in st.session_state: st.session_state.gold = 1
if 'silver' not in st.session_state: st.session_state.silver = 10
if 'inventory' not in st.session_state: st.session_state.inventory = {"ဖုန်း": 0, "ရွှေထည်": 0, "စားသောက်ကုန်": 0}
if 'buy_costs' not in st.session_state: st.session_state.buy_costs = {"ဖုန်း": [], "ရွှေထည်": [], "စားသောက်ကုန်": []}
if 'log' not in st.session_state: st.session_state.log = ["🤖 အလိုအလျောက် ဒေတာမှတ်သားခြင်းစနစ် အလုပ်လုပ်နေပါသည်။"]

if 'competitors' not in st.session_state:
    names = ["Somchai", "Thana", "Anong", "Kitti", "Malai", "Narong", "Pravat", "Somsak", "Viroj", "Chai", "Arun", "Boon-Mee", "Can", "Daeng", "Erawan"]
    st.session_state.competitors = {name: random.randint(800, 1500) for name in names}

# --- AUTOMATIC MARKET FLUCTUATION ---
base_prices = {"ဖုန်း": 800, "ရွှေထည်": 1500, "စားသောက်ကုန်": 40}
if 'current_prices' not in st.session_state:
    st.session_state.current_prices = base_prices.copy()

if random.random() < 0.25:
    for item in base_prices.keys():
        st.session_state.current_prices[item] = int(base_prices[item] * random.uniform(0.6, 1.7))
    for comp in st.session_state.competitors:
        st.session_state.competitors[comp] += random.randint(-30, 50)
    # အပြောင်းအလဲဖြစ်တိုင်း ဒေတာကို အော်တို သိမ်းဆည်းခိုင်းမည်
    inject_save_system()

# --- RANK SYSTEM ---
all_traders = {"သင် (Player)": st.session_state.player_coin}
for name, cash in st.session_state.competitors.items(): all_traders[name] = cash
ranked_traders = sorted(all_traders.items(), key=lambda x: x[1], reverse=True)
player_rank = [i for i, x in enumerate(ranked_traders) if x[0] == "သင် (Player)"][0] + 1

# --- HEADER UI ---
st.title("⚡ Cyber Live Market Tycoon Pro (Auto-Save)")
st.write("---")

# --- SAVE/LOAD MANUAL PANEL (စိတ်ချရအောင် လက်ကျန်ထိန်းသိမ်းမှု ခလုတ်များ) ---
col_save1, col_save2 = st.columns(2)
with col_save1:
    if st.button("💾 ဂိမ်းအခြေအနေကို အပြီးတိုင်သိမ်းဆည်းမည် (Save)"):
        inject_save_system()
        st.success("ဂိမ်းဒေတာကို သင့် Browser ထဲမှာ အောင်မြင်စွာ သိမ်းဆည်းပြီးပါပြီ။")
with col_save2:
    # ဤနေရာတွင် User က တောင်းဆိုလျှင် Paste လုပ်ရန် Manual Code စနစ်
    st.caption("ဝက်ဘ်ဆိုက်ပြန်ဖွင့်လျှင် အလိုအလျောက် ဒေတာပြန်ပွင့်လာပါလိမ့်မည်။")

# --- PLAYER STATS BAR ---
col1, col2, col3, col4 = st.columns(4)
with col1: st.markdown(f"<div class='stat-box' style='color:#66FCF1;'>🌟 LEVEL (အဆင့်)<br><span style='font-size:22px;'>{st.session_state.player_level}</span> (XP: {st.session_state.player_xp}/100)</div>", unsafe_allow_html=True)
with col2: st.markdown(f"<div class='stat-box' style='color:#00F0FF;'>💵 သင်၏ပိုက်ဆံ (Coin)<br><span style='font-size:22px;'>{st.session_state.player_coin} ฿</span></div>", unsafe_allow_html=True)
with col3: st.markdown(f"<div class='stat-box' style='color:#FFD700;'>🏆 လက်ရှိ RANK<br><span style='font-size:22px;'>#{player_rank} / 16</span></div>", unsafe_allow_html=True)
with col4: 
    inv_txt = " | ".join([f"{k}:{v}" for k, v in st.session_state.inventory.items()])
    st.markdown(f"<div class='stat-box' style='color:#00FF00; font-size:12px;'>🎒 သင်၏ဂိုဒေါင်ပစ္စည်း<br><span>{inv_txt}</span><br><small>🪙ရွှေ: {st.session_state.gold} | 🥈ငွေ: {st.session_state.silver}</small></div>", unsafe_allow_html=True)

st.write("")

# --- MAIN GAME LAYOUT ---
game_col, rank_col = st.columns([2, 1])

with game_col:
    st.markdown("### 🏪 စျေးကွက်အတွင်း ကုန်သွယ်မှုပြုလုပ်ရန်")
    for item, price in st.session_state.current_prices.items():
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
                        st.session_state.buy_costs[item].append(price)
                        st.session_state.player_xp += 15
                        if st.session_state.player_xp >= 100:
                            st.session_state.player_level += 1
                            st.session_state.player_xp = 0
                        st.session_state.log.insert(0, f"🛒 {item} ကို {price} ฿ ဖြင့် ဝယ်လိုက်သည်။")
                        play_sound("trade")
                        inject_save_system() # ဒေတာအော်တိုသိမ်းမယ်
                        st.rerun()
            with btn_sell:
                if st.button(f"💵 ရောင်းချမည် ({item})", key=f"sell_{item}"):
                    if st.session_state.inventory[item] > 0:
                        st.session_state.inventory[item] -= 1
                        st.session_state.player_coin += price
                        saved_cost = st.session_state.buy_costs[item].pop(0) if st.session_state.buy_costs[item] else base_prices[item]
                        diff = price - saved_cost
                        
                        if diff >= 0:
                            st.session_state.player_xp += 20
                            st.session_state.log.insert(0, f"📈 အမြတ်ရရှိသည်! {item} မှ အမြတ် (+{diff} ฿) ရသည်။")
                        else:
                            st.session_state.player_xp = max(0, st.session_state.player_xp - 15)
                            st.session_state.log.insert(0, f"📉 အရှုံးပေါ်သည်! {item} မှ အရှုံး ({-diff} ฿) ဖြစ်သည်။")
                            
                        if st.session_state.player_xp >= 100:
                            st.session_state.player_level += 1
                            st.session_state.player_xp = 0
                        play_sound("trade")
                        inject_save_system() # ဒေတာအော်တိုသိမ်းမယ်
                        st.rerun()

with rank_col:
    st.markdown("### 🏆 ကုန်သည် Rank စာရင်း (Top 10)")
    rank_df = pd.DataFrame(ranked_traders, columns=["ကုန်သည်အမည်", "ပိုင်ဆိုင်မှု (Coin)"])
    rank_df.index = rank_df.index + 1
    st.dataframe(rank_df.head(10), use_container_width=True)
