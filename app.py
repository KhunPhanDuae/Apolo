import streamlit as st
import random
import pandas as pd
import json
import base64

# Page configuration
st.set_page_config(page_title="Cyber Live Market Tycoon Pro", page_icon="📈", layout="wide")

st.logo("https://assets.mixkit.co/active_storage/sfx/2019/2019-84.wav") # dummy load
st.fragment(run_every="2s")

# --- PREMIUM CYBER DARK STYLE ---
st.markdown("""
<style>
    .stApp { background-color: #0B0C10; color: #C5C6C7; }
    h1, h2, h3, h4 { color: #66FCF1 !important; font-family: 'Courier New', monospace; }
    .stat-box { background: #1F2833; color: #fff; padding: 10px; border-radius: 10px; text-align: center; font-weight: bold; border: 1px solid #45A29E; }
    .game-card { background-color: #1F2833; padding: 15px; border-radius: 12px; border: 1px solid #45A29E; margin-bottom: 10px; }
    .stButton>button { background: linear-gradient(135deg, #45A29E 0%, #1F2833 100%); color: #66FCF1 !important; border: 1px solid #66FCF1 !important; border-radius: 8px; font-weight: bold; width: 100%; }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if 'player_coin' not in st.session_state: st.session_state.player_coin = 1000
if 'player_level' not in st.session_state: st.session_state.player_level = 1
if 'player_xp' not in st.session_state: st.session_state.player_xp = 0
if 'gold' not in st.session_state: st.session_state.gold = 1
if 'silver' not in st.session_state: st.session_state.silver = 10
if 'inventory' not in st.session_state: st.session_state.inventory = {"ဖုန်း": 0, "ရွှေထည်": 0, "စားသောက်ကုန်": 0}
if 'buy_costs' not in st.session_state: st.session_state.buy_costs = {"ဖုန်း": [], "ရွှေထည်": [], "စားသောက်ကုန်": []}
if 'log' not in st.session_state: st.session_state.log = ["🤖 စနစ်များအားလုံး တိကျသေချာစွာ စတင်လိုက်ပါပြီ။"]

if 'competitors' not in st.session_state:
    names = ["Somchai", "Thana", "Anong", "Kitti", "Malai", "Narong", "Pravat", "Somsak", "Viroj", "Chai"]
    st.session_state.competitors = {name: random.randint(800, 1500) for name in names}

# --- SAVE / LOAD LOGIC (ဒေတာ သိမ်းဆည်း/ပြန်ယူခြင်း စနစ်) ---
def generate_save_code():
    data = {
        "coin": st.session_state.player_coin,
        "level": st.session_state.player_level,
        "xp": st.session_state.player_xp,
        "gold": st.session_state.gold,
        "silver": st.session_state.silver,
        "inventory": st.session_state.inventory,
        "buy_costs": st.session_state.buy_costs
    }
    # JSON ကို စာသားကုဒ်ပြောင်းပစ်ခြင်း
    json_str = json.dumps(data)
    b64_code = base64.b64encode(json_str.encode()).decode()
    return b64_code

def load_save_code(code):
    try:
        json_str = base64.b64decode(code.encode()).decode()
        data = json.loads(json_str)
        st.session_state.player_coin = data["coin"]
        st.session_state.player_level = data["level"]
        st.session_state.player_xp = data["xp"]
        st.session_state.gold = data["gold"]
        st.session_state.silver = data["silver"]
        st.session_state.inventory = data["inventory"]
        st.session_state.buy_costs = data["buy_costs"]
        return True
    except:
        return False

# --- AUTO MARKET LOGIC ---
base_prices = {"ဖုန်း": 800, "ရွှေထည်": 1500, "စားသောက်ကုန်": 40}
if 'current_prices' not in st.session_state: st.session_state.current_prices = base_prices.copy()

if random.random() < 0.3:
    for item in base_prices.keys():
        st.session_state.current_prices[item] = int(base_prices[item] * random.uniform(0.6, 1.7))
    for comp in st.session_state.competitors:
        st.session_state.competitors[comp] += random.randint(-40, 60)

# Rank calculation
all_traders = {"သင် (Player)": st.session_state.player_coin}
for name, cash in st.session_state.competitors.items(): all_traders[name] = cash
ranked_traders = sorted(all_traders.items(), key=lambda x: x[1], reverse=True)
player_rank = [i for i, x in enumerate(ranked_traders) if x[0] == "သင် (Player)"][0] + 1

# --- UI MAIN ---
st.title("⚡ Cyber Live Market Tycoon Pro")

# Stats Bar
col1, col2, col3, col4 = st.columns(4)
with col1: st.markdown(f"<div class='stat-box'>🌟 LEVEL: {st.session_state.player_level} (XP: {st.session_state.player_xp}/100)</div>", unsafe_allow_html=True)
with col2: st.markdown(f"<div class='stat-box'>💵 COIN: {st.session_state.player_coin} ฿</div>", unsafe_allow_html=True)
with col3: st.markdown(f"<div class='stat-box'>🏆 RANK: #{player_rank}</div>", unsafe_allow_html=True)
with col4: st.markdown(f"<div class='stat-box'>🎒 ဝင်ငွေ/ပစ္စည်း: {st.session_state.inventory}</div>", unsafe_allow_html=True)

# Game & Trade Columns
game_col, rank_col = st.columns([2, 1])
with game_col:
    st.markdown("### 🏪 ကုန်သွယ်မှုပြုလုပ်ရန်")
    for item, price in st.session_state.current_prices.items():
        costs = st.session_state.buy_costs[item]
        avg_text = f"{int(sum(costs)/len(costs))} ฿" if costs else "မရှိသေးပါ"
        st.markdown(f"<div class='game-card'>📦 <b>{item}</b> — စျေး: {price} ฿ | အဝယ်ရင်းနှီးစျေး: {avg_text}</div>", unsafe_allow_html=True)
        
        b_col, s_col = st.columns(2)
        with b_col:
            if st.button(f"🛒 ဝယ် {item}", key=f"b_{item}"):
                if st.session_state.player_coin >= price:
                    st.session_state.player_coin -= price
                    st.session_state.inventory[item] += 1
                    st.session_state.buy_costs[item].append(price)
                    st.session_state.player_xp += 15
                    if st.session_state.player_xp >= 100:
                        st.session_state.player_level += 1
                        st.session_state.player_xp = 0
                    st.rerun()
        with s_col:
            if st.button(f"💵 ရောင်း {item}", key=f"s_{item}"):
                if st.session_state.inventory[item] > 0:
                    st.session_state.inventory[item] -= 1
                    st.session_state.player_coin += price
                    st.session_state.player_xp += 20
                    if st.session_state.player_xp >= 100:
                        st.session_state.player_level += 1
                        st.session_state.player_xp = 0
                    st.rerun()

with rank_col:
    st.markdown("### 🏆 Top 10 Traders")
    rank_df = pd.DataFrame(ranked_traders, columns=["ကုန်သည်အမည်", "ပိုင်ဆိုင်မှု"])
    st.dataframe(rank_df.head(10), use_container_width=True)

# --- 💾 ဒေတာ ထိန်းသိမ်းရေး ဂိတ် (SAVE / LOAD INTERFACE) ---
st.write("---")
st.markdown("### 💾 ဒေတာ ထိန်းသိမ်းရေး ဂိတ်")
save_col, load_col = st.columns(2)

with save_col:
    st.write("ဂိမ်းပိတ်ခါနီးလျှင် ဤခလုတ်ကိုနှိပ်၍ ကုဒ်ကိုသိမ်းထားပါ")
    if st.button("📝 သိမ်းဆည်းမည့် 'စာသားကုဒ်' ထုတ်ယူမည်"):
        code = generate_save_code()
        st.text_area("သင်၏ ဂိမ်းကုဒ် (၎င်းကို Copy ကူးပြီး .txt ထဲ သိမ်းထားပါ) :", value=code, height=70)

with load_col:
    st.write("နောက်တစ်ခါပြန်ဝင်လျှင် ကုဒ်ကိုဒီမှာပြန်ထည့်ပါ")
    input_code = st.text_input("သိမ်းဆည်းထားသော ကုဒ်ကို ဤနေရာတွင် ထည့်ပါ:")
    if st.button("📥 ဂိမ်းဒေတာ ပြန်လည်ရယူမည် (Load)"):
        if input_code:
            success = load_save_code(input_code)
            if success:
                st.success("🎉 အရင်ဆော့ထားသည့်နေရာအတိုင်း ဒေတာပြန်ပွင့်လာပါပြီ။")
                st.rerun()
            else:
                st.error("❌ ကုဒ်မှားယွင်းနေပါသည်။")
