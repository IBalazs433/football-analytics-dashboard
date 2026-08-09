import database.queries as queries
import streamlit as st


conn = queries.get_connection()

st.set_page_config(
    page_title="Football Analytics Dashboard",
    page_icon="⚽",
    layout="wide",
)

st.title("⚽ Football Analytics Dashboard")

st.markdown("""
Interactive football analytics dashboard built with **SQLite**, **Python**, **Pandas**, **Plotly** and **Streamlit**.
""")


st.divider()

st.subheader("Project")

st.markdown("""
Explore football data across **countries**, **leagues**, **seasons**, **teams**, and **individual matches** through interactive tables, statistics, and visualizations.
""")

st.markdown("""
Use the navigation menu on the left to start exploring.
""")


st.divider()

st.subheader("Database")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Countries", queries.get_number_of_countries(conn))
    st.metric("Leagues", queries.get_number_of_leagues(conn))

with c2:
    st.metric("Seasons", queries.get_number_of_seasons(conn))
    st.metric("Teams", queries.get_number_of_teams(conn))

with c3:
    st.metric("Matches", queries.get_number_of_matches(conn))
    st.metric("Goals", queries.get_number_of_goals(conn))

st.markdown("""
**Current coverage**

🇬🇧 **England** — Premier League  
🇩🇪 **Germany** — Bundesliga  
🇪🇸 **Spain** — La Liga  
🇮🇹 **Italy** — Serie A  
🇫🇷 **France** — Ligue 1
""")

st.markdown("""
**Data included**

- Leagues and seasons
- Teams
- Matches
- Goals
- Shots
- Shots on target
- Corners
- Yellow & red cards
""")

st.metric("First match in database", queries.get_first_match_date(conn))
st.metric("Last match in database", queries.get_last_match_date(conn))


st.divider()

st.subheader("Pages")

st.markdown("""
📊 **League Analysis** — Analyze league standings, performance, and historical trends.  
⚽ **Team Analysis** — Explore team form, performance, and match statistics.  
🤝 **Head-to-Head** — Compare the historical performance of two teams.  
🔎 **Match Analysis** — Explore detailed statistics for individual matches.  
""")