import streamlit as st
import random
import pandas as pd

# Page configuration
st.set_page_config(page_title="Auto Market Tycoon", page_icon="📈", layout="wide")

# --- Streamlit Auto Refresh (ဘာမှမနှိပ်လဲ အော်တိုလည်ပတ်စေရန်) ---
# ၂ စက္ကန့်တိုင်းမှာ ဂိမ်းကို အော်တို Refresh လုပ်ပြီး စျေးကွက်နဲ့ ပြိုင်ဘက်တွေကို လှုပ်ရှားစေပါတယ်
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
        "lose": "https://assets.mixkit.co/active_storage/sfx/2622/2622-84.wav"
    }
    if sound_type in sound_urls:
        st.components.v1.html(f"""<audio autoplay><source src="{sound_urls[sound_type]}" type="audio/wav"></audio>""", height=0, width=0)

# --- GAME STATE INITIALIZATION ---
if 'player_coin' not in st.session_state: st.session_state.player_coin = 1000
if 'player_level' not in st.session_state: st.session_state.player_level = 1
if 'inventory' not in st.session_state: st.session_state.inventory = {"ဖုန်း": 0, "ရွှေထည်": 0, "စားသောက်ကုန်": 0}
if 'log' not in st.session_state: st.session_state.log = ["🤖 စျေးကွက် အလိုအလျောက် ပတ်ဝန်းကျင် စတင်ပါပြီ။"]

# ပြိုင်ဘက် ကုန်သည် ၃၀ ဦး စာရင်း (Leaderboard အတွက် အစောပိုင်း သတ်မှတ်ချက်)
if 'competitors' not in st.session_state:
    names = [
        "Somchai", "Thana", "Anong", "Kitti", "Malai", "Narong", "Pravat", "Somsak", "Viroj", "Chai",
        "Arun", "Boon-Mee", "Can", "Daeng", "Erawan", "Kamal", "Lawan", "Mee", "Noi", "Pim",
        "Rung", "Sakda", "Siri", "Suchart", "Sunan", "Surachai", "Teerachai", "Ubon", "Wanchai", "Yod"
    ]
    st.session_state.competitors = {name: random.randint(500, 1500) for name in names}

# --- AUTOMATIC MARKET FLUCTUATION (အော်တိုပြောင်းလဲမှုစနစ်) ---
# ကစားသမား ဘာမှမနှိပ်ရင်တောင် ဤနေရာက ကုဒ်တွေကြောင့် စျေးနှုန်းနဲ့ ပြိုင်ဘက်ပိုက်ဆံတွေ အမြဲအော်တို ပြောင်းနေမှာပါ
base_prices = {"ဖုန်း": 800, "ရွှေထည်": 1500, "စားသောက်ကုန်": 40}
price_modifiers = {item: random.uniform(0.5, 1.8) for item in base_prices.keys()}
current_prices = {item: int(base * price_modifiers[item]) for item, base in base_prices.items()}

# ပြိုင်ဘက်များလည်း အနောက်ကွယ်မှာ အော်တို စီးပွားရေးလုပ်ပြီး ပိုက်ဆံတက်/ကျဖြစ်နေစေရန်
for comp in st.session_state.competitors:
    st.session_state.competitors[comp] += random.randint(-50, 80)
    if st.session_state.competitors[comp] < 100: st.session_state.competitors[comp] = 100

# --- LEADERBOARD RANKING တွက်ချက်ခြင်း ---
all_traders = {"သင် (Player)": st.session_state.player_coin}
for name, cash in st.session_state.competitors.items():
    all_traders[name] = cash

# ပိုက်ဆံအများဆုံးလူကို Rank 1 ပေးပြီး စီလိုက်ခြင်း
ranked_traders = sorted(all_traders.items(), key=lambda x: x[1], reverse=True)
player_rank = [i for i, x in enumerate(ranked_traders) if x[0] == "သင် (Player)"][0] + 1

# Player ရဲ့ Level ကို ပိုက်ဆံအလိုက် အော်တို သတ်မှတ်ပေးခြင်း
st.session_state.player_level = max(1, int(st.session_state.player_coin / 1000) + 1)

# --- HEADER UI ---
st.title("⚡ Cyber Live Market Tycoon")
st.markdown("🌐 *ဂိမ်းသည် အချိန်နှင့်အမျှ အော်တိုလည်ပတ်နေပါသည်။ သင်သည် စျေးကွက်ကို စောင့်ကြည့်ပြီး အချိန်ကိုက် ဝင်ရောက်စွက်ဖက်ရုံရုံသာ။*")
st.write("---")

# --- PLAYER STATS BAR ---
col1, col2, col3, col4 = st.columns(4)
with col1: st.markdown(f"<div class='stat-box' style='color:#66FCF1;'>🌟 LEVEL<br><span style='font-size:22px;'>{st.session_state.player_level}</span></div>", unsafe_allow_html=True)
with col2: st.markdown(f"<div class='stat-box' style='color:#00F0FF;'>💵 သင်၏ပိုက်ဆံ<br><span style='font-size:22px;'>{st.session_state.player_coin} ฿</span></div>", unsafe_allow_html=True)
with col3: st.markdown(f"<div class='stat-box' style='color:#FFD700;'>🏆 လက်ရှိ RANK<br><span style='font-size:22px;'>#{player_rank} / 31</span></div>", unsafe_allow_html=True)
with col4: 
    inv_txt = " | ".join([f"{k}:{v}" for k, v in st.session_state.inventory.items()])
    st.markdown(f"<div class='stat-box' style='color:#00FF00; font-size:12px;'>🎒 သင်၏ဂိုဒေါင်ပစ္စည်း<br><span>{inv_txt}</span></div>", unsafe_allow_html=True)

st.write("")

# --- MAIN LAYOUT (ဘယ်ဘက်မှာ ကစားကွင်း၊ ညာဘက်မှာ Rank စာရင်း) ---
game_col, rank_col = st.columns([2, 1])

with game_col:
    st.markdown("### 🏪 Live Cyber Market (ဝင်ရောက်စွက်ဖက်ရန် နယ်မြေ)")
    
    # ပစ္စည်းတစ်ခုချင်းစီရဲ့ အချိန်မှန် အတက်အကျပြကွက်
    for item, price in current_prices.items():
        with st.container():
            st.markdown(f"""
            <div class='game-card'>
                <span style='font-size:18px; font-weight:bold;'>📦 {item}</span> — 
                လက်ရှိစျေး: <span style='color:#66FCF1; font-weight:bold;'>{price} ฿</span> 
                <span style='font-size:12px; color:#aaa;'>(မူရင်းရင်းနှီးစျေး: {base_prices[item]} ฿)</span>
            </div>
            """, unsafe_allow_html=True)
            
            btn_buy, btn_sell = st.columns(2)
            with btn_buy:
                if st.button(f"🛒 {item} ကို ဝယ်ယူမည် (Buy)", key=f"buy_{item}"):
                    if st.session_state.player_coin >= price:
                        st.session_state.player_coin -= price
                        st.session_state.inventory[item] += 1
                        st.session_state.log.insert(0, f"🛒 သင်သည် {item} ကို {price} ฿ ဖြင့် ဝယ်ယူ စွက်ဖက်ခဲ့သည်။")
                        play_sound("trade")
                        st.rerun()
            with btn_sell:
                if st.button(f"💵 {item} ကို ရောင်းချမည် (Sell)", key=f"sell_{item}"):
                    if st.session_state.inventory[item] > 0:
                        st.session_state.inventory[item] -= 1
                        st.session_state.player_coin += price
                        diff = price - base_prices[item]
                        st.session_state.log.insert(0, f"📈 သင်သည် {item} ကို ရောင်းချပြီး အမြတ်/အရှုံး ({diff} ฿) ယူခဲ့သည်။")
                        play_sound("trade")
                        st.rerun()
            st.write("")

    # --- LIVE LOGS ---
    st.markdown("### 📜 Live ဖြစ်ရပ်မှတ်တမ်း")
    for l in st.session_state.log[:3]:
        st.caption(l)

with rank_col:
    st.markdown("### 🏆 Top 10 Traders (Rank စာရင်း)")
    # Rank ဇယားကို DataFrame နဲ့ လှလှပပ ဖော်ပြခြင်း
    rank_df = pd.DataFrame(ranked_traders, columns=["ကုန်သည်အမည်", "ပိုင်ဆိုင်မှု (Coin)"])
    rank_df.index = rank_df.index + 1
    st.dataframe(rank_df.head(10), use_container_width=True)
    
    st.markdown(f"**သင့်အဆင့်:** Rank `#{player_rank}` တွင် ရှိနေပြီး ပြိုင်ဘက် ၃၀ ဦးနှင့် အားပြိုင်နေရသည်။")
