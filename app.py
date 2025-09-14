import streamlit as st
from pages import cricbuzz_home, CRUD_operations, live_matches, Top_Sqlstats

# Database connection config
DB_KWARGS = dict(
    host="localhost",
    user="root",
    password="blacky1996",
    database="Cricbuzz"
)

# Set page config
st.set_page_config(page_title="Mainpage_Intro", layout="wide")

page_bg_color = """
<style>
.stApp {
    background-color: #0D1B2A;  /* Dark bluish Oxford Blue */
    color: white;
}

[data-testid="stAppViewContainer"] > .main {
    color: white;
}
</style>
"""
st.markdown(page_bg_color, unsafe_allow_html=True)

# App Title
st.title("🏏 CricFusion – Real-Time Cricket Match Data Analytics")

# Project Intro
st.markdown("""
## 🚀 Project Introduction

Welcome to **CricFusion**, your interactive dashboard designed to provide live statistics, player analytics, and match summaries for the **Asia Cup 2025**.

This project aims to:
- Deliver real-time player and match insights
- Provide easy navigation for cricket enthusiasts  
- Support CRUD operations for data management  
- Offer top statistical summaries and in-depth analysis

Built with Streamlit and backed by a MySQL database, CricFusion empowers you to stay updated with the excitement of the Asia Cup in a beautiful and efficient interface.
""")

# Asia Cup 2025 Info
st.markdown("""
## 🏏 Asia Cup 2025 – Tournament Overview

The **17th edition of the Asia Cup** is being held from **9 to 28 September 2025**.  
It’s played in the **T20 International (T20I)** format with a total of **19 matches**.  

Originally awarded to **India**, the tournament is being played in the **United Arab Emirates (UAE)** due to political tensions, with games hosted at:  
- 🏟️ Dubai International Cricket Stadium, Dubai  
- 🏟️ Sheikh Zayed Cricket Stadium, Abu Dhabi  

---

## 🌏 Participating Teams (8)

- 🇮🇳 India  
- 🇵🇰 Pakistan  
- 🇱🇰 Sri Lanka  
- 🇧🇩 Bangladesh  
- 🇦🇫 Afghanistan  
- 🇦🇪 United Arab Emirates (UAE)  
- 🇴🇲 Oman  
- 🇭🇰 Hong Kong  

---

## 🗂️ Groups & Format

**Group A**  
- 🇮🇳 India  
- 🇵🇰 Pakistan  
- 🇴🇲 Oman  
- 🇦🇪 UAE  

**Group B**  
- 🇦🇫 Afghanistan  
- 🇧🇩 Bangladesh  
- 🇱🇰 Sri Lanka  
- 🇭🇰 Hong Kong  

➡️ Top **2 teams from each group** qualify for the **Super Four** stage.  
➡️ The top 2 teams from the Super Four then meet in the **Grand Final**.  

---

## 📌 Quick Facts  

- 🗓 **Dates:** 9–28 September 2025  
- 🏆 **Defending Champion:** India (2023)  
- 📍 **Host Venues:** Dubai & Abu Dhabi, UAE  
- 🔢 **Matches:** 19 T20Is  
""")