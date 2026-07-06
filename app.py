import streamlit as st
import pandas as pd
from pytrends.request import TrendReq

# Page configuration for beautiful UI
st.set_page_config(
    page_title="Thai Market Research Pro", 
    page_icon="📊", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Look & UI Touch
st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .stButton>button {
        background-color: #ff4b4b;
        color: white;
        border-radius: 12px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        width: 100%;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #ff2b2b; color: white; }
    .card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        margin-bottom: 15px;
        border-left: 5px solid #ff4b4b;
    }
    .metric-box {
        background: linear-gradient(135deg, #6B73FF 10%, #000DFF 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR SETTINGS ---
st.sidebar.markdown("## ⚙️ စနစ်ထိန်းချုပ်ခန်း")
st.sidebar.write("သင့်စျေးကွက်အတွက် လိုအပ်တာများကို ဤနေရာတွင် ပြင်ဆင်ပါ")

keyword_input = st.sidebar.text_input("🔍 စောင့်ကြည့်မည့် ပစ္စည်း (ထိုင်းလို):", "เสื้อผ้าแฟชั่น") 
days_filter = st.sidebar.selectbox(
    "📅 စောင့်ကြည့်မည့် ကာလအပိုင်းအခြား:", 
    ["today 1-m", "today 3-m", "now 7-d"],
    format_func=lambda x: "လွန်ခဲ့သော ၁ လစာ" if x=="today 1-m" else "လွန်ခဲ့သော ၃ လစာ" if x=="today 3-m" else "လွန်ခဲ့သော ၇ ရက်စာ"
)

# Quick Category Buttons
st.sidebar.markdown("### 🏷️ အမြန်ရွေးချယ်ရန် ကဏ္ဍများ")
st.sidebar.caption("အောက်ပါခလုတ်များကို နှိပ်ပြီး စျေးကွက်နမူနာများကို လေ့လာနိုင်သည်")
if st.sidebar.button("👜 အိတ်မျိုးစုံ (กระเป๋า)"):
    keyword_input = "กระเป๋า"
if st.sidebar.button("👟 ဖိနပ် (รองเท้า)"):
    keyword_input = "รองเท้า"
if st.sidebar.button("💄 အလှကုန် (เครื่องสำอาง)"):
    keyword_input = "เครื่องสำอาง"
if st.sidebar.button("🧸 အရုပ်/ကလေးပစ္စည်း (ของเล่น)"):
    keyword_input = "ของเล่น"

# --- MAIN PAGE HEADER ---
st.title("📊 Thai Market Research Pro")
st.markdown(f"**လက်ရှိစောင့်ကြည့်နေသော စျေးကွက်ပစ္စည်း:** `{keyword_input}`")

# --- TAB SYSTEM FOR CLEAN LOOK ---
tab1, tab2, tab3 = st.tabs(["🔥 Google Trends ဒေတာ", "📚 စျေးကွက်ဗဟုသုတ (ဖတ်စရာ)", "🛒 E-commerce Shortcuts"])

# ----------------------------------------------------
# TAB 1: GOOGLE TRENDS DATA
# ----------------------------------------------------
with tab1:
    st.markdown("### 📈 လူကြိုက်များဆုံးနှင့် အမေးအများဆုံး Keyword များ")
    
    try:
        pytrends = TrendReq(hl='th-TH', tz=420)
        pytrends.build_payload([keyword_input], cat=0, timeframe=days_filter, geo='TH', gprop='')
        related_queries = pytrends.related_queries()
        
        if related_queries and keyword_input in related_queries:
            top_queries = related_queries[keyword_input]['top']
            rising_queries = related_queries[keyword_input]['rising']
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"<div class='card'><h4>🔝 ထိပ်တန်း ရှာဖွေမှုများ (Top)</h4><p>လူတွေ အမြဲတမ်း ပုံမှန်အများဆုံး ရှာဖွေလေ့ရှိသော စကားလုံးများ</p></div>", unsafe_allow_html=True)
                if top_queries is not None and not top_queries.empty:
                    st.dataframe(top_queries, use_container_width=True)
                else:
                    st.info("ဒေတာ မရှိသေးပါ။")
                    
            with col2:
                st.markdown(f"<div class='card'><h4>⚡️ အရှိန်အဟုန် တက်လာသည့် ရှာဖွေမှုများ (Rising)</h4><p>လက်ရှိရက်ပိုင်းအတွင်း ရှာဖွေမှု ရာခိုင်နှုန်း အဆမတန် မြင့်တက်လာသော စကားလုံးများ</p></div>", unsafe_allow_html=True)
                if rising_queries is not None and not rising_queries.empty:
                    st.dataframe(rising_queries, use_container_width=True)
                else:
                    st.info("ဒေတာ မရှိသေးပါ။")
        else:
            st.warning("ဤ Keyword အတွက် ဒေတာအလုံအလောက် မရှိသေးပါ။ Sidebar တွင် အခြားစကားလုံး ပြောင်းရိုက်ကြည့်ပါ။")
            
    except Exception as e:
        st.error("Google Trends ဆာဗာ မအားလပ်သေးပါ။ ခေတ္တစောင့်ပြီး စာမျက်နှာကို Refresh ပြန်လုပ်ပေးပါ။")

# ----------------------------------------------------
# TAB 2: MARKET INSIGHTS (READING SECTION)
# ----------------------------------------------------
with tab2:
    st.markdown("### 📚 ထိုင်းနိုင်ငံတွင် အရောင်းအဝယ်လုပ်လျှင် မဖြစ်မနေဖတ်ရန်")
    
    col_insight1, col_insight2 = st.columns(2)
    
    with col_insight1:
        st.markdown(f"""
        <div class='card'>
            <h4 style='color: #ff4b4b;'>💡 ၁။ 'Top Keywords' နှင့် 'Rising' ကို ဘယ်လိုသုံးမလဲ။</h4>
            <p><b>Top Keywords (ထိပ်တန်းရှာဖွေမှု):</b> ၎င်းစကားလုံးများကို သင့်ကုန်ပစ္စည်းရဲ့ နာမည်ပေးတဲ့နေရာ (Title) နဲ့ ကြော်ငြာစာသား (Caption) ထဲမှာ မဖြစ်မနေ ထည့်ရေးရပါမယ်။ ဒါမှ လူတွေ ရှာတဲ့အခါ သင့်ဆိုင်က အပေါ်ဆုံးမှာ ပေါ်လာမှာပါ။</p>
            <p><b>Rising Keywords (အရှိန်တက်လာသောရှာဖွေမှု):</b> ဒါကတော့ အခုမှ စပြီး ခေတ်စားလာတဲ့ ရေစီးကြောင်း (Trend) ဖြစ်ပါတယ်။ ပြိုင်ဘက်တွေ မရိပ်မိခင် ဒီပစ္စည်းတွေကို မြန်မြန်သွင်းပြီး အရင်ဦးအောင် ရောင်းချနိုင်ရင် အမြတ်အစွန်း အများကြီး ရနိုင်ပါတယ်။</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='card'>
            <h4 style='color: #ff4b4b;'>📦 ၂။ ကုန်ပစ္စည်း စျေးနှုန်းသတ်မှတ်ခြင်း ဗျူဟာ</h4>
            <p>ထိုင်းဝယ်သူများသည် <b>Quality (အရည်အသွေး)</b> နှင့် <b>Fast Delivery (အမြန်ပို့ဆောင်မှု)</b> ကို အလွန်ဦးစားပေးသည်။ စျေးနှုန်းတစ်ခုတည်းကိုပဲ လျှော့ချပြီး ပြိုင်ဆိုင်ခြင်းသည် ရေရှည်တွင် အရှုံးပေါ်စေနိုင်သည်။ ပစ္စည်းထုပ်ပိုးမှု လှလှပပနှင့် လက်ဆောင်အသေးစားလေးများ ထည့်ပေးခြင်းက သင့်ကို ပြိုင်ဘက်များထက် ထူးခြားစေပါလိမ့်မည်။</p>
        </div>
        """, unsafe_allow_html=True)

    with col_insight2:
        st.markdown(f"""
        <div class='card'>
            <h4 style='color: #ff4b4b;'>📱 ၃။ ထိုင်းအွန်လိုင်းစျေးကွက် သဘာဝ</h4>
            <ul>
                <li><b>TikTok Shop:</b> စိတ်ခံစားမှုကြောင့် ဝယ်ယူခြင်း (Impulse Buying) အတွက် အကောင်းဆုံး။ အဝတ်အထည်၊ အလှကုန်နှင့် အဆာပြေမုန့်များအတွက် သင့်တော်သည်။</li>
                <li><b>Shopee / Lazada:</b> ဝယ်သူက တိတိကျကျ ရှာဖွေပြီးမှ ဝယ်လေ့ရှိသည်။ လူသုံးကုန်၊ အီလက်ထရွန်နစ်နှင့် တန်ဖိုးကြီးပစ္စည်းများအတွက် ပိုမိုသင့်တော်သည်။</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='card'>
            <h4 style='color: #ff4b4b;'>⚠️ ၄။ သတိပြုရန် အချက်ပြချက် (Red Flags)</h4>
            <p>အကယ်၍ 'Rising' ဇယားထဲတွင် ရာခိုင်နှုန်းများ အဆမတန် တက်နေသော်လည်း အပြင်တွင် ဝယ်သူမရှိပါက ၎င်းသည် ခေတ္တခဏသာ ခေတ်စားပြီး ပြန်ကျသွားမည့် <b>Fad Trend</b> ဖြစ်နိုင်သည်။ ပစ္စည်းများကို အမြောက်အမြား ကြိုတင်ဝယ်စုခြင်းကို ရှောင်ကြဉ်ပါ။</p>
        </div>
        """, unsafe_allow_html=True)

# ----------------------------------------------------
# TAB 3: E-COMMERCE SHORTCUTS
# ----------------------------------------------------
with tab3:
    st.markdown("### 🛒 ပြိုင်ဘက်များနှင့် လက်ရှိစျေးကွက်ပေါက်စျေးကို တစ်ချက်ကလစ်ဖြင့် သွားကြည့်ရန်")
    st.write("အောက်ပါခလုတ်များကို နှိပ်ပါက သက်ဆိုင်ရာ စျေးကွက်ထဲသို့ တိုက်ရိုက်ရောက်ရှိသွားမည် ဖြစ်သည်-")
    
    col3, col4, col5 = st.columns(3)
    
    with col3:
        st.markdown(f"<div style='text-align: center; margin-bottom: 10px;'><b>📱 TikTok Creative Center</b></div>", unsafe_allow_html=True)
        st.link_button("🔥 TikTok Trends သို့သွားရန်", "https://ads.tiktok.com/business/creativecenter/trends/products/pc/en", use_container_width=True)
        
    with col4:
        st.markdown(f"<div style='text-align: center; margin-bottom: 10px;'><b>🧡 Shopee Marketplace</b></div>", unsafe_allow_html=True)
        st.link_button(f"🛍️ Shopee တွင် '{keyword_input}' ရှာရန်", f"https://shopee.co.th/search?keyword={keyword_input}", use_container_width=True)
        
    with col5:
        st.markdown(f"<div style='text-align: center; margin-bottom: 10px;'><b>💙 Lazada Marketplace</b></div>", unsafe_allow_html=True)
        st.link_button(f"📦 Lazada တွင် '{keyword_input}' ရှာရန်", f"https://www.lazada.co.th/catalog/?q={keyword_input}", use_container_width=True)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>🤖 Thai Market Research Pro Edition | 2026</p>", unsafe_allow_html=True)
