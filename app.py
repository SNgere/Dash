import dash_bootstrap_components as dbc
from dash import Dash, html
from header import header, filter
import duckdb

app = Dash(
    external_stylesheets=[dbc.themes.DARKLY],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)

app.title = "NYC Vehicle Collisions Analysis"

con = duckdb.connect("crashes.duckdb", read_only=True)

kpi_query = con.execute("""
    SELECT 
        COUNT(*) AS total_collisions, 
        SUM(PERSONS_KILLED) AS persons_killed, 
        SUM(PERSONS_INJURED) AS persons_injured
    FROM crashes
""").fetchone()

total_crashes, persons_killed, persons_injured = map(int, kpi_query)

app.layout = (
    dbc.Container(
        children=[
            header(),
            filter(),
            dbc.Row(
                children=[
                    dbc.Col(
                        dbc.Card(
                            children=[
                                dbc.CardBody(
                                    html.H4(f"{total_crashes:,}"), className="p-1 text-center text-nowrap"
                                ),
                                dbc.CardFooter(
                                    html.Small("Total Crashes"),
                                    className="text-nowrap",
                                ),
                            ],
                            color="danger",
                            outline=True,
                            class_name="shadow-lg",
                        ),
                        className="flex-grow-0",
                        xs=4,
                        md=1,
                    ),
                    dbc.Col(
                        dbc.Card(
                            children=[
                                dbc.CardBody(
                                    html.H4(f"{persons_injured:,}"), className="p-1 text-center"
                                ),
                                dbc.CardFooter(
                                    html.Small("Total Injured"),
                                    className="text-nowrap",
                                ),
                            ],
                            color="danger",
                            outline=True,
                            class_name="shadow-lg",
                        ),
                        className="flex-grow-0",
                        xs=4,
                        md=1,
                    ),
                    dbc.Col(
                        dbc.Card(
                            children=[
                                dbc.CardBody(
                                    html.H4(f"{persons_killed:,}"), className="p-1 text-center"
                                ),
                                dbc.CardFooter(
                                    html.Small("Total Killed"),
                                    className="text-nowrap",
                                ),
                            ],
                            color="danger",
                            outline=True,
                            class_name="shadow-lg",
                        ),
                        className="flex-grow-0",
                        xs=4,
                        md=1,
                    ),
                ],
                className="mt-3",
                justify="center",
            ),
        ],
        fluid=True,
    ),
)


if __name__ == "__main__":
    app.run(debug=True)
