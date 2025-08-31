import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, html, dcc
from header import header, filter
from kpi import kpi
import duckdb
from line_word import row
from dash_bootstrap_templates import ThemeSwitchAIO
import plotly.express as px


con = duckdb.connect("crashes.duckdb", read_only=True)

app = Dash(
    external_stylesheets=[dbc.themes.DARKLY],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)

app.title = "NYC Vehicle Collisions Analysis"


app.layout = (
    dbc.Container(
        children=[header(), filter(), html.Div(id="content")],
        fluid=True,
    ),
)

bar_query = """
    SELECT 
        WEEKDAY, 
        COUNT(WEEKDAY) AS counts
    FROM crashes
    WHERE BOROUGH IN ? AND YEAR BETWEEN ? AND ?
    GROUP BY WEEKDAY
    ORDER BY counts ASC;
 """


def bar_chart(borough, year_range, template, con):
    start_year, end_year = year_range

    if not borough:
        borough = ["QUEENS", "BROOKLYN", "MANHATTAN", "BRONX", "STATEN ISLAND"]

    params = (borough, start_year, end_year)

    bardf = con.execute(bar_query, parameters=params).df()

    fig = px.bar(
        bardf,
        x="counts",
        y="WEEKDAY",
        color="counts",
        template=template,
        color_continuous_scale="YlOrRd",
    ).update_layout(
        coloraxis_showscale=False,
        margin=dict(t=10, b=10, l=10, r=10),
        xaxis=dict(title="Number of Collisions"),
        yaxis=dict(title="Day of Week"),
    )

    return fig


@app.callback(
    Output("content", "children"),
    [
        Input("borough-checklist", "value"),
        Input("year-range", "value"),
        Input(ThemeSwitchAIO.ids.switch("theme"), "value"),
    ],
)
def update_app(borough, year_range, toggle):
    template = "flatly" if toggle else "darkly"
    return [
        kpi(borough, year_range, template, con),
        row(borough, year_range, template, con),
        dbc.Row(
            children=dbc.Col(
                children=[
                    dbc.Card(
                        children=[
                            dbc.CardHeader(
                                "Crash Frequency by Day of Week",
                                className="fw-bold border-0",
                            ),
                            dbc.CardBody(
                                children=[
                                    dcc.Graph(
                                        figure=bar_chart(
                                            borough, year_range, template, con
                                        ),
                                        config={
                                            "displayModeBar": False,
                                            "staticPlot": True,
                                        },
                                    )
                                ],
                                className="border-0 flex-grow-0",
                            ),
                            dbc.CardFooter(
                                "Bar chart showing crash frequency throughout the week",
                                className="fw-bold border-0",
                            ),
                        ],
                        className="border-0 shadow-lg",
                    )
                ],
                xs=12,
                md=4,
            ),
            className="mt-3 gy-3",
        ),
    ]


if __name__ == "__main__":
    app.run(debug=True)
