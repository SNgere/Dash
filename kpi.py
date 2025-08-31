import dash_bootstrap_components as dbc
from dash import html

kpi_query = """
    SELECT 
        COUNT(*) AS total_collisions, 
        SUM(PERSONS_KILLED) AS persons_killed, 
        SUM(PERSONS_INJURED) AS persons_injured
    FROM crashes
    WHERE BOROUGH IN ? AND YEAR BETWEEN ? AND ?                       
"""


def kpi(borough, year_range, template, con):
    start_year, end_year = year_range

    if not borough:
        borough = ["QUEENS", "BROOKLYN", "MANHATTAN", "BRONX", "STATEN ISLAND"]

    params = (borough, start_year, end_year)

    total_crashes, persons_killed, persons_injured = map(
        int, con.execute(kpi_query, parameters=params).fetchone()
    )

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
