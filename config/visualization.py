import pandas as pd


COLORS = {
    "for": "#1F2041",
    "against": "#119DA4",
    "wins": "#119DA4",
    "draws": "#FFC857",
    "losses": "#1F2041",
    "shots_on_target": "#1F2041",
    "shots_off_target": "#119DA4",
    "red_cards": "#FF5722",
    "neutral": "#808080",
}


def sort_seasons(df: pd.DataFrame, season_column: str = "season") -> pd.DataFrame:
    """Return a season DataFrame sorted chronologically from earliest to latest."""
    return df.sort_values(by=season_column, ascending=True)


def apply_common_layout(
    fig,
    title: str,
    x_axis_title: str,
    y_axis_title: str,
    legend_title: str = "",
    y_tickformat: str = ",.2f",
    x_tickformat: str | None = None,
):
    """Apply the shared Plotly styling used throughout the dashboard."""
    fig.update_layout(
        template="plotly_white",
        title=title,
        xaxis_title=x_axis_title,
        yaxis_title=y_axis_title,
        legend_title=legend_title,
        margin={"l": 16, "r": 16, "t": 56, "b": 16},
        hoverlabel={"bgcolor": "white"},
    )
    fig.update_yaxes(rangemode="tozero", tickformat=y_tickformat)
    if x_tickformat:
        fig.update_xaxes(tickformat=x_tickformat)
    return fig


def apply_standard_hover(
    fig,
    x_label: str,
    y_label: str,
    value_format: str = ",.2f",
):
    """Apply a consistent hover template for simple line/bar charts."""
    fig.update_traces(
        hovertemplate=(
            f"<b>%{{fullData.name}}</b><br>"
            f"{x_label}: %{{x}}<br>"
            f"{y_label}: %{{y:{value_format}}}"
            "<extra></extra>"
        )
    )
    return fig


def apply_category_hover(
    fig,
    category_label: str,
    value_label: str,
    value_format: str = ",.2f",
):
    """Apply the hover formatting used for horizontal category charts."""
    fig.update_traces(
        hovertemplate=(
            f"<b>%{{y}}</b><br>"
            f"{value_label}: %{{x:{value_format}}}"
            "<extra></extra>"
        )
    )
    fig.update_layout(yaxis_title=category_label)
    return fig


def apply_stacked_hover(fig, category_axis: str, value_format: str = ",.2f"):
    """Apply hover formatting for stacked bar charts."""
    if category_axis == "y":
        fig.update_traces(
            hovertemplate=(
                "<b>%{y}</b><br>"
                "%{fullData.name}: %{x:" + value_format + "}"
                "<extra></extra>"
            )
        )
    else:
        fig.update_traces(
            hovertemplate=(
                "<b>%{x}</b><br>"
                "%{fullData.name}: %{y:" + value_format + "}"
                "<extra></extra>"
            )
        )
    return fig


def apply_pie_hover(fig, value_label: str):
    """Apply the hover formatting used for pie charts."""
    fig.update_traces(
        hovertemplate=(
            "<b>%{label}</b><br>"
            + value_label
            + ": %{value:,.0f}<br>"
            "Share: %{percent:.1%}<extra></extra>"
        )
    )
    return fig


def render_form_badges(st, form_string: str) -> None:
    """Render a compact form summary with the shared dashboard badge colors."""
    if not form_string:
        return

    colors = {
        "W": COLORS["wins"],
        "D": COLORS["draws"],
        "L": COLORS["losses"],
        "?": COLORS["neutral"],
    }

    results = [result for result in form_string.split() if result]
    if not results:
        return

    badges = []
    for result in results:
        badges.append(
            f"""
            <div style="display: flex; justify-content: center; align-items: center; width: 32px; height: 32px; min-width: 32px; border-radius: 5px; background-color: {colors.get(result, COLORS['neutral'])}; color: white; font-weight: 600;">
                {result}
            </div>
            """
        )

    st.html(f'<div style="display: flex; gap: 6px; flex-wrap: wrap;">{"".join(badges)}</div>')


def render_chart(st, fig):
    """Render a Plotly chart using the shared dashboard stretch layout."""
    st.plotly_chart(fig, width="stretch")
