import database.queries as queries
import streamlit as st


conn = queries.get_connection()
    
st.set_page_config(
    page_title="🤝 Head-to-Head",
    page_icon="🤝",
    layout="wide"
)


st.sidebar.header("Filters")

country = st.sidebar.selectbox(
    "Country", 
    queries.get_countries(conn)
)

team_a = st.sidebar.selectbox(
    "Team A", 
    queries.get_teams(conn, country)
)

team_b = st.sidebar.selectbox(
    "Team B",
    queries.get_teams(conn, country),
    index=1
)

window = st.sidebar.selectbox(
    "Rolling Window",
    [10, 20, 30, 40, 50],
)


st.title("🤝 Head-to-Head")

st.header("Overall Record")

head_to_head_statistics = queries.get_recent_head_to_head_statistics(conn, team_a, team_b, window)

st.dataframe(
    head_to_head_statistics,
    width="stretch",
)


st.divider()

recent_head_to_head_matches = queries.get_recent_head_to_head_matches(conn, team_a, team_b, window)

st.header(f"Last {min(window, len(recent_head_to_head_matches))} Matches")

if recent_head_to_head_matches.empty:
    st.info("No matches found.")
else:
    st.dataframe(
        recent_head_to_head_matches,
        width="stretch"
    )
