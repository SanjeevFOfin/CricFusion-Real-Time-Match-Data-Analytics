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
st.set_page_config(page_title="Player Stats CRUD", layout="wide")


def app():
    st.title("CRUD Operations Page")
    st.write("Here you can perform CRUD operations on the database.")


# Cricket-themed background CSS
page_bg_img = """
<style>
.stApp {
    background-image: url("https://cricketer.io/wp-content/uploads/2025/08/Asia-Cup-Tickets-UAE-2025-1-1.webp");
    background-size: cover;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)
st.title("⚡ Player Stats Management (CRUD Operations)")

@st.cache_data
def run_query(query, fetch=True):
    try:
        conn = mysql.connector.connect(**DB_KWARGS)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        if fetch:
            result = cursor.fetchall()
            conn.close()
            return pd.DataFrame(result)
        else:
            conn.commit()
            conn.close()
            return None
    except Exception as e:
        st.error(f"Database error: {e}")
        return pd.DataFrame()

# ----- CREATE (Insert New Player Stats) -----
st.header("➕ Add New Player Stats")

with st.form("create_form"):
    player_id = st.text_input("Player ID")
    player_name = st.text_input("Player Name")
    team_name = st.text_input("Team Name")
    runs = st.number_input("Runs", step=1)
    balls = st.number_input("Balls", step=1)
    strike_rate = st.number_input("Strike Rate", format="%.2f")
    submit_create = st.form_submit_button("Add Player Stats")

    if submit_create:
        query = f"""
            INSERT INTO batsman_data (player_id, player_name, team_name, runs, balls, strike_rate)
            VALUES ('{player_id}', '{player_name}', '{team_name}', {runs}, {balls}, {strike_rate});
        """
        run_query(query, fetch=False)
        st.success("✅ New player stats inserted successfully.")

# ----- READ (View Player Stats) -----
st.header("📋 View All Player Stats")

if st.button("Load All Player Stats"):
    query = "SELECT * FROM batsman_data;"
    df = run_query(query)
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("No data found.")

# ----- UPDATE (Update Existing Player Stats) -----
st.header("✏️ Update Player Stats")

with st.form("update_form"):
    update_player_id = st.text_input("Enter Player ID to Update")
    new_runs = st.number_input("New Runs", step=1)
    new_balls = st.number_input("New Balls", step=1)
    new_strike_rate = st.number_input("New Strike Rate", format="%.2f")
    submit_update = st.form_submit_button("Update Player Stats")

    if submit_update:
        query = f"""
            UPDATE batsman_data
            SET runs = {new_runs}, balls = {new_balls}, strike_rate = {new_strike_rate}
            WHERE player_id = '{update_player_id}';
        """
        run_query(query, fetch=False)
        st.success(f"✅ Player ID {update_player_id} stats updated.")

# ----- DELETE (Remove Player Stats) -----
st.header("❌ Delete Player Stats")

with st.form("delete_form"):
    delete_player_id = st.text_input("Enter Player ID to Delete")
    submit_delete = st.form_submit_button("Delete Player Stats")

    if submit_delete:
        query = f"DELETE FROM batsman_data WHERE player_id = '{delete_player_id}';"
        run_query(query, fetch=False)
        st.success(f"✅ Player ID {delete_player_id} stats deleted.")
