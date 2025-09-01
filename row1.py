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

time_query = """
SELECT 
    (HOUR+1) AS HOUR,
    COUNT(*) AS counts
FROM crashes
WHERE BOROUGH IN ? AND YEAR BETWEEN ? AND ?
GROUP BY HOUR
ORDER BY HOUR
"""

bar_query = """
    SELECT 
        WEEKDAY, 
        COUNT(WEEKDAY) AS counts
    FROM crashes
    WHERE BOROUGH IN ? AND YEAR BETWEEN ? AND ?
    GROUP BY WEEKDAY
    ORDER BY counts ASC;
 """


def bar_chart(borough, year_range, template, con):
    start_year, end_year = year_range

    if not borough:
        borough = ["QUEENS", "BROOKLYN", "MANHATTAN", "BRONX", "STATEN ISLAND"]

    params = (borough, start_year, end_year)

    bardf = con.execute(bar_query, parameters=params).df()

    fig = px.bar(
        bardf,
        x="counts",
        y="WEEKDAY",
        color="counts",
        template=template,
        color_continuous_scale="YlOrRd",
    ).update_layout(
        coloraxis_showscale=False,
        margin=dict(t=10, b=10, l=10, r=10),
        xaxis=dict(title="Number of Collisions"),
        yaxis=dict(title="Day of Week"),
    )

    return fig


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


def time_chart(borough, year_range, template, con):
    start_year, end_year = year_range

    if not borough:
        borough = ["QUEENS", "BROOKLYN", "MANHATTAN", "BRONX", "STATEN ISLAND"]

    params = (borough, start_year, end_year)

    df = con.execute(time_query, parameters=params).df()
    df["theta_deg"] = df["HOUR"] * (360 / 24)
    df["label"] = df["HOUR"].apply(lambda h: f"{int(h):02d}:00")

    fig = px.bar_polar(
        df,
        r="counts",
        theta="theta_deg",
        color="counts",
        template=template,
        # color_continuous_scale=px.colors.sequential.Plasma_r,
        color_continuous_scale="YlOrRd",
        hover_name="label",
        hover_data=["counts"],
    ).update_layout(
        coloraxis_showscale=False,
        margin=dict(t=20, b=20, l=35, r=35),
        polar=dict(
            radialaxis=dict(showticklabels=False, ticks=""),
            angularaxis=dict(
                direction="clockwise",
                rotation=90,
                tickmode="array",
                tickvals=[h * 15 for h in range(0, 24, 1)],
                ticktext=[f"{h:02d}:00" for h in range(0, 24, 1)],
            ),
        ),
        showlegend=False,
    )

    return fig


def word_cloud_plot(worddf):
    word_dict = dict(zip(worddf["Word"], worddf["Count"]))
    wordcloud = WordCloud(
        width=1200,
        height=700,
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


def row(borough, year_range, template, con):
    return dbc.Row(
        children=[
            dbc.Col(
                children=[
                    dbc.Card(
                        children=[
                            dbc.CardHeader(
                                "Crash Frequency by Time of Day",
                                className="fw-bold border-0",
                            ),
                            dbc.CardBody(
                                children=[
                                    dcc.Graph(
                                        figure=time_chart(
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
                md=4,
            ),
            dbc.Col(
                children=[
                    dbc.Card(
                        children=[
                            dbc.CardHeader(
                                "Crash Frequency by Day of Week",
                                className="fw-bold border-0",
                            ),
                            dbc.CardBody(
                                children=[
                                    dcc.Graph(
                                        figure=bar_chart(
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
                md=3,
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
                md=5,
            ),
        ],
        className="mt-1 gy-3",
        justify="around",
    )
