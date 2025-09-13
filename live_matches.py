import streamlit as st
import pandas as pd
import mysql.connector
from contextlib import contextmanager
import plotly.express as px

# Database configuration
DB_KWARGS = dict(
    host="localhost",
    user="root",
    password="blacky1996",
    database="Cricbuzz"
)

# Page config
st.set_page_config(page_title="CricFusion Dashboard", layout="wide")

import streamlit as st

def app():
    st.title("Live Matches Page")
    st.write("Display live match information here.")


# Cricket-themed background CSS
page_bg_img = """
<style>
.stApp {
    background-image: url("https://www.shutterstock.com/image-photo/blurry-image-cricket-player-midswing-600nw-2616235749.jpg");
    background-size: cover;
}
.card {
    background-color: #E0FFFF;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
    text-align: center;
    margin-bottom: 20px;
    color: black;  /* Ensure text is visible */
}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

st.title("🏏 CricFusion – Interactive Cricket Dashboard")

@contextmanager
def get_db_connection():
    conn = mysql.connector.connect(**DB_KWARGS)
    try:
        yield conn
    finally:
        conn.close()

@st.cache_data
def run_query(query, params=None):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params or [])
            result = cursor.fetchall()
        return pd.DataFrame(result)
    except Exception as e:
        st.error(f"Database error: {e}")
        return pd.DataFrame()

# Fetch Match IDs for slicer
with st.spinner("Loading Match IDs..."):
    matchid_query = "SELECT DISTINCT matchId FROM match_summaries ORDER BY matchId DESC;"
    df_matchids = run_query(matchid_query)
    matchid_options = ["All"] + df_matchids['matchId'].astype(str).tolist()

selected_matchid = st.selectbox("🆔 Select Match ID", options=matchid_options)

# Build filter condition
matchid_filter = ""
params = []
if selected_matchid != "All":
    matchid_filter = "WHERE match_summaries.matchId = %s"
    params = [selected_matchid]

# Display key match details as cards (only when a specific match is selected)
if selected_matchid != "All":
    query_match_info = """
        SELECT team1, team2, winner, Date, venue
        FROM match_summaries
        WHERE matchId = %s
        LIMIT 1;
    """
    with st.spinner("Loading Match Info..."):
        df_match_info = run_query(query_match_info, params)

    if not df_match_info.empty:
        team1 = df_match_info.at[0, 'team1']
        team2 = df_match_info.at[0, 'team2']
        winner = df_match_info.at[0, 'winner']
        match_date = df_match_info.at[0, 'Date']
        venue = df_match_info.at[0, 'venue']

        col_card1, col_card2, col_card3, col_card4, col_card5 = st.columns(5)
        
        with col_card1:
            st.markdown(f"""
            <div class="card">
                <h3>🏟️ Team 1</h3>
                <h2>{team1}</h2>
            </div>
            """, unsafe_allow_html=True)

        with col_card2:
            st.markdown(f"""
            <div class="card">
                <h3>🏟️ Team 2</h3>
                <h2>{team2}</h2>
            </div>
            """, unsafe_allow_html=True)

        with col_card3:
            st.markdown(f"""
            <div class="card">
                <h3>🏆 Winner</h3>
                <h2>{winner}</h2>
            </div>
            """, unsafe_allow_html=True)

        with col_card4:
            st.markdown(f"""
            <div class="card">
                <h3>📅 Match Date</h3>
                <h2>{match_date}</h2>
            </div>
            """, unsafe_allow_html=True)

        with col_card5:
            st.markdown(f"""
            <div class="card">
                <h3>📍 Venue</h3>
                <h2>{venue}</h2>
            </div>
            """, unsafe_allow_html=True)


st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🌟 Top 10 Run Scorers (All Time / Selected Match)")
    query_top_scorers = f"""
        SELECT batsman_data.player_name, batsman_data.team_name, 
               SUM(batsman_data.runs) AS total_runs, 
               COUNT(batsman_data.matchId) AS matches_played, 
               AVG(batsman_data.strike_rate) AS avg_strike_rate
        FROM batsman_data
        JOIN match_summaries ON batsman_data.matchId = match_summaries.matchId
        {matchid_filter}
        GROUP BY batsman_data.player_name, batsman_data.team_name
        ORDER BY total_runs DESC
        LIMIT 10;
    """
    with st.spinner("Loading Top Scorers..."):
        df_top_scorers = run_query(query_top_scorers, params)
    if not df_top_scorers.empty:
        df_top_scorers.index = range(1, len(df_top_scorers) + 1)
        st.dataframe(df_top_scorers, use_container_width=True, height=400)
    else:
        st.warning("⚠️ No data available for Top Scorers.")

with col2:
    st.subheader("🌪️ Top 10 Wicket-Takers (All Time / Selected Match)")
    query_top_wickets = f"""
        SELECT bowler_data.player_name, bowler_data.team_name, 
               SUM(bowler_data.wickets) AS total_wickets, 
               COUNT(bowler_data.matchId) AS matches_played, 
               AVG(bowler_data.economy) AS avg_economy
        FROM bowler_data
        JOIN match_summaries ON bowler_data.matchId = match_summaries.matchId
        {matchid_filter}
        GROUP BY bowler_data.player_name, bowler_data.team_name
        ORDER BY total_wickets DESC
        LIMIT 10;
    """
    with st.spinner("Loading Top Wicket-Takers..."):
        df_top_wickets = run_query(query_top_wickets, params)

    if not df_top_wickets.empty:
        # Bar Chart Visualization
        fig_wickets = px.bar(
            df_top_wickets,
            x="player_name",
            y="total_wickets",
            color="team_name",
            title="Top 10 Wicket-Takers",
            labels={"player_name": "Player", "total_wickets": "Total Wickets"},
            text="total_wickets"
        )
        fig_wickets.update_layout(xaxis_title="Player", yaxis_title="Wickets Taken", height=500)
        st.plotly_chart(fig_wickets, use_container_width=True)
    else:
        st.warning("⚠️ No data available for Top Wicket-Takers.")

st.markdown("---")

col3, col4 = st.columns([1, 1])

with col3:
    st.subheader("🏆 Winners Distribution (Last 7 Days)")
    if selected_matchid == "All":
        query_winners = """
            SELECT winner AS team_name, COUNT(matchId) AS wins
            FROM match_summaries
            WHERE Date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
            GROUP BY winner;
        """
        with st.spinner("Loading Winners Distribution..."):
            df_winners = run_query(query_winners)
        if not df_winners.empty:
            fig_winners = px.pie(
                df_winners,
                names="team_name",
                values="wins",
                title="Winning Teams Last 7 Days"
            )
            fig_winners.update_layout(height=400)  # <-- Set pie chart height here
            st.plotly_chart(fig_winners, use_container_width=True)
        else:
            st.warning("⚠️ No recent winner data available.")
    else:
        st.info("🏏 Pie chart disabled when filtering by specific Match ID.")

with col4:
    st.subheader("📊 Total Wickets Taken Per Venue (Last 30 Days)")
    query_wickets_venue = """
        SELECT ms.venue AS venue_name, SUM(bd.wickets) AS total_wickets
        FROM match_summaries ms
        JOIN bowler_data bd ON ms.matchId = bd.matchId
        WHERE ms.Date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
        GROUP BY ms.venue
        ORDER BY total_wickets DESC
        LIMIT 10;
    """
    with st.spinner("Loading Wickets Data Per Venue..."):
        df_wickets_venue = run_query(query_wickets_venue)

    if not df_wickets_venue.empty:
        fig_wickets_venue = px.bar(
            df_wickets_venue,
            x='venue_name',
            y='total_wickets',
            title='Total Wickets Taken Per Venue (Last 30 Days)',
            labels={'venue_name': 'Venue', 'total_wickets': 'Total Wickets'},
            text='total_wickets'
        )
        fig_wickets_venue.update_layout(
            xaxis_title="Venue",
            yaxis_title="Wickets Taken",
            height=400  # <-- Set bar chart height here
        )
        st.plotly_chart(fig_wickets_venue, use_container_width=True)
    else:
        st.warning("⚠️ No recent wickets data available.")
