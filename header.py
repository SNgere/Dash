import dash_bootstrap_components as dbc
from dash import html
from dash_bootstrap_templates import ThemeSwitchAIO
from dash import dcc

icons = "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"


def header():
    return html.Section(
        children=[
            html.Div(
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
                className="flex justify-end",
            ),
            html.Div(
                children=[
                    html.H2(
                        "NYC Motor Vehicles Crashes Dashboard",
                        className="text-3xl md:text-3xl lg:text-4xl font-bold",
                    ),
                    html.P(
                        "Real-time analysis of traffic incidents across New York City",
                        className="font-extrabold mb-2",
                    ),
                    html.Small(
                        children=[
                            html.I(
                                className="fa-solid fa-arrows-rotate fa-1x",
                            ),
                            html.Span(
                                children="Last Updated: Aug 25 2025",
                                className="pl-1",
                            ),
                        ],
                        className="flex-grow-0 bg-yellow-300 text-black font-light p-2 rounded-md font-[serif]",
                    ),
                ],
                className="text-center",
            ),
        ]
    )


def filter2():
    return html.Section(
        children=[
            html.H3("Filters", className="font-bold underline underline-offset-2"),
            html.Div(
                children=[
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
                        className="flex flex-wrap justify-center"
                    ),
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
                ],
                className="grid grid-cols-1 lg:grid-cols-2 gap-3 lg:gap-1 items-center mt-2"
            ),
        ],
        className="mx-auto max-w-7xl py-4"
    )


def filter():
    return dbc.Row(
        dbc.Col(
            dbc.Card(
                [
                    dbc.CardHeader(
                        "Filters", className="border-0 bg-transparent fw-bold"
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
