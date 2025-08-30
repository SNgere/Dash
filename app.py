import dash_bootstrap_components as dbc
from dash import Dash, dcc
from header import header

app = Dash(
    external_stylesheets=[dbc.themes.DARKLY],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)

app.title = "NYC Vehicle Collisions Analysis"


app.layout = (
    dbc.Container(
        children=[
            header(),
            dbc.Row(
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                "Filters", className="border-0 bg-transparent"
                            ),
                            dbc.CardBody(
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Checklist(
                                                id="borough-checklist",
                                                options=[
                                                    {"label": b, "value": b.upper()}
                                                    for b in [
                                                        "Queens",
                                                        "Brooklyn",
                                                        "Manhattan",
                                                        "Bronx",
                                                        "Staten Island",
                                                    ]
                                                ],
                                                value=[
                                                    "QUEENS",
                                                    "BROOKLYN",
                                                    "MANHATTAN",
                                                    "BRONX",
                                                    "STATEN ISLAND",
                                                ],
                                                inline=True,
                                                switch=True,
                                            ),
                                            md=6,xs=12
                                        ),
                                        dbc.Col(
                                            dcc.RangeSlider(
                                                id="year-range",
                                                min=2018,
                                                max=2026,
                                                step=1,
                                                value=[2018, 2026],
                                                marks={year: str(year) if year % 2 == 0 else "" for year in range(2018, 2027)},
                                                tooltip={
                                                    "placement": "bottom",
                                                    "always_visible": True,
                                                    "style": {"color": "white"},
                                                },
                                                allowCross=False,
                                                updatemode="mouseup",
                                                pushable=1,
                                                included=True,
                                            ),
                                            md=6,xs=12
                                        ),
                                    ],
                                    className="gy-2"
                                )
                            ),
                        ],
                        className="border-0 bg-transparent",
                    ),
                    width=10,
                ),
                justify="center",
                className="shadow-sm",
            ),
        ],
        fluid=True,
    ),
)


if __name__ == "__main__":
    app.run(debug=True)
