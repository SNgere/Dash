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

    return html.Section(
        children=[
            html.Div(
                children=[
                    html.Div(
                        children=[
                            html.Div(
                                children=[
                                    html.Small(
                                        "Total Crashes", className="text-gray-500"
                                    ),
                                    html.H2(
                                        f"{total_crashes:,}",
                                        className="text-blue-700 font-extrabold text-lg md:text-xl lg:text-2xl",
                                    ),
                                ]
                            ),
                        ],
                        className="sp-4",
                    ),
                    html.Div(
                        children=[
                            html.Div(
                                children=[
                                    html.Small(
                                        "Total Injured", className="text-gray-500"
                                    ),
                                    html.H2(
                                        f"{persons_injured:,}",
                                        className="text-green-700 font-extrabold text-lg md:text-xl lg:text-2xl",
                                    ),
                                ]
                            ),
                        ],
                        className="p-4",
                    ),
                    html.Div(
                        children=[
                            html.Div(
                                children=[
                                    html.Small(
                                        "Total Killed", className="text-gray-500"
                                    ),
                                    html.H2(
                                        f"{persons_killed:,}",
                                        "text-red-700 font-extrabold text-lg md:text-xl lg:text-2xl",
                                    ),
                                ]
                            )
                        ],
                        className="p-4",
                    ),
                ],
                className="grid grid-cols-3 gap-3 text-center",
            ),
        ],
        className="mx-auto max-w-4xl p-4 lg:p-8",
    )
