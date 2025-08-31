import dash_bootstrap_components as dbc
from dash import html
from dash_bootstrap_templates import ThemeSwitchAIO
from dash import dcc

icons = "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"


def header():
    return dbc.Row(
        children=[
            dbc.Col(
                children=[
                    html.H2(
                        "NYC Motor Vehicles Crashes Dashboard",
                        className="text-center text-decoration-none",
                    ),
                    html.P(
                        "Real-time analysis of traffic incidents across New York City",
                        className="text-center font-weight-bolder",
                    ),
                    html.Small(
                        children=[
                            html.Span(
                                children="Last Updated: June 22 2025",
                                className="badge bg-info",
                            ),
                        ],
                        className=" d-block text-center blockquote",
                    ),
                ],
                width={"size": 10},
            ),
            dbc.Col(
                children=[
                    ThemeSwitchAIO(
                        aio_id="theme",
                        themes=[
                            dbc.themes.FLATLY,
                            dbc.themes.DARKLY,
                        ],
                        switch_props={"persistence": True},
                        icons={
                            "left": "fa fa-moon",
                            "right": "fa fa-sun text-warning",
                        },
                    ),
                ],
                width={"size": 2},
            ),
        ],
        className="mt-3",
    )


def filter():
    return dbc.Row(
        dbc.Col(
            dbc.Card(
                [
                    dbc.CardHeader("Filters", className="border-0 bg-transparent"),
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
                                    md=6,
                                    xs=12,
                                ),
                                dbc.Col(
                                    dcc.RangeSlider(
                                        id="year-range",
                                        min=2012,
                                        max=2026,
                                        step=1,
                                        value=[2012, 2026],
                                        marks={
                                            year: str(year) if year % 2 == 0 else ""
                                            for year in range(2012, 2027)
                                        },
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
                                    md=6,
                                    xs=12,
                                ),
                            ],
                            className="gy-2",
                        )
                    ),
                ],
                className="border-0 bg-transparent",
            ),
            width=10,
        ),
        justify="center",
        className="shadow-sm",
    )
