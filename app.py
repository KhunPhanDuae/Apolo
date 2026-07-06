import streamlit as st
import random
import pandas as pd

# Page configuration
st.set_page_config(page_title="Accurate Market Tycoon", page_icon="📈", layout="wide")

# --- Streamlit Auto Refresh (ဒေတာမရှုပ်ထွေးစေဘဲ စျေးကွက်ကိုပဲ အော်တိုပြောင်းလဲစေမည့်စနစ်) ---
st.logo("https://assets.mixkit.co/active_storage/sfx/2019/2019-84.wav") # Dummy
st.fragment(run_every="3s")

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
        "trade": "https://assets.mixkit.co/active_storage/sfx/2019/2019-84.wav",
        "win": "https://assets.mixkit.co/active_storage/sfx/1435/1435-84.wav"
    }
    if sound_type in sound_urls:
        st.components.v1.html(f"""<audio autoplay><source src="{sound_urls[sound_type]}" type="audio/wav"></audio>""", height=0, width=0)

# --- GAME STATE INITIALIZATION (ဒေတာများ ပျောက်မကုန်စေရန် သေချာထိန်းသိမ်းခြင်း) ---
if 'player_coin' not in st.session_state: st.session_state.player_coin = 1000
if 'player_level' not in st.session_state: st.session_state.player_level = 1
if 'inventory' not in st.session_state: st.session_state.inventory = {"ဖုန်း": 0, "ရွှေထည်": 0, "စားသောက်ကုန်": 0}
if 'buy_prices' not in st.session_state: st.session_state.buy_prices = {"ဖုန်း": 0, "ရွှေထည်": 0, "စားသောက်ကုန်": 0} # ဝယ်စျေးမှတ်ရန်
if 'last_profit_loss' not in st.session_state: st.session_state.last_profit_loss = "" # နောက်ဆုံးရလဒ်ပြရန်
if 'log' not in st.session_state: st.session_state.log = ["🤖 စနစ်သစ်- စျေးကွက်ဒေတာများကို တိကျစွာ စတင်တွက်ချက်နေပါပြီ။"]

# ပြိုင်ဘက် ၃၀ ဦးစာရင်း
if 'competitors' not in st.session_state:
    names = [
        "Somchai", "Thana", "Anong", "Kitti", "Malai", "Narong", "Pravat", "Somsak", "Viroj", "Chai",
        "Arun", "Boon-Mee", "Can", "Daeng", "Erawan", "Kamal", "Lawan", "Mee", "Noi", "Pim",
        "Rung", "Sakda", "Siri", "Suchart", "Sunan", "Surachai", "Teerachai", "Ubon", "Wanchai", "Yod"
    ]
    st.session_state.competitors = {name: random.randint(500, 1500) for name in names}

# --- AUTOMATIC MARKET ENGINE (အော်တို စျေးကွက်ပြောင်းလဲမှု) ---
base_prices = {"ဖုန်း": 800, "ရွှေထည်": 1500, "စားသောက်ကုန်": 40}

# ရွေးချယ်မှုအလိုက် ပေါက်စျေးများ အမြဲတမ်းပြောင်းလဲနေစေရန်
if 'current_prices' not in st.session_state or random.random() < 0.4:
    st.session_state.current_prices = {item: int(base * random.uniform(0.6, 1.7)) for item, base in base_prices.items()}
    # ပြိုင်ဘက်များကိုလည်း အော်တိုပိုက်ဆံ အတက်အကျဖြစ်စေရန်
    for comp in st.session_state.competitors:
        st.session_state.competitors[comp] += random.randint(-40, 60)
        if st.session_state.competitors[comp] < 100: st.session_state.competitors[comp] = 100

current_prices = st.session_state.current_prices

# --- LEADERBOARD & RANK တွက်ချက်ခြင်း ---
all_traders = {"သင် (Player)": st.session_state.player_coin}
for name, cash in st.session_state.competitors.items():
    all_traders[name] = cash

ranked_traders = sorted(all_traders.items(), key=lambda x: x[1], reverse=True)
player_rank = [i for i, x in enumerate(ranked_traders) if x[0] == "သင် (Player)"][0] + 1

# အဆင့် Level ကို ပိုင်ဆိုင်မှု Coin ပေါ်မူတည်ပြီး မှန်မှန်ကန်ကန် တက်/ကျ လုပ်ပေးခြင်း
old_level = st.session_state.player_level
st.session_state.player_level = max(1, int(st.session_state.player_coin / 1000) + 1)
if st.session_state.player_level > old_level:
    st.session_state.log.insert(0, f"🎉 ဂုဏ်ယူပါသည်! သင်၏စီးပွားရေးတိုးတက်မှုကြောင့် အဆင့် LEVEL {st.session_state.level} သို့ တက်လှမ်းသွားပါပြီ။")
elif st.session_state.player_level < old_level:
    st.session_state.log.insert(0, f"📉 သတိပေးချက်- သင်၏ပိုင်ဆိုင်မှုကျဆင်းသွားသဖြင့် အဆင့် LEVEL {st.session_state.level} သို့ ပြန်ကျသွားသည်။")

# --- HEADER UI ---
st.title("⚡ Cyber Live Market Tycoon (Pro Edition)")
st.markdown("🌐 *ဒေတာများနှင့် ပိုက်ဆံအဝင်အထွက်ကို ရာနှုန်းပြည့် တိကျစွာ ပြင်ဆင်ထားသော ဗားရှင်းဖြစ်ပါသည်။*")
st.write("---")

# --- PLAYER STATS BAR ---
col1, col2, col3, col4 = st.columns(4)
with col1: st.markdown(f"<div class='stat-box' style='color:#66FCF1;'>🌟 LEVEL<br><span style='font-size:22px;'>{st.session_state.player_level}</span></div>", unsafe_allow_html=True)
with col2: st.markdown(f"<div class='stat-box' style='color:#00F0FF;'>💵 သင်၏ပိုက်ဆံ (Coin)<br><span style='font-size:22px;'>{st.session_state.player_coin} ฿</span></div>", unsafe_allow_html=True)
with col3: st.markdown(f"<div class='stat-box' style='color:#FFD700;'>🏆 လက်ရှိ RANK<br><span style='font-size:22px;'>#{player_rank} / 31</span></div>", unsafe_allow_html=True)
with col4: 
    inv_txt = " | ".join([f"{k}:{v}" for k, v in st.session_state.inventory.items()])
    st.markdown(f"<div class='stat-box' style='color:#00FF00; font-size:12px;'>🎒 သင်၏ဂိုဒေါင်ပစ္စည်း<br><span>{inv_txt if inv_text else 'ဗလာ'}</span></div>", unsafe_allow_html=True)

# ပြကွက်အသစ်- နောက်ဆုံးအရောင်းအဝယ်မှ အမြတ်/အရှုံးကို အပေါ်မှာ အထူးဖော်ပြပေးခြင်း
if st.session_state.last_profit_loss:
    st.markdown(st.session_state.last_profit_loss, unsafe_allow_html=True)

st.write("")

# --- MAIN LAYOUT ---
game_col, rank_col = st.columns([2, 1])

with game_col:
    st.markdown("### 🏪 Live Cyber Market")
    
    for item, price in current_prices.items():
        with st.container():
            # ကစားသမား ဝယ်ထားတဲ့ မူရင်းစျေးနှုန်းကို ပြသပေးခြင်း
            bought_at = st.session_state.buy_prices[item]
            bought_text = f" (သင်ဝယ်ထားသည့်စျေး: {bought_at} ฿)" if st.session_state.inventory[item] > 0 else ""
            
            st.markdown(f"""
            <div class='game-card'>
                <span style='font-size:18px; font-weight:bold;'>📦 {item}</span> — 
                လက်ရှိစျေးကွက်ပေါက်စျေး: <span style='color:#66FCF1; font-weight:bold;'>{price} ฿</span> 
                <span style='font-size:12px; color:#aaa;'>{bought_text}</span>
            </div>
            """, unsafe_allow_html=True)
            
            btn_buy, btn_sell = st.columns(2)
            with btn_buy:
                if st.button(f"🛒 {item} ကို ဝယ်ယူမည်", key=f"b_{item}"):
                    if st.session_state.player_coin >= price:
                        st.session_state.player_coin -= price # ပိုက်ဆံကို ချက်ချင်းနုတ်ယူသည်
                        st.session_state.inventory[item] += 1
                        st.session_state.buy_prices[item] = price # ဝယ်စျေးကို တိကျစွာမှတ်သားသည်
                        st.session_state.log.insert(0, f"🛒 {item} ကို {price} ฿ ဖြင့် အဝယ်သွင်းခဲ့သည်။")
                        play_sound("trade")
                        st.render() # ချက်ချင်း မျက်နှာပြင်ကို Update လုပ်သည်
            with btn_sell:
                if st.button(f"💵 {item} ကို ပြန်ရောင်းမည်", key=f"s_{item}"):
                    if st.session_state.inventory[item] > 0:
                        st.session_state.inventory[item] -= 1
                        st.session_state.player_coin += price # ပိုက်ဆံ ချက်ချင်းပေါင်းထည့်သည်
                        
                        # အမြတ် သို့မဟုတ် အရှုံး အတိအကျ တွက်ချက်ခြင်း
                        cost = st.session_state.buy_prices[item]
                        profit_or_loss = price - cost
                        
                        if profit_or_loss > 0:
                            st.session_state.last_profit_loss = f"<div style='background-color:#1c3d27; color:#2ecc71; padding:10px; border-radius:5px; text-align:center; font-weight:bold;'>📈 အရောင်းအဝယ်ရလဒ်- အမြတ်ရပါသည်! (+{profit_or_loss} ฿)</div>"
                        elif profit_or_loss < 0:
                            st.session_state.last_profit_loss = f"<div style='background-color:#4a1c1c; color:#e74c3c; padding:10px; border-radius:5px; text-align:center; font-weight:bold;'>📉 အရောင်းအဝယ်ရလဒ်- အရှုံးပေါ်ပါသည်! ({profit_or_loss} ฿)</div>"
                        else:
                            st.session_state.last_profit_loss = "<div style='background-color:#333; color:#fff; padding:10px; border-radius:5px; text-align:center;'>⚖️ အရောင်းအဝယ်ရလဒ်- အရှုံးအမြတ်မရှိ ကာမိရုံသာ။</div>"
                        
                        st.session_state.log.insert(0, f"💵 {item} ကို {price} ฿ ဖြင့် ပြန်လည်ရောင်းချခဲ့သည်။")
                        play_sound("trade")
                        st.render()
            st.write("")

    st.markdown("### 📜 ကုန်သွယ်မှုမှတ်တမ်းအတို")
    for l in st.session_state.log[:2]:
        st.caption(l)

with rank_col:
    st.markdown("### 🏆 Top 10 Traders")
    rank_df = pd.DataFrame(ranked_traders, columns=["ကုန်သည်အမည်", "ပိုင်ဆိုင်မှု (Coin)"])
    rank_df.index = rank_df.index + 1
    st.dataframe(rank_df.head(10), use_container_width=True)
    st.markdown(f"**သင့်အဆင့်:** `#{player_rank}` နေရာမှာ အပြိုင်အဆိုင် ရှိနေပါတယ်။")
