import duckdb
import dash_bootstrap_components as dbc
from dash import html

con = duckdb.connect("crashes.duckdb", read_only=True)

kpi_query = con.execute("""
    SELECT 
        COUNT(*) AS total_collisions, 
        SUM(PERSONS_KILLED) AS persons_killed, 
        SUM(PERSONS_INJURED) AS persons_injured
    FROM crashes
""").fetchone()

total_crashes, persons_killed, persons_injured = map(int, kpi_query)


def kpi():
    return dbc.Row(
        children=[
            dbc.Col(
                dbc.Card(
                    children=[
                        dbc.CardBody(
                            html.H4(f"{total_crashes:,}"),
                            className="p-1 text-center text-nowrap",
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
    )
