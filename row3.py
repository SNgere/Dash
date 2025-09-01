import dash_bootstrap_components as dbc
from dash import dcc
import plotly.express as px

line_query = """
SELECT 
    BOROUGH,
    YEAR AS Year,
    COUNT(*) AS total_collisions
FROM crashes
WHERE BOROUGH IN ? AND YEAR BETWEEN ? AND ?
GROUP BY BOROUGH,YEAR
ORDER BY BOROUGH, YEAR;
"""

bar_query = """
WITH all_vehicles AS (
    SELECT BOROUGH, Year, "VEHICLE TYPE CODE 1" AS Vehicles
    FROM crashes
    WHERE "VEHICLE TYPE CODE 1" IS NOT NULL AND "VEHICLE TYPE CODE 1" <> ''
    UNION ALL
    SELECT BOROUGH, Year, "VEHICLE TYPE CODE 2" AS Vehicles
    FROM crashes
    WHERE "VEHICLE TYPE CODE 2" IS NOT NULL AND "VEHICLE TYPE CODE 2" <> ''
    UNION ALL
    SELECT BOROUGH, Year, "VEHICLE TYPE CODE 3" AS Vehicles
    FROM crashes
    WHERE "VEHICLE TYPE CODE 3" IS NOT NULL AND "VEHICLE TYPE CODE 3" <> ''
    UNION ALL
    SELECT BOROUGH, Year, "VEHICLE TYPE CODE 4" AS Vehicles
    FROM crashes
    WHERE "VEHICLE TYPE CODE 4" IS NOT NULL AND "VEHICLE TYPE CODE 4" <> ''
    UNION ALL
    SELECT BOROUGH, Year, "VEHICLE TYPE CODE 5" AS Vehicles
    FROM crashes
    WHERE "VEHICLE TYPE CODE 5" IS NOT NULL AND "VEHICLE TYPE CODE 5" <> ''
)
SELECT
    Vehicles,
    COUNT(*) AS count
FROM all_vehicles
WHERE BOROUGH IN ? AND YEAR BETWEEN ? AND ?
GROUP BY Vehicles
ORDER BY count DESC
LIMIT 6;
"""


map_query = """
SELECT
    BOROUGH,
    "PERSONS_INJURED",
    "PERSONS_KILLED",
    "CONTRIBUTING FACTOR VEHICLE 1" AS "CONTRIBUTING FACTOR",
    "VEHICLE TYPE CODE 1" AS "VEHICLE TYPE",
    LATITUDE, 
    LONGITUDE
FROM crashes
WHERE BOROUGH IN ? AND YEAR = 2025 
"""


def map(borough, template, con):
    if not borough:
        borough = ["QUEENS", "BROOKLYN", "MANHATTAN", "BRONX", "STATEN ISLAND"]

    params = (borough,)

    mapdf = con.execute(map_query, parameters=params).df()

    return (
        px.scatter_map(
            mapdf,
            lat="LATITUDE",
            lon="LONGITUDE",
            color="BOROUGH",
            center={"lat": 40.7128, "lon": -74.0060},  # Center on NYC
            # size='NUMBER OF PERSONS KILLED',
            # size_max=15,
            zoom=9,
            height=700,
            # title="NYC Traffic Collisions by Borough",
            template=template,
            map_style="open-street-map",  #'carto-positron', #'open-street-map',  #'carto-positron',
            color_discrete_sequence=px.colors.qualitative.Prism,
            # color_discrete_sequence=px.colors.qualitative.Antique,
            hover_data=[
                "PERSONS_INJURED",
                "PERSONS_KILLED",
                "CONTRIBUTING FACTOR",
                "VEHICLE TYPE",
            ],
            # hover_name='BOROUGH',
        )
        .update_traces(
            cluster=dict(enabled=True, step=50, size=20), marker=dict(size=20)
        )
        .update_layout(
            margin=dict(b=20, l=10, r=10, t=10),
            # showlegend=False,
            legend=dict(orientation="h", y=1, yanchor="bottom"),
            legend_title=None,
        )
    )


def row3(borough, year_range, template, con):
    return dbc.Row(
        children=[
            dbc.Col(
                children=[
                    dbc.Card(
                        children=[
                            dbc.CardHeader(
                                "Geographic Distribution of Crashes (2025 Only)",
                                className="fw-bold border-0",
                            ),
                            dbc.CardBody(
                                children=[
                                    dcc.Graph(
                                        figure=map(borough, template, con),
                                        config={
                                            "displayModeBar": False,
                                            "staticPlot": False,
                                        },
                                    )
                                ],
                                className="border-0",
                            ),
                            dbc.CardFooter(
                                "Tip: You can switch layers on and off by clicking items in the legend",
                                className="fw-bold border-0 text-center font-italic",
                            ),
                        ],
                        className="border-0 shadow-lg",
                    )
                ],
                xs=12,
                md=10,
            ),
        ],
        className="mt-1 gy-3 mb-5",
        justify="center",
    )
