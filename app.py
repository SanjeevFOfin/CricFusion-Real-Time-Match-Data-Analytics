import streamlit as st
from pages import cricbuzz_home, CRUD_operations, live_matches, Top_Sqlstats

# Cricket-themed background CSS
page_bg_img = """
<style>
.stApp {
    background-image: url("https://images.slivcdn.com/videoasset_images/manage_file/1000007861/1757519547213308_AsiaCup_2025_GOB_3_Landscape_Thumb_SP_3.jpg?w=1349&q=low");
    background-size: cover;
    background-attachment: fixed;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Page config
st.set_page_config(page_title="Main_Page", layout="wide")

# App Title
st.title("🏏 CricFusion – Asia Cup 2025 Live Stats Dashboard")

# Welcome Section
st.markdown("""
Welcome to **CricFusion**, your ultimate interactive dashboard for live stats, player analytics, and match summaries from the **Asia Cup 2025**!

Here, you can:
- Explore in-depth player statistics  
- View match summaries  
- Analyze top scorers and bowlers  
- Navigate through different matches easily

Stay updated with real-time cricket action, powered by our efficient data pipeline and beautiful Streamlit interface.

⚡ Enjoy the excitement of cricket in Asia Cup 2025! ⚡
""")

# Asia Cup Info Section
st.markdown("""
## 📖 About Asia Cup 2025

The **Asia Cup 2025** is one of the most anticipated cricket tournaments in Asia, featuring top cricketing nations like India, Pakistan, Sri Lanka, Bangladesh, and others.  
This tournament showcases fierce rivalries, emerging talents, and the spirit of cricket.

👉 **Format:** T20 (most likely)  
📍 **Host Country:** To be announced  
🏆 **Defending Champion (2023):** India

Stay tuned for live match updates, player performance insights, and in-depth analytics as the tournament progresses.

Let the battle for Asia’s cricket supremacy begin! 🎉
""")
