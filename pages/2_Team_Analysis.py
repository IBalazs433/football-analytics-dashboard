import database.queries as queries
import streamlit as st


conn = queries.get_connection()

st.set_page_config(
    page_title="⚽ Team Analysis",
    page_icon="⚽",
    layout="wide"
)


st.sidebar.header("Filters")

country = st.sidebar.selectbox(
    "Country",
    queries.get_countries(conn),
    key="country_selectbox"
)

team = st.sidebar.selectbox(
    "Team",
    queries.get_teams(conn, country),
    key="team_selectbox"
)

window = st.sidebar.selectbox(
    "Rolling Window",
    [10, 20, 30, 40, 50],
)


st.title("⚽ Team Analysis")


st.subheader("Overview")

statistics = queries.get_team_statistics(conn, team, window)

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Matches", statistics.iloc[0]["matches"])
    st.metric("Wins", statistics.iloc[0]["wins"])
    st.metric("Draws", statistics.iloc[0]["draws"])
    st.metric("Losses", statistics.iloc[0]["losses"])

with c2:
    st.metric("Goals For", statistics.iloc[0]["avg_goals_for"])
    st.metric("Goals Against", statistics.iloc[0]["avg_goals_against"])
    st.metric("Corners For", statistics.iloc[0]["avg_corners_for"])
    st.metric("Corners Against", statistics.iloc[0]["avg_corners_against"])

with c3:
    st.metric("Shots For", statistics.iloc[0]["avg_shots_for"])
    st.metric("Shots Against", statistics.iloc[0]["avg_shots_against"])
    st.metric("Shots on Target For", statistics.iloc[0]["avg_shots_on_target_for"])
    st.metric("Shots on Target Against", statistics.iloc[0]["avg_shots_on_target_against"])


st.divider()

st.subheader("Recent Form")

st.info(queries.get_recent_team_form(conn, team, window))


st.divider()

recent_matches = queries.get_recent_team_matches(conn, team, window)

st.subheader(f"Last {min(window, len(recent_matches))} Matches")

if recent_matches.empty:
    st.info("No matches found.")
else:
    st.dataframe(
        recent_matches,
        use_container_width=True,
    )

st.divider()


st.subheader("Statistics")

team_trend_statistics = queries.get_team_trend_statistics(conn, team)

tab1, tab2, tab3, tab4 = st.tabs([
    "Goals",
    "Shots",
    "Corners",
    "Cards"
])

with tab1:
    st.dataframe(team_trend_statistics[["season", "avg_goals_for", "avg_goals_against"]], width="stretch")

with tab2:
    st.dataframe(team_trend_statistics[["season", "avg_shots_for", "avg_shots_against", "avg_shots_on_target_for", "avg_shots_on_target_against"]], width="stretch")

with tab3:
    st.dataframe(team_trend_statistics[["season", "avg_corners_for", "avg_corners_against"]], width="stretch")

with tab4:
    st.dataframe(team_trend_statistics[["season", "avg_yellow_cards_for", "avg_yellow_cards_against", "avg_red_cards_for", "avg_red_cards_against"]], width="stretch")
