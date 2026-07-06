import streamlit as st
import random

# Page configuration
st.set_page_config(page_title="Thai Market & RPG Game", page_icon="⚔️", layout="wide")

# CSS for styling
st.markdown("""
<style>
    .stat-box {
        background-color: #1E1E2F;
        color: #FFFFFF;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
    }
    .game-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        border-top: 5px solid #FF4B4B;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State for Game variables
if 'level' not in st.session_state: st.session_state.level = 1
if 'exp' not in st.session_state: st.session_state.exp = 0
if 'coin' not in st.session_state: st.session_state.coin = 500
if 'gold' not in st.session_state: st.session_state.gold = 0
if 'silver' not in st.session_state: st.session_state.silver = 5
if 'inventory_bag' not in st.session_state: st.session_state.inventory_bag = {"အိတ်": 0, "ဖိနပ်": 0, "အလှကုန်": 0}
if 'log' not in st.session_state: st.session_state.log = ["ဂိမ်းစတင်ပါပြီ။ စွန့်စားခန်းထွက်ပြီး ပိုက်ဆံရှာပါ။"]

# Market Prices (Changes dynamically a bit)
prices = {"အိတ်": 150, "ဖိနပ်": 100, "အလှကုန်": 80}

def add_log(text):
    st.session_state.log.insert(0, text)
    if len(st.session_state.log) > 5:
        st.session_state.log.pop()

def check_levelup():
    exp_needed = st.session_state.level * 100
    if st.session_state.exp >= exp_needed:
        st.session_state.level += 1
        st.session_state.exp -= exp_needed
        add_log(f"🎉 ဂုဏ်ယူပါသည်။ အဆင့် (Level) {st.session_state.level} သို့ တက်လှမ်းသွားပါပြီ။")

# --- HEADER ---
st.title("⚔️ RPG Adventure & Thai Trading Game")
st.write("စျေးကွက်ရှာဖွေရင်း စွန့်စားခန်းဖွင့်ပြီး အချမ်းသာဆုံး ကုန်သည်ကြီး ဖြစ်အောင်လုပ်ပါ။")

# --- MAIN NAVIGATION TABS ---
tab1, tab2, tab3 = st.tabs(["🎮 ဂိမ်းကစားကွင်း (RPG & Trade)", "📊 Market Research (စျေးကွက်ကြည့်ရန်)", "📚 ဂိမ်းလမ်းညွှန်"])

# ----------------------------------------------------
# TAB 1: THE GAME
# ----------------------------------------------------
with tab1:
    # --- STATS BAR ---
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1: st.markdown(f"<div class='stat-box' style='border-bottom: 4px solid #FFD700;'>🌟 အဆင့် (Level)<br><span style='font-size:20px;'>{st.session_state.level}</span> (XP: {st.session_state.exp})</div>", unsafe_allow_html=True)
    with col2: st.markdown(f"<div class='stat-box' style='border-bottom: 4px solid #00F0FF;'>💵 ပိုက်ဆံ (Coin)<br><span style='font-size:20px;'>{st.session_state.coin} ฿</span></div>", unsafe_allow_html=True)
    with col3: st.markdown(f"<div class='stat-box' style='border-bottom: 4px solid #FFAA00;'>🟡 ရွှေ (Gold)<br><span style='font-size:20px;'>{st.session_state.gold} တုံး</span></div>", unsafe_allow_html=True)
    with col4: st.markdown(f"<div class='stat-box' style='border-bottom: 4px solid #C0C0C0;'>⚪ ငွေ (Silver)<br><span style='font-size:20px;'>{st.session_state.silver} ပြား</span></div>", unsafe_allow_html=True)
    with col5: st.markdown(f"<div class='stat-box' style='border-bottom: 4px solid #00FF00;'>🎒 ထုပ်ပိုးအိတ်<br><span style='font-size:14px;'>အိတ်:{st.session_state.inventory_bag['အိတ်']} | ဖိနပ်:{st.session_state.inventory_bag['ဖိနပ်']} | အလှကုန်:{st.session_state.inventory_bag['အလှကုန်']}</span></div>", unsafe_allow_html=True)

    st.write("")

    # --- GAME ACTIONS ---
    col_act1, col_act2, col_act3 = st.columns(3)

    with col_act1:
        st.markdown("<div class='game-card'><h3>🔍 ရှာဖွေခြင်း (Scouting)</h3><p>ထိုင်းစျေးကွက်ထဲ လှည့်လည်ပြီး ပစ္စည်းနဲ့ ငွေပြားများ ရှာဖွေမယ်</p></div>", unsafe_allow_html=True)
        if st.button("🗺️ စျေးကွက်ထဲ လည်ပတ်ရှာဖွေရန်"):
            loot = random.choice(["coin", "silver", "item", "nothing"])
            xp_gain = random.randint(10, 20)
            st.session_state.exp += xp_gain
            
            if loot == "coin":
                amt = random.randint(50, 100)
                st.session_state.coin += amt
                add_log(f"🔍 စျေးကွက်ထဲတွင် ပိုက်ဆံ {amt} ဘတ် ကောက်ရခဲ့သည်။ (+{xp_gain} XP)")
            elif loot == "silver":
                st.session_state.silver += 1
                add_log(f"🔍 စျေးကွက်ထဲတွင် ငွေပြား ၁ ပြား တွေ့ရှိခဲ့သည်။ (+{xp_gain} XP)")
            elif loot == "item":
                itm = random.choice(["အိတ်", "ဖိနပ်", "အလှကုန်"])
                st.session_state.inventory_bag[itm] += 1
                add_log(f"🔍 စျေးကွက်ထဲတွင် ရောင်းကုန် တန်ဖိုးရှိ [{itm}] တိုက်ရိုက်ရရှိခဲ့သည်။ (+{xp_gain} XP)")
            else:
                add_log(f"🔍 စျေးကွက်ထဲ လည်ပတ်သော်လည်း ဘာမှမတွေ့ခဲ့ပါ။ (+{xp_gain} XP)")
            check_levelup()
            st.rerun()

    with col_act2:
        st.markdown("<div class='game-card'><h3>⚔️ စွန့်စားတိုက်ခိုက်ခြင်း (Adventure)</h3><p>တောတွင်းက သားရဲတွေနဲ့ စျေးကွက်ဖျက်ဆီးသူတွေကို တိုက်ခိုက်ပြီး ရွှေရှာမယ်</p></div>", unsafe_allow_html=True)
        if st.button("⚔️ စွန့်စားခန်းထွက် တိုက်ခိုက်ရန်"):
            win = random.choice([True, True, False]) # 66% chance to win
            xp_gain = random.randint(25, 40)
            st.session_state.exp += xp_gain
            
            if win:
                gold_gain = random.randint(1, 2)
                coin_gain = random.randint(100, 200)
                st.session_state.gold += gold_gain
                st.session_state.coin += coin_gain
                add_log(f"⚔️ တိုက်ပွဲနိုင်ခဲ့သည်။ ရွှေ {gold_gain} တုံးနှင့် ပိုက်ဆံ {coin_gain} ဘတ် ရရှိသည်။ (+{xp_gain} XP)")
            else:
                lost_coin = random.randint(30, 60)
                st.session_state.coin = max(0, st.session_state.coin - lost_coin)
                add_log(f"💀 တိုက်ပွဲရှုံးနိမ့်ပြီး ဒဏ်ရာရခဲ့သည်။ ကုသစရိတ် {lost_coin} ဘတ် ကုန်ကျသည်။ (+{xp_gain} XP)")
            check_levelup()
            st.rerun()

    with col_act3:
        st.markdown("<div class='game-card'><h3>🏪 အရောင်းအဝယ်လုပ်ခြင်း (Trading)</h3><p>ရရှိထားတဲ့ ပစ္စည်းတွေကို ပြန်ရောင်းချပြီး Coin အဖြစ် ပြောင်းလဲမယ်</p></div>", unsafe_allow_html=True)
        st.write(f"💰 **လက်ရှိပေါက်စျေး:** အိတ်({prices['အိတ်']}฿) | ဖိနပ်({prices['ဖိနပ်']}฿) | အလှကုန်({prices['အလှကုန်']}฿)")
        
        for item, price in prices.items():
            if st.session_state.inventory_bag[item] > 0:
                if st.button(f"💵 {item} (၁) ခု ရောင်းမည်"):
                    st.session_state.inventory_bag[item] -= 1
                    st.session_state.coin += price
                    add_log(f"🏪 {item} ကို ပေါက်စျေး {price} ဘတ်ဖြင့် ရောင်းချလိုက်သည်။")
                    st.rerun()
        
        st.write("---")
        st.caption("ရွှေ/ငွေ လဲလှယ်ခန်း")
        if st.session_state.silver >= 10:
            if st.button("⚪ ငွေပြား ၁၀ ပြား ➡️ ရွှေ ၁ တုံး လဲမည်"):
                st.session_state.silver -= 10
                st.session_state.gold += 1
                add_log("🪙 ငွေပြားများကို ရွှေတုံးအဖြစ် လဲလှယ်လိုက်သည်။")
                st.rerun()

    # --- GAME LOG SCREEN ---
    st.markdown("### 📜 လုပ်ဆောင်ချက် မှတ်တမ်း (Game Logs)")
    for l in st.session_state.log:
        st.text(l)

# ----------------------------------------------------
# TAB 2: ORIGINAL MARKET RESEARCH TOOL
# ----------------------------------------------------
with tab2:
    st.subheader("📊 ပုံမှန် စျေးကွက်စောင့်ကြည့်ရေး ဧရိယာ")
    st.info("ဂိမ်းဆော့ရင်း အပြင်က တကယ့် ထိုင်းစျေးကွက် Keywords တွေကို ဒီမှာ စမ်းသပ်ရှာဖွေနိုင်ပါတယ်")
    
    keyword_input = st.text_input("စောင့်ကြည့်မည့် ပစ္စည်း (ထိုင်းလို):", "เสื้อผ้าแฟชั่น") 
    
    if st.button("🔍 ဒေတာအသစ် ဆွဲယူရန်"):
        try:
            from pytrends.request import TrendReq
            pytrends = TrendReq(hl='th-TH', tz=420)
            pytrends.build_payload([keyword_input], cat=0, timeframe="today 1-m", geo='TH', gprop='')
            related_queries = pytrends.related_queries()
            if related_queries and keyword_input in related_queries:
                st.write(related_queries[keyword_input]['top'].head(5))
            else:
                st.warning("ဒေတာ ရှာမတွေ့ပါ။")
        except:
            st.error("Google Trends ဆာဗာ ခေတ္တမအားပါ။")

# ----------------------------------------------------
# TAB 3: GAME GUIDE
# ----------------------------------------------------
with tab3:
    st.markdown("""
    ### 📚 ကစားနည်း လမ်းညွှန်ချက်
    1. **အဆင့်မြှင့်ရန် (Level Up):** ခလုတ်တွေကို နှိပ်ပြီး အလုပ်လုပ်တိုင်း XP ရပါမယ်။ XP ပြည့်ရင် အဆင့်တက်ပါမယ်။
    2. **ပိုက်ဆံ (Coin):** ဒါက ဂိမ်းထဲက အဓိက သုံးစွဲငွေ ဖြစ်ပါတယ်။ ပစ္စည်းရောင်းရင် သို့မဟုတ် စွန့်စားခန်းနိုင်ရင် ရပါတယ်။
    3. **ငွေပြား (Silver):** စျေးကွက်ထဲ ရှာဖွေရင် အဓိက တွေ့ရတတ်ပါတယ်။ ငွေပြား ၁၀ ပြားပြည့်ရင် ရွှေတုံးအဖြစ် ပြောင်းလဲနိုင်ပါတယ်။
    4. **ရွှေတုံး (Gold):** တကယ့် စွန့်စားခန်း တိုက်ပွဲတွေမှာပဲ ရနိုင်တဲ့ အဖိုးတန်ရတနာ ဖြစ်ပါတယ်။
    """)
