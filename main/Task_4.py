import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# -----------------------------
# Load data
# -----------------------------

df = pd.read_csv(r"D:\Python\Quantium\quantium-starter-repo-main\quantium-starter-repo-main\data\formatted_output.csv")

df["Date"] = pd.to_datetime(df["Date"])

daily_sales = (
    df.groupby(["Date", "Region"])["Sales"]
    .sum()
    .reset_index()
)

# -----------------------------
# App
# -----------------------------

app = Dash(__name__)

app.layout = html.Div([

    # HEADER
    html.Div([
        html.Img(
            src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTDOj-Xv6gLbWVu8iiniZOWcQv_FvDCfcg0AQ&s",
            className="logo"
        ),

        html.Div([
            html.H1(
                "Soul Foods Sales Intelligence Dashboard",
                className="title"
            ),

            html.P(
                "Assessing the impact of the Pink Morsel price increase",
                className="subtitle"
            )
        ])
    ],
    className="header"),


    # FILTER CARD

    html.Div([

        html.H3(
            "Sales Region Filter",
            className="section-title"
        ),

        dcc.RadioItems(
            id="region-filter",

            options=[
                {"label": " All Regions", "value": "all"},
                {"label": " North", "value": "north"},
                {"label": " East", "value": "east"},
                {"label": " South", "value": "south"},
                {"label": " West", "value": "west"}
            ],

            value="all",

            inline=True,

            className="radio-group"
        )

    ],
    className="filter-card"),


    # CHART CARD

    html.Div([

        dcc.Graph(
            id="sales-chart"
        )

    ],
    className="chart-card")

])

# -----------------------------
# Callback
# -----------------------------

@app.callback(
    Output("sales-chart", "figure"),
    Input("region-filter", "value")
)

def update_chart(selected_region):

    if selected_region == "all":

        chart_data = (
            daily_sales.groupby("Date")["Sales"]
            .sum()
            .reset_index()
        )

    else:

        chart_data = daily_sales[
            daily_sales["Region"].str.lower() == selected_region
        ]

    fig = px.line(
        chart_data,
        x="Date",
        y="Sales",
        markers=True
    )

    fig.add_vline(
        x="2021-01-15",
        line_dash="dash",
        line_width=3,
        annotation_text="Price Increase",
        annotation_position="top right"
    )

    fig.update_layout(

        title="Pink Morsel Sales Trend",

        paper_bgcolor="#111827",
        plot_bgcolor="#111827",

        font=dict(
            family="Inter",
            color="white"
        ),

        title_font=dict(
            size=24
        ),

        xaxis_title="Date",
        yaxis_title="Sales Revenue ($)",

        hovermode="x unified",

        margin=dict(
            l=40,
            r=40,
            t=60,
            b=40
        )
    )

    fig.update_traces(
        line=dict(width=4)
    )

    return fig


if __name__ == "__main__":
    app.run(debug=True)