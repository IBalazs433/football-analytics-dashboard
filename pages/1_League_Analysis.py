import database.queries as queries
import streamlit as st
import plotly.express as px
from config import visualization as viz


conn = queries.get_connection()

st.set_page_config(
    page_title="League Analysis",
    page_icon="📊 ",
    layout="wide"
)


st.sidebar.header("Filters")

countries = queries.get_countries(conn).iloc[:, 0].tolist()
index = countries.index("England") if "England" in countries else 0
country = st.sidebar.selectbox(
    "Country",
    countries,
    index=index
)

leagues = queries.get_leagues(conn, country).iloc[:, 0].tolist()
index = leagues.index("Premier League") if "Premier League" in leagues else 0
league = st.sidebar.selectbox(
    "League",
    leagues,
    index=index
)

season = st.sidebar.selectbox(
    "Season",
    queries.get_seasons(conn, league).iloc[:, 0].tolist(),
    index=0
)


st.title("📊 League Analysis")

st.markdown("""
Analyse league performance across seasons, including standings, match statistics, and historical trends.
""")


st.header("Overview")

statistics = queries.get_league_statistics(conn, league, season)

if statistics.empty:
    st.info("No league statistics found for the selected filters.")
    st.stop()

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

st.header("Standings")

tab1, tab2, tab3 = st.tabs([
    "League Table",
    "Home Table",
    "Away Table"
])

with tab1:
    league_table = queries.get_league_table(conn, league, season)
    height = len(league_table) * 35 + 37 
    st.dataframe(
        league_table,
        hide_index=True,
        column_config={
            "team": "Team",
            "matches": "MP",
            "wins": "W",
            "draws": "D",
            "losses": "L",
            "goals_for": "GF",
            "goals_against": "GA",
            "points": "Pts"
        },
        width="stretch",
        height=height,
        row_height=35,
    )

with tab2:
    league_home_table = queries.get_league_home_table(conn, league, season)
    height = len(league_home_table) * 35 + 37
    st.dataframe(
        league_home_table,
        hide_index=True,
        column_config={
            "team": "Team",
            "matches": "MP",
            "wins": "W",
            "draws": "D",
            "losses": "L",
            "goals_for": "GF",
            "goals_against": "GA",
            "points": "Pts"
        },
        width="stretch",
        height=height,
        row_height=35,
    )

with tab3:
    league_away_table = queries.get_league_away_table(conn, league, season)
    height = len(league_away_table) * 35 + 37
    st.dataframe(
        league_away_table,
        hide_index=True,
        column_config={
            "team": "Team",
            "matches": "MP",
            "wins": "W",
            "draws": "D",
            "losses": "L",
            "goals_for": "GF",
            "goals_against": "GA",
            "points": "Pts"
        },
        width="stretch",
        height=height,
        row_height=35,
    )


st.divider()

st.header("Season Trends")

tab1, tab2, tab3, tab4 = st.tabs([
    "Goals",
    "Shots",
    "Corners",
    "Cards"
])

trend_statistics = viz.sort_seasons(queries.get_league_trend_statistics(conn, league))

with tab1:
    goal_trend = trend_statistics.rename(
        columns={"average_goals_per_match": "Goals per Match"}
    )

    fig = px.line(
        goal_trend,
        x="season",
        y="Goals per Match",
        markers=True,
        color_discrete_sequence=[viz.COLORS["for"]],
    )

    fig.update_traces(
        name="Goals per Match",
    )
    viz.apply_common_layout(
        fig,
        title="Goals per Match",
        x_axis_title="Season",
        y_axis_title="Goals per Match",
    )
    fig.update_traces(
        hovertemplate="<b>Goals per Match</b><br>Season: %{x}<br>Value: %{y:,.2f}<extra></extra>"
    )

    viz.render_chart(st, fig)

with tab2:
    shots_trend = trend_statistics.rename(
        columns={
            "average_shots_per_match": "Shots per Match",
            "average_shots_on_target": "Shots on Target per Match",
        }
    )

    fig = px.line(
        shots_trend,
        x="season",
        y=[
            "Shots per Match",
            "Shots on Target per Match",
        ],
        markers=True,
        color_discrete_map={
            "Shots per Match": viz.COLORS["shots_on_target"],
            "Shots on Target per Match": viz.COLORS["shots_off_target"],
        },
    )
    viz.apply_common_layout(
        fig,
        title="Shots per Match",
        x_axis_title="Season",
        y_axis_title="Shots per Match",
    )
    viz.apply_standard_hover(
        fig,
        x_label="Season",
        y_label="Value",
    )

    viz.render_chart(st, fig)

with tab3:
    corners_trend = trend_statistics.rename(
        columns={"average_corners_per_match": "Corners per Match"}
    )

    fig = px.line(
        corners_trend,
        x="season",
        y="Corners per Match",
        markers=True,
        color_discrete_sequence=[viz.COLORS["for"]],
    )

    fig.update_traces(
        name="Corners per Match",
        hovertemplate="<b>Corners per Match</b><br>Season: %{x}<br>Value: %{y:,.2f}<extra></extra>",
    )
    viz.apply_common_layout(
        fig,
        title="Corners per Match",
        x_axis_title="Season",
        y_axis_title="Corners per Match",
    )

    viz.render_chart(st, fig)

with tab4:
    cards_trend = trend_statistics.rename(
        columns={
            "average_yellow_cards_per_match": "Yellow Cards per Match",
            "average_red_cards_per_match": "Red Cards per Match",
        }
    )

    fig = px.line(
        cards_trend,
        x="season",
        y=[
            "Yellow Cards per Match",
            "Red Cards per Match",
        ],
        markers=True,
        color_discrete_map={
            "Yellow Cards per Match": viz.COLORS["for"],
            "Red Cards per Match": viz.COLORS["red_cards"],
        },
    )
    viz.apply_common_layout(
        fig,
        title="Cards per Match",
        x_axis_title="Season",
        y_axis_title="Cards per Match",
    )
    viz.apply_standard_hover(
        fig,
        x_label="Season",
        y_label="Value",
    )

    viz.render_chart(st, fig)