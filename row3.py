import dash_bootstrap_components as dbc
from dash import dcc, html
import plotly.express as px


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
    return html.Section(
        html.Div(
            children=[
                html.Div(
                    children=[
                        dbc.Card(
                            dbc.CardHeader(
                                "Crash Frequency by Day of Week",
                                className="border-0 fw-bold mb-2",
                            ),
                            className="border-0",
                        ),
                        html.Div(
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
                        dbc.Card(
                            dbc.CardFooter(
                                "Tip: You can switch layers on and off by clicking items in the legend",
                                className="border-0 fw-bold mb-2",
                            ),
                            className="border-0 text-center",
                        ),
                    ],
                    className="shadow-lg rounded-md border-[#848484] p-4",
                ),
            ]
        ),
        className="container mx-auto space-y-5 px-4 mb-3",
    )
