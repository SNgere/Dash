import dash_bootstrap_components as dbc
from dash import dcc
import plotly.express as px
from wordcloud import WordCloud
from io import BytesIO
import base64

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


word_query = """
    WITH factors AS (
    SELECT BOROUGH, Year, "CONTRIBUTING FACTOR VEHICLE 1" AS reasons
    FROM crashes
    UNION ALL
    SELECT BOROUGH, Year, "CONTRIBUTING FACTOR VEHICLE 2"
    FROM crashes
    UNION ALL
    SELECT BOROUGH, Year, "CONTRIBUTING FACTOR VEHICLE 3"
    FROM crashes
    UNION ALL
    SELECT BOROUGH, Year, "CONTRIBUTING FACTOR VEHICLE 4"
    FROM crashes
    UNION ALL
    SELECT BOROUGH, Year, "CONTRIBUTING FACTOR VEHICLE 5"
    FROM crashes
),
reasons AS (
    SELECT Year, reasons
    FROM factors
    WHERE BOROUGH IN ? AND YEAR BETWEEN ? AND ?
),
words AS (
    SELECT reasons AS Word, COUNT(reasons) AS Count
    FROM reasons
    GROUP BY reasons
    
) 
SELECT * 
FROM words
ORDER BY Count DESC
 """


def line_chart(con, borough, year_range):
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
        template="flatly",
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


def word_cloud_plot(worddf):
    word_dict = dict(zip(worddf["Word"], worddf["Count"]))
    wordcloud = WordCloud(
        width=1200,
        height=600,
        background_color=None,
        mode="RGBA",
        colormap="Set1",
        # colormap="YlOrRd",
    ).generate_from_frequencies(word_dict)
    return wordcloud


def word_cloud_func(con, borough, year_range):
    start_year, end_year = year_range

    if not borough:
        borough = ["QUEENS", "BROOKLYN", "MANHATTAN", "BRONX", "STATEN ISLAND"]

    params = (borough, start_year, end_year)

    worddf = con.execute(word_query, parameters=params).df()
    wordcloud = word_cloud_plot(worddf)
    buffer = BytesIO()
    wordcloud.to_image().save(buffer, format="PNG")
    img_base64 = base64.b64encode(buffer.getvalue()).decode()

    return f"data:image/png;base64,{img_base64}"


def row(con, borough, year_range):
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
                                        figure=line_chart(con, borough, year_range),
                                        config={
                                            "displayModeBar": False,
                                            "staticPlot": True,
                                        },
                                    )
                                ],
                                className="border-0",
                            ),
                            dbc.CardFooter(
                                "Line chart showing the number of crashes by borough over time",
                                className="fw-bold border-0",
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
                                "Contributing Factors Analysis",
                                className="fw-bold border-0",
                            ),
                            dbc.CardImg(
                                src=word_cloud_func(con, borough, year_range),
                                className="border-0",
                            ),
                            dbc.CardFooter(
                                "Analysis of the most common contributing factors in vehicle crashes",
                                className="fw-bold border-0",
                            ),
                        ],
                        className="border-0 shadow-lg",
                    )
                ],
                className="align-content-center",
                xs=12,
                md=6,
            ),
        ],
        className="mt-3 gy-3",
        # justify="around",
    )
