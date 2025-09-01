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

bar_query ="""
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



def line_chart(borough, year_range, template, con):
    start_year, end_year = year_range

    if not borough:
        borough = ["QUEENS", "BROOKLYN", "MANHATTAN", "BRONX", "STATEN ISLAND"]

    params = (borough, start_year, end_year)

    linedf = con.execute(line_query, parameters=params).df()

    fig = px.line(
        linedf,
        x="Year",
        y="total_collisions",
        color="BOROUGH",
        markers=True,
        color_discrete_sequence=px.colors.qualitative.Set1,
        line_shape="spline",
        # range_x=[2012, 2025],
        # template="darkly",
        template=template,
        category_orders={
            "BOROUGH": ["BROOKLYN", "QUEENS", "MANHATTAN", "BRONX", "STATEN ISLAND"]
        },
    ).update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=1),
        yaxis=dict(title="Number of Collisions"),
        legend_title=None,
        margin=dict(t=10, b=40, l=10, r=10),
    )
    return fig


def bar_plot(borough, year_range, template, con):
    start_year, end_year = year_range

    if not borough:
        borough = ["QUEENS", "BROOKLYN", "MANHATTAN", "BRONX", "STATEN ISLAND"]

    params = (borough, start_year, end_year)
    dfb = con.execute(bar_query, parameters=params).df()

    fig_bar = px.bar(
        dfb,
        x="Vehicles",
        y="count",
        color="Vehicles",
        orientation="v",
        # title="Top vehicle types in collisions",
        text_auto=".2s",
        color_discrete_sequence=px.colors.qualitative.Set1,
        template=template,
    ).update_layout(
        showlegend=False,
        autosize=True,
        margin=dict(t=40, r=10, b=20, l=10),
        yaxis=dict(title="Number of Collisions"),
    )
    return fig_bar



def row2(borough, year_range, template, con):
    return dbc.Row(
        children=[
            dbc.Col(
                children=[
                    dbc.Card(
                        children=[
                            dbc.CardHeader(
                                "Crashes by Borough Over Time",
                                className="fw-bold border-0",
                            ),
                            dbc.CardBody(
                                children=[
                                    dcc.Graph(
                                        figure=line_chart(
                                            borough, year_range, template, con
                                        ),
                                        config={
                                            "displayModeBar": False,
                                            "staticPlot": True,
                                        },
                                    )
                                ],
                                className="border-0",
                            ),
                        ],
                        className="border-0 shadow-lg",
                    )
                ],
                xs=12,
                md=6,
            ),
            dbc.Col(
                children=[
                    dbc.Card(
                        children=[
                            dbc.CardHeader(
                                "Top vehicle types in collisions",
                                className="fw-bold border-0",
                            ),
                            dbc.CardBody(
                                children=[
                                    dcc.Graph(
                                        figure=bar_plot(
                                            borough, year_range, template, con
                                        ),
                                        config={
                                            "displayModeBar": False,
                                            "staticPlot": True,
                                        },
                                    )
                                ],
                                className="border-0",
                            ),
                        ],
                        className="border-0 shadow-lg",
                    )
                ],
                xs=12,
                md=5,
            ),
        ],
        className="mt-1 gy-3 mb-3",
        justify="center",
    )
