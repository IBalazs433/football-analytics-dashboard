import database.queries as queries
import streamlit as st
import plotly.express as px
import pandas as pd
from config import visualization as viz


conn = queries.get_connection()
    
st.set_page_config(
    page_title="Head-to-Head",
    page_icon="🤝",
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

teams = queries.get_teams(conn, country).iloc[:, 0].tolist()
index_1 = teams.index("Liverpool") if "Liverpool" in teams else 0
team_a = st.sidebar.selectbox(
    "Team A",
    teams,
    index=index_1
)

index_2 = teams.index("Man United") if "Man United" in teams else 1
team_b = st.sidebar.selectbox(
    "Team B",
    teams,
    index=index_2,
)

window = st.sidebar.selectbox(
    "Rolling Window",
    [5, 10, 15, 20, 25, 30],
)


st.title("🤝 Head-to-Head")

st.markdown("""
Compare the historical performance and statistics of two teams across their previous meetings.
""")


st.header("Overall Record")

head_to_head_statistics = queries.get_recent_head_to_head_statistics(conn, team_a, team_b, window)

if head_to_head_statistics.empty:
    st.info("No head-to-head statistics found for the selected teams.")
    st.stop()

statistics = head_to_head_statistics.iloc[0]

col1, col2 = st.columns(2)

with col1:
    st.metric("Matches", int(statistics["matches"]))
    st.metric(f"{team_a} Wins", int(statistics["team_a_wins"]))
    st.metric(f"{team_b} Wins", int(statistics["team_b_wins"]))
    st.metric("Draws", int(statistics["draws"]))

with col2:
    outcomes = {
        "Result": [f"{team_a} Win", f"{team_b} Win", "Draw"],
        "Matches": [
            statistics["team_a_wins"],
            statistics["team_b_wins"],
            statistics["draws"]]
    }

    fig = px.pie(
        outcomes, 
        names="Result", 
        values="Matches", 
        title=f"Head-to-Head Record: {team_a} vs {team_b}",
        color="Result",
        color_discrete_map={
            f"{team_a} Win": viz.COLORS["wins"],
            f"{team_b} Win": viz.COLORS["losses"],
            "Draw": viz.COLORS["draws"],
        }
    )

    viz.apply_common_layout(
        fig,
        title=f"Head-to-Head Record: {team_a} vs {team_b}",
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
        "Statistic": [f"Goals For {team_a}", f"Goals For {team_b}"],
        "Average per Match": [
            statistics["avg_team_a_goals"],
            statistics["avg_team_b_goals"],
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
            f"Goals For {team_a}": viz.COLORS["for"],
            f"Goals For {team_b}": viz.COLORS["against"],
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
        "Team": [f"{team_a}", f"{team_b}"],
        "Shots on Target": [
            statistics["avg_team_a_shots_on_target"],
            statistics["avg_team_b_shots_on_target"],
        ],
        "Shots off Target": [
            statistics["avg_team_a_shots"] - statistics["avg_team_a_shots_on_target"],
            statistics["avg_team_b_shots"] - statistics["avg_team_b_shots_on_target"]
        ]
    })

    fig = px.bar(
        shots,
        x=["Shots on Target", "Shots off Target"],
        y="Team",
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
        "Statistic": [f"Corners For {team_a}", f"Corners For {team_b}"],
        "Average per Match": [
            statistics["avg_team_a_corners"],
            statistics["avg_team_b_corners"]
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
            f"Corners For {team_a}": viz.COLORS["for"],
            f"Corners For {team_b}": viz.COLORS["against"],
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
        "Team": [f"{team_a}", f"{team_b}"],
        "Yellow Cards": [
            statistics["avg_team_a_yellow_cards"],
            statistics["avg_team_b_yellow_cards"]
        ],
        "Red Cards": [
            statistics["avg_team_a_red_cards"],
            statistics["avg_team_b_red_cards"]
        ]
    })

    fig = px.bar(
        cards,
        x=["Yellow Cards", "Red Cards"],
        y="Team",
        orientation="h",
        title="Cards per Match",
        color_discrete_map={
            "Yellow Cards": viz.COLORS["for"],
            "Red Cards": viz.COLORS["red_cards"],
        }
    )

    viz.apply_common_layout(
        fig,
        title="Cards per Match",
        x_axis_title="Average per Match",
        y_axis_title="",
    )
    fig.update_layout(barmode="stack")
    viz.apply_stacked_hover(fig, category_axis="y")

    viz.render_chart(st, fig)


st.divider()

recent_head_to_head_matches = queries.get_recent_head_to_head_matches(conn, team_a, team_b, window)

st.header(f"Last Matches")

if recent_head_to_head_matches.empty:
    st.info("No head-to-head matches found for the selected teams.")
    st.stop()

rows = ""

for _, match in recent_head_to_head_matches.iterrows():

    home_team = match["home_team"]
    away_team = match["away_team"]

    home_goals = match["home_goals"]
    away_goals = match["away_goals"]

    if home_goals > away_goals:
        home_team_html = f"<strong>{home_team}</strong>"
        away_team_html = away_team

    elif away_goals > home_goals:
        home_team_html = home_team
        away_team_html = f"<strong>{away_team}</strong>"

    else:
        home_team_html = home_team
        away_team_html = away_team

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
        </div>
    </div>
    """

st.html(rows)
