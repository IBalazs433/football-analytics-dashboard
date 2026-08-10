import pandas as pd
import plotly.express as px
import streamlit as st
from config import visualization as viz

import database.queries as queries


conn = queries.get_connection()

st.set_page_config(
    page_title="Match Analysis",
    page_icon="🔎",
    layout="wide"
)


st.sidebar.header("Filters")

country = st.sidebar.selectbox(
    "Country",
    queries.get_countries(conn).iloc[:, 0].tolist(),
)

league = st.sidebar.selectbox(
    "League",
    queries.get_leagues(conn, country).iloc[:, 0].tolist(),
)

season = st.sidebar.selectbox(
    "Season",
    queries.get_seasons(conn, league).iloc[:, 0].tolist(),
)

home_team = st.sidebar.selectbox(
    "Home Team",
    queries.get_teams_from_season(conn, country, league, season).iloc[:, 0].tolist(),
)

away_team = st.sidebar.selectbox(
    "Away Team",
    queries.get_teams_from_season(conn, country, league, season).iloc[:, 0].tolist(),
    index=1,
)

date = st.sidebar.selectbox(
    "Date",
    queries.get_match_dates(conn, country, league, season, home_team, away_team).iloc[:, 0].tolist(),
)


st.title("🔎 Match Analysis")

st.markdown("""
Explore detailed statistics and match context for individual football matches.
""")


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

    match_row = match_df.iloc[0]

    performance = pd.DataFrame([
        {"Metric": "Shots", "Team": "Home", "Value": match_row["home_shots"]},
        {"Metric": "Shots", "Team": "Away", "Value": match_row["away_shots"]},
        {"Metric": "Shots on Target", "Team": "Home", "Value": match_row["home_shots_on_target"]},
        {"Metric": "Shots on Target", "Team": "Away", "Value": match_row["away_shots_on_target"]},
        {"Metric": "Corners", "Team": "Home", "Value": match_row["home_corners"]},
        {"Metric": "Corners", "Team": "Away", "Value": match_row["away_corners"]},
        {"Metric": "Yellow Cards", "Team": "Home", "Value": match_row["home_yellow_cards"]},
        {"Metric": "Yellow Cards", "Team": "Away", "Value": match_row["away_yellow_cards"]},
        {"Metric": "Red Cards", "Team": "Home", "Value": match_row["home_red_cards"]},
        {"Metric": "Red Cards", "Team": "Away", "Value": match_row["away_red_cards"]},
    ])

    fig = px.bar(
        performance,
        x="Metric",
        y="Value",
        color="Team",
        barmode="group",
        title="Match Event Profile",
        color_discrete_map={
            "Home": viz.COLORS["for"],
            "Away": viz.COLORS["against"],
        },
    )

    viz.apply_common_layout(
        fig,
        title="Match Event Profile",
        x_axis_title="Metric",
        y_axis_title="Count",
        y_tickformat=",.0f",
    )
    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>%{fullData.name}: %{y:,.0f}<extra></extra>"
    )

    viz.render_chart(st, fig)


    st.divider()

    st.header(f"{home_team} Form Before Match")
    form = queries.get_recent_team_form_before_date(conn, home_team, 5, date=date)
    viz.render_form_badges(st, form)

    st.header(f"{away_team} Form Before Match")
    form = queries.get_recent_team_form_before_date(conn, away_team, 5, date=date)
    viz.render_form_badges(st, form)


    st.divider()

    st.header("Previous Meetings")

    recent_matches = queries.get_head_to_head_matches_before_date(conn, home_team, away_team, 5, date=date)

    if recent_matches.empty:
        st.info("No matches found.")

    else:
        rows = ""

        for _, match in recent_matches.iterrows():

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
