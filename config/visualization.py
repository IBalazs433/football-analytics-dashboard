import pandas as pd
import plotly.express as px


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
    fig.update_traces(
        hovertemplate=(
            "<b>%{label}</b><br>"
            + value_label
            + ": %{value:,.0f}<br>"
            "Share: %{percent:.1%}<extra></extra>"
        )
    )
    return fig


def render_chart(st, fig):
    st.plotly_chart(fig, use_container_width=True)
