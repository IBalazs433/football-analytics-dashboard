import database.queries as queries
import streamlit as st


conn = queries.get_connection()

st.set_page_config(
    page_title="📋 Match Analysis",
    page_icon="📋",
    layout="wide"
)


st.sidebar.header("Filters")

country = st.sidebar.selectbox(
    "Country", 
    queries.get_countries(conn)
)

league = st.sidebar.selectbox(
    "League", 
    queries.get_leagues(conn, country)
)

season = st.sidebar.selectbox(
    "Season", 
    queries.get_seasons(conn, league)
)

home_team = st.sidebar.selectbox(
    "Home Team", 
    queries.get_teams_from_season(conn, country, league, season)
)

away_team = st.sidebar.selectbox(
    "Away Team", 
    queries.get_teams_from_season(conn, country, league, season),
    index=1
)

date = st.sidebar.selectbox(
    "Date", 
    queries.get_match_dates(conn, country, league, season, home_team, away_team)
)


st.title("📋 Match Analysis")


st.header("Match Summary")

match_df = queries.get_match_statistics(conn, country, league, season, home_team, away_team, date)

if match_df.empty:
    st.info("No match found.")

else:
    c1, c2, c3 = st.columns([2, 1, 2])

    with c1:
        st.metric("Home Team", match_df["home_team"].values[0])

    with c2:
        st.metric("Score", f"{match_df['home_goals'].values[0]} - {match_df['away_goals'].values[0]}")

    with c3:
        st.metric("Away Team", match_df["away_team"].values[0])


    st.divider()

    st.header("Match Statistics")

    st.dataframe(match_df, width="stretch")


    st.divider()

    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Home Team Form")
        st.info(queries.get_recent_team_form_before_date(conn, home_team, 5, date=date))

    with c2:
        st.subheader("Away Team Form")
        st.info(queries.get_recent_team_form_before_date(conn, away_team, 5, date=date))

    st.divider()


    st.subheader("Previous Meetings")

    recent_matches = queries.get_head_to_head_matches_before_date(conn, home_team, away_team, 5, date=date)

    if recent_matches.empty:
        st.info("No matches found.")
    else:
        st.dataframe(
            recent_matches,
            use_container_width=True,
        )
