import streamlit as st
import pandas as pd
import mysql.connector

# Database connection config
DB_KWARGS = dict(
    host="localhost",
    user="root",
    password="blacky1996",
    database="Cricbuzz"
)

# Page config
st.set_page_config(page_title="cricbuzz_home", layout="wide")

# Cricket-themed background CSS
page_bg_img = """
<style>
.stApp {
    background-image: url("https://www.timeoutjeddah.com/cloud/timeoutjeddah/2025/07/21/ezgif-171adb7263919d-1024x768.jpg");
    background-size: cover;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

st.markdown(
    """
    <style>
    .css-18e3th9 {  /* Streamlit main block */
        display: flex;
        justify-content: center;
    }
    .main-container {
        max-width: 1200px;
        width: 100%;
        margin: auto;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <style>
    .css-10trblm {  /* Streamlit default class for title */
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.title("🏏 CricFusion – Home Page")
    
# ==========================================================
# CricFusion – Real-Time Cricket Match Data Analytics
# Full Streamlit App (Raw Data Viewer + 11 SQL Analyses)
# ==========================================================

# -------------------------------
# Project Info
# -------------------------------
st.markdown(
    """
    <h3 style='color:white;'>Project Name: CricFusion – Real-Time Cricket Match Data Analytics</h3>
    <h3 style='color:white;'>Project Type: Data Analysis & Web Application</h3>
    <h3 style='color:white;'>Contribution: Individual (SANJEEV RAJ T)</h3>
    <h3 style='color:white;'>GitHub Link: 
        <a href='https://github.com/SanjeevFOfin/CricFusion-Real-Time-Match-Data-Analytics'
        style='color:blue;'>My Project Repository</a>
    </h3>
    <h3 style='color:white;'>Project Summary:</h3>
    <p style='color:white; font-size:18px;'>
    CricFusion connects cricket data enthusiasts with powerful real-time statistics and deep analytics.
    It allows viewing raw cricket data (matches, players, performances) and performing advanced SQL analyses.
    Built using Streamlit for UI and MySQL for data storage, this project supports in-depth querying and visualization of cricket insights.
    </p>
    """,
    unsafe_allow_html=True
)
st.markdown("---")

@st.cache_data
def run_query(query):
    try:
        conn = mysql.connector.connect(**DB_KWARGS)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        result = cursor.fetchall()
        conn.close()
        return pd.DataFrame(result)
    except Exception as e:
        st.error(f"Database connection error: {e}")
        return pd.DataFrame()

# === Raw Dataset Viewer Dropdown ===
st.header("📊 Raw Dataset Viewer")
raw_dataset = st.selectbox(
    "Select Dataset to View",
    ["Match Summaries", "Batsman Data", "Bowler Data", "Player Descriptions"]
)

if st.button("View Dataset"):
    if raw_dataset == "Match Summaries":
        query = "SELECT * FROM match_summaries;"
    elif raw_dataset == "Batsman Data":
        query = "SELECT * FROM batsman_data;"
    elif raw_dataset == "Bowler Data":
        query = "SELECT * FROM bowler_data;"
    else:
        query = "SELECT * FROM player_descriptions;"

    df = run_query(query)
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("No data found or database connection issue.")

# ==========================================================
# Skills Takeaway
# ==========================================================
st.markdown(
    """
    <h3 style='color:white;'>🔧 Skills Takeaway from This Project</h3> 
    <p style='color:white; font-size:20px;'> 
    <b>Python</b>, <b>SQL</b>, <b>Streamlit Interface Development</b>, <b>Data Analysis</b>, <b>RapidAPI Integration</b>, <b>Postman for Web Scraping</b>
    </p>
    """,
    unsafe_allow_html=True
)

st.markdown("---")
