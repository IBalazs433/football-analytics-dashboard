import database.queries as queries
import streamlit as st


conn = queries.get_connection()

st.set_page_config(
    page_title="📊 League Analysis",
    page_icon="📊 ",
    layout="wide"
)


st.sidebar.header("Filters")

country = st.sidebar.selectbox(
    "Country",
    queries.get_countries(conn),
)

league = st.sidebar.selectbox(
    "League",
    queries.get_leagues(conn, country),
)

season = st.sidebar.selectbox(
    "Season",
    queries.get_seasons(conn, league)
)


st.title("📊 League Analysis")

st.markdown("""
Analyse league performance across seasons, including standings, match statistics, and historical trends.
""")


st.subheader("Overview")

statistics = queries.get_league_statistics(conn, league, season)

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Matches", statistics.iloc[0]["total_matches"])
    st.metric("Goals", statistics.iloc[0]["total_goals"])

with c2:
    st.metric("Average Shots per Match", statistics.iloc[0]["average_shots_per_match"])
    st.metric("Average Shots on Target", statistics.iloc[0]["average_shots_on_target"])

with c3:
    st.metric("Average Yellow Cards per Match", statistics.iloc[0]["average_yellow_cards_per_match"])
    st.metric("Average Red Cards per Match", statistics.iloc[0]["average_red_cards_per_match"])


st.divider()

st.subheader("Standings")

tab1, tab2, tab3 = st.tabs([
    "League Table",
    "Home Table",
    "Away Table"
])

with tab1:
    st.dataframe(queries.get_league_table(conn, league, season), width="stretch")

with tab2:
    st.dataframe(queries.get_league_home_table(conn, league, season), width="stretch")

with tab3:
    st.dataframe(queries.get_league_away_table(conn, league, season), width="stretch")


st.divider()

st.subheader("Season Trends")

tab1, tab2, tab3, tab4 = st.tabs([
    "Goals",
    "Shots",
    "Corners",
    "Cards"
])

trend_statistics = queries.get_league_trend_statistics(conn, league)

with tab1:
    st.dataframe(trend_statistics[["season", "average_goals_per_match"]], width="stretch")

with tab2:
    st.dataframe(trend_statistics[["season", "average_shots_per_match", "average_shots_on_target"]], width="stretch")

with tab3:
    st.dataframe(trend_statistics[["season", "average_corners_per_match"]], width="stretch")

with tab4:
    st.dataframe(trend_statistics[["season", "average_yellow_cards_per_match", "average_red_cards_per_match"]], width="stretch")