import dash_bootstrap_components as dbc
from dash import Dash, html
from dash_bootstrap_templates import ThemeSwitchAIO


icons = "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"


app = Dash(
    external_stylesheets=[dbc.themes.DARKLY, icons],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)

app.title = "NYC Vehicle Collisions Analysis"

app.layout = (
    dbc.Container(
        children=[
            dbc.Row(
                children=[
                    dbc.Col(
                        children=[
                            html.H1(
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
                            # html.Span(
                            #     "Theme",
                            #     className="me-3 small",
                            # ),
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
                className="mt-3 shadow",
            ),
        ],
        fluid=True,
    ),
)


if __name__ == "__main__":
    app.run(debug=True)
