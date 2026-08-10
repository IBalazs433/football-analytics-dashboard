import database.queries as queries
import streamlit as st
import plotly.express as px
import pandas as pd
from config import visualization as viz


conn = queries.get_connection()

st.set_page_config(
    page_title="Team Analysis",
    page_icon="📋",
    layout="wide"
)


st.sidebar.header("Filters")

country = st.sidebar.selectbox(
    "Country",
    queries.get_countries(conn).iloc[:, 0].tolist(),
    key="country_selectbox"
)

team = st.sidebar.selectbox(
    "Team",
    queries.get_teams(conn, country).iloc[:, 0].tolist(),
    key="team_selectbox"
)

window = st.sidebar.selectbox(
    "Rolling Window",
    [5, 10, 15, 20, 25, 30],
)


st.title("📋 Team Analysis")

st.markdown("""Analyse an individual team's performance, form, and statistics across its matches and seasons.
""")


st.header("Overview")

team_statistics = queries.get_team_statistics(conn, team, window)

if team_statistics.empty:
    st.info("No team statistics found for the selected filters.")
    st.stop()

statistics = team_statistics.iloc[0]

c1, c2 = st.columns(2)

with c1:
    st.metric("Matches", statistics["matches"])
    st.metric("Wins", statistics["wins"])
    st.metric("Draws", statistics["draws"])
    st.metric("Losses", statistics["losses"])

with c2:
    outcomes = pd.DataFrame({
        "Result": ["Wins", "Draws", "Losses"],
        "Matches": [
            statistics["wins"],
            statistics["draws"],
            statistics["losses"]
        ]
    })

    fig = px.pie(
        outcomes,
        names="Result",
        values="Matches",
        title="Match Results",
        color="Result",
        color_discrete_map={
            "Wins": viz.COLORS["wins"],
            "Draws": viz.COLORS["draws"],
            "Losses": viz.COLORS["losses"],
        }
    )

    viz.apply_common_layout(
        fig,
        title="Match Results",
        x_axis_title="",
        y_axis_title="",
    )
    viz.apply_pie_hover(
        fig,
        value_label="Matches",
    )

    viz.render_chart(st, fig)

c1, c2 = st.columns(2)

with c1:
    goals = pd.DataFrame({
        "Statistic": ["Goals For", "Goals Against"],
        "Average per Match": [
            statistics["avg_goals_for"],
            statistics["avg_goals_against"]
        ]
    })

    fig = px.bar(
        goals,
        orientation='h',
        x="Average per Match",
        y="Statistic",
        title="Goals per Match",
        color="Statistic",
        color_discrete_map={
            "Goals For": viz.COLORS["for"],
            "Goals Against": viz.COLORS["against"],
        }
    )

    viz.apply_common_layout(
        fig,
        title="Goals per Match",
        x_axis_title="Average per Match",
        y_axis_title="",
    )
    viz.apply_category_hover(
        fig,
        category_label="",
        value_label="Average per Match",
    )

    viz.render_chart(st, fig)

with c2:
    shots = pd.DataFrame({
        "Statistic": ["Shots Against", "Shots For"],
        "Shots on Target": [
            statistics["avg_shots_on_target_against"],
            statistics["avg_shots_on_target_for"]
        ],
        "Shots off Target": [
            statistics["avg_shots_against"] - statistics["avg_shots_on_target_against"],
            statistics["avg_shots_for"] - statistics["avg_shots_on_target_for"]
        ]
    })

    fig = px.bar(
        shots,
        x=["Shots on Target", "Shots off Target"],
        y="Statistic",
        orientation="h",
        title="Shots per Match",
        color_discrete_map={
            "Shots on Target": viz.COLORS["shots_on_target"],
            "Shots off Target": viz.COLORS["shots_off_target"],
        }
    )

    viz.apply_common_layout(
        fig,
        title="Shots per Match",
        x_axis_title="Average per Match",
        y_axis_title="",
    )
    fig.update_layout(barmode="stack")
    viz.apply_stacked_hover(fig, category_axis="y")

    viz.render_chart(st, fig)

c1, c2 = st.columns(2)

with c1:
    corners = pd.DataFrame({
        "Statistic": ["Corners For", "Corners Against"],
        "Average per Match": [
            statistics["avg_corners_for"],
            statistics["avg_corners_against"]
        ]
    })

    fig = px.bar(
        corners,
        orientation='h',
        x="Average per Match",
        y="Statistic",
        title="Corners per Match",
        color="Statistic",
        color_discrete_map={
            "Corners For": viz.COLORS["for"],
            "Corners Against": viz.COLORS["against"],
        }
    )

    viz.apply_common_layout(
        fig,
        title="Corners per Match",
        x_axis_title="Average per Match",
        y_axis_title="",
    )
    viz.apply_category_hover(
        fig,
        category_label="",
        value_label="Average per Match",
    )

    viz.render_chart(st, fig)

with c2:
    cards = pd.DataFrame({
        "Statistic": ["Yellow Cards For", "Yellow Cards Against", "Red Cards For", "Red Cards Against"],
        "Average per Match": [
            statistics["avg_yellow_cards_for"],
            statistics["avg_yellow_cards_against"],
            statistics["avg_red_cards_for"],
            statistics["avg_red_cards_against"]
        ]
    })

    fig = px.bar(
        cards,
        orientation='h',
        x="Average per Match",
        y="Statistic",
        title="Cards per Match",
        color="Statistic",
        color_discrete_map={
            "Yellow Cards For": viz.COLORS["for"],
            "Yellow Cards Against": viz.COLORS["against"],
            "Red Cards For": viz.COLORS["red_cards"],
            "Red Cards Against": viz.COLORS["red_cards"],
        }
    )

    viz.apply_common_layout(
        fig,
        title="Cards per Match",
        x_axis_title="Average per Match",
        y_axis_title="",
    )
    viz.apply_category_hover(
        fig,
        category_label="",
        value_label="Average per Match",
    )

    viz.render_chart(st, fig)


st.divider()

st.header("Recent Form")
form = queries.get_recent_team_form(conn, team, window)
viz.render_form_badges(st, form)


st.divider()

st.header("Last Matches")

recent_matches = queries.get_recent_team_matches(conn, team, window)

if recent_matches.empty:
    st.info("No matches found.")

else:
    colors = {
        "W": "#119DA4",
        "D": "#FFC857",
        "L": "#1F2041",
        "?": "#808080",
    }

    rows = ""

    for _, match in recent_matches.iterrows():

        home_team = match["home_team"]
        away_team = match["away_team"]

        home_goals = match["home_goals"]
        away_goals = match["away_goals"]

        result = match["result"]

        # Bold the winning team
        if home_goals > away_goals:
            home_team_html = f"<strong>{home_team}</strong>"
            away_team_html = away_team

        elif away_goals > home_goals:
            home_team_html = home_team
            away_team_html = f"<strong>{away_team}</strong>"

        else:
            home_team_html = home_team
            away_team_html = away_team

        result_color = colors.get(result, "#808080")

        rows += f"""
        <div style="
            display: grid;
            grid-template-columns: 100px 1fr 100px 1fr 50px;
            align-items: center;
            padding: 10px 0;
            border-bottom: 1px solid #E5E7EB;
        ">
            <div>{match["date"]}</div>

            <div style="text-align: right; padding-right: 15px;">
                {home_team_html}
            </div>

            <div style="
                text-align: center;
                font-weight: 600;
            ">
                {home_goals} - {away_goals}
            </div>

            <div style="padding-left: 15px;">
                {away_team_html}
            </div>

            <div style="
                text-align: center;
                font-weight: 600;
                color: {result_color};
            ">
                {result}
            </div>
        </div>
        """

    st.html(rows)


st.divider()    

st.header("Statistics")

team_trend_statistics = viz.sort_seasons(queries.get_team_trend_statistics(conn, team))

tab1, tab2, tab3, tab4 = st.tabs([
    "Goals",
    "Shots",
    "Corners",
    "Cards"
])

with tab1:
    goals = team_trend_statistics[["season", "avg_goals_for", "avg_goals_against"]].rename(
        columns={
            "avg_goals_for": "Goals For",
            "avg_goals_against": "Goals Against",
        }
    )

    fig = px.line(
        goals,
        x="season",
        y=["Goals For", "Goals Against"],
        markers=True,
        title="Goals per Match",
        color_discrete_map={
            "Goals For": viz.COLORS["for"],
            "Goals Against": viz.COLORS["against"],
        },
    )

    viz.apply_common_layout(
        fig,
        title="Goals per Match",
        x_axis_title="Season",
        y_axis_title="Goals per Match",
    )
    viz.apply_standard_hover(fig, x_label="Season", y_label="Value")

    viz.render_chart(st, fig)

with tab2:
    shots = team_trend_statistics[
        [
            "season",
            "avg_shots_for",
            "avg_shots_on_target_for",
            "avg_shots_against",
            "avg_shots_on_target_against",
        ]
    ].rename(
        columns={
            "avg_shots_for": "Shots For",
            "avg_shots_on_target_for": "Shots on Target For",
            "avg_shots_against": "Shots Against",
            "avg_shots_on_target_against": "Shots on Target Against",
        }
    )

    fig = px.line(
        shots,
        x="season",
        y=["Shots For", "Shots Against", "Shots on Target For", "Shots on Target Against"],
        markers=True,
        title="Shots per Match",
        color_discrete_map={
            "Shots For": viz.COLORS["for"],
            "Shots Against": viz.COLORS["against"],
            "Shots on Target For": viz.COLORS["shots_on_target"],
            "Shots on Target Against": viz.COLORS["shots_on_target"],
        },
    )

    fig.update_traces(
        selector={"name": "Shots on Target Against"},
        line={"dash": "dash"},
    )

    viz.apply_common_layout(
        fig,
        title="Shots per Match",
        x_axis_title="Season",
        y_axis_title="Shots per Match",
    )
    viz.apply_standard_hover(fig, x_label="Season", y_label="Value")

    viz.render_chart(st, fig)

with tab3:
    corners = team_trend_statistics[["season", "avg_corners_for", "avg_corners_against"]].rename(
        columns={
            "avg_corners_for": "Corners For",
            "avg_corners_against": "Corners Against",
        }
    )

    fig = px.line(
        corners,
        x="season",
        y=["Corners For", "Corners Against"],
        markers=True,
        title="Corners per Match",
        color_discrete_map={
            "Corners For": viz.COLORS["for"],
            "Corners Against": viz.COLORS["against"],
        },
    )

    viz.apply_common_layout(
        fig,
        title="Corners per Match",
        x_axis_title="Season",
        y_axis_title="Corners per Match",
    )
    viz.apply_standard_hover(fig, x_label="Season", y_label="Value")

    viz.render_chart(st, fig)

with tab4:
    cards = team_trend_statistics[
        [
            "season",
            "avg_yellow_cards_for",
            "avg_yellow_cards_against",
            "avg_red_cards_for",
            "avg_red_cards_against",
        ]
    ].rename(
        columns={
            "avg_yellow_cards_for": "Yellow Cards For",
            "avg_yellow_cards_against": "Yellow Cards Against",
            "avg_red_cards_for": "Red Cards For",
            "avg_red_cards_against": "Red Cards Against",
        }
    )
    
    fig = px.line(
        cards,
        x="season",
        y=["Yellow Cards For", "Yellow Cards Against", "Red Cards For", "Red Cards Against"],
        markers=True,
        title="Cards per Match",
        color_discrete_map={
            "Yellow Cards For": viz.COLORS["for"],
            "Yellow Cards Against": viz.COLORS["against"],
            "Red Cards For": viz.COLORS["red_cards"],
            "Red Cards Against": viz.COLORS["red_cards"],
        },
    )

    fig.update_traces(
        selector={"name": "Red Cards Against"},
        line={"dash": "dash"},
    )

    viz.apply_common_layout(
        fig,
        title="Cards per Match",
        x_axis_title="Season",
        y_axis_title="Cards per Match",
    )
    viz.apply_standard_hover(fig, x_label="Season", y_label="Value")

    viz.render_chart(st, fig)