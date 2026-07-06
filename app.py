import streamlit as st
import pandas as pd
from pytrends.request import TrendReq
import requests
from bs4 import BeautifulSoup
import time

# Page configuration
st.set_page_config(page_title="Thai Market Research Tool", page_icon="📈", layout="wide")

st.title("📈 Thai Market Research Tool (Beta)")
st.subheader("ဝယ်သူတွေ ဘာလိုချင်လဲ၊ ပြိုင်ဘက်တွေ ဘာလုပ်နေလဲ စောင့်ကြည့်ရန်")

# Sidebar for controls
st.sidebar.header("⚙️ Settings / ရှာဖွေရန်")
keyword_input = st.sidebar.text_input("စောင့်ကြည့်ချင်သည့် ပစ္စည်း သို့မဟုတ် Keyword ရိုက်ပါ:", "เสื้อผ้าแฟชั่น") # Default: Fashion clothing
days_filter = st.sidebar.selectbox("အချိန်အပိုင်းအခြား ရွေးချယ်ပါ:", ["today 3-m", "today 1-m", "now 7-d"])

# ----------------------------------------------------
# TAB 1: Google Trends (လူတွေ ဘာရှာနေကြလဲ)
# ----------------------------------------------------
st.markdown("---")
st.header("🔥 Google Trends - လူတွေ ဘယ်လို Keyword ရှာဖွေမှု အများဆုံးလဲ")

try:
    # Initialize pytrends for Thailand (TH)
    pytrends = TrendReq(hl='th-TH', tz=420)
    
    # Build payload
    pytrends.build_payload([keyword_input], cat=0, timeframe=days_filter, geo='TH', gprop='')
    
    # Related Queries
    related_queries = pytrends.related_queries()
    
    if related_queries and keyword_input in related_queries:
        top_queries = related_queries[keyword_input]['top']
        rising_queries = related_queries[keyword_input]['rising']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔝 ထိပ်တန်း ရှာဖွေမှုများ (Top Keywords)")
            if top_queries is not None and not top_queries.empty:
                st.dataframe(top_queries, use_container_width=True)
            else:
                st.write("ဒေတာ မရှိသေးပါ။")
                
        with col2:
            st.subheader("⚡️ အရှိန်အဟုန် တက်လာသည့် ရှာဖွေမှုများ (Rising Keywords)")
            if rising_queries is not None and not rising_queries.empty:
                st.dataframe(rising_queries, use_container_width=True)
            else:
                st.write("ဒေတာ မရှိသေးပါ။")
    else:
        st.warning("ဤ Keyword အတွက် သက်ဆိုင်ရာ ရှာဖွေမှုဒေတာ အလုံအလောက်မရှိသေးပါ။ အခြားစကားလုံး ပြောင်းရိုက်ကြည့်ပါ။")

except Exception as e:
    st.error(f"Google Trends ချိတ်ဆက်ရာတွင် အမှားအယွင်းရှိနေပါသည်: {e}")

# ----------------------------------------------------
# TAB 2: Best Seller & Competitor Monitor (မိတ်ဆက်)
# ----------------------------------------------------
st.markdown("---")
st.header("🛍️ E-commerce & Social Media Best Seller Insights")
st.info("TikTok Shop, Shopee, Lazada တို့သည် ခွင့်ပြုချက်မရှိဘဲ ကုဒ်ဖြင့်တိုက်ရိုက်ဆွဲယူခြင်း (Scraping) ကို ပိတ်ပင်ထားတတ်သဖြင့် တရားဝင် API သုံးရန် လိုအပ်ပါသည်။ အောက်တွင် အလွယ်တကူ သွားရောက်လေ့လာနိုင်မည့် Link များကို စီစဉ်ပေးထားပါသည်။")

# Helpful shortcuts for Thailand Market
col3, col4, col5 = st.columns(3)

with col3:
    st.markdown("### 📱 TikTok Shop Trend")
    st.write("TikTok ပေါ်မှာ လက်ရှိ အရောင်းရဆုံးနဲ့ Trend ဖြစ်နေတာတွေကို ကြည့်ရန်-")
    st.markdown(f"[TikTok Creative Center - Thailand](https://ads.tiktok.com/business/creativecenter/trends/products/pc/en)", unsafe_allow_html=True)

with col4:
    st.markdown("### 🧡 Shopee Top Sales")
    st.write("Shopee မှာ လက်ရှိ လူကြိုက်များနေတဲ့ ကုန်ပစ္စည်းတွေကို ရှာရန်-")
    shopee_url = f"https://shopee.co.th/search?keyword={keyword_input}"
    st.markdown(f"[Shopee Thailand တွင် {keyword_input} ကို ရှာရန်]({shopee_url})", unsafe_allow_html=True)

with col5:
    st.markdown("### 💙 Lazada Best Matches")
    st.write("Lazada စျေးကွက်ထဲက ပြိုင်ဘက်တွေရဲ့ စျေးနှုန်းကို စစ်ရန်-")
    lazada_url = f"https://www.lazada.co.th/catalog/?q={keyword_input}"
    st.markdown(f"[Lazada Thailand တွင် {keyword_input} ကို ရှာရန်]({lazada_url})", unsafe_allow_html=True)

st.markdown("---")
st.caption("Developed for Thai Market Research App | 2026")
