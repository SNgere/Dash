import dash_bootstrap_components as dbc
from dash import dcc, html
import plotly.express as px
from wordcloud import WordCloud
from io import BytesIO
import base64


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


def bar_chart(borough, year_range, template, con):
    start_year, end_year = year_range

    if not borough:
        borough = ["QUEENS", "BROOKLYN", "MANHATTAN", "BRONX", "STATEN ISLAND"]

    params = (borough, start_year, end_year)

    bardf = con.execute(bar_query, parameters=params).df()

    fig = px.bar(
        bardf,
        orientation="h",
        x="counts",
        y="WEEKDAY",
        color="counts",
        template=template,
        color_continuous_scale="YlOrRd",
    ).update_layout(
        coloraxis_showscale=False,
        bargap=0.6,
        margin=dict(t=10, b=10, l=10, r=10),
        xaxis=dict(title="Number of Collisions"),
        yaxis=dict(title="Day of Week"),
    )

    return fig


def word_cloud_plot(worddf):
    word_dict = dict(zip(worddf["Word"], worddf["Count"]))
    wordcloud = WordCloud(
        width=1000,
        height=500,
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
    return html.Section(
        children=[
            html.Div(
                children=[
                    html.Div(
                        children=[
                            dbc.Card(
                                dbc.CardHeader(
                                    "Crash Frequency by Time of Day",
                                    className="border-0 fw-bold mb-2",
                                ),
                                className="border-0",
                            ),
                            html.Div(
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
                        className="shadow-lg rounded-md border-[#848484] p-4",
                    ),
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
                        className="shadow-lg rounded-md border-[#848484] p-4",
                    ),
                ],
                className="grid grid-cols-1 lg:grid-cols-2 gap-5 pt-4",
            ),
            html.Div(
                children=[
                    dbc.Card(
                        dbc.CardHeader(
                            "Top Contributing Factors in NYC Vehicle Collisions",
                            className="border-0 fw-bold mb-2",
                        ),
                        className="border-0",
                    ),
                    html.Div(
                        children=[
                            html.Img(
                                src=word_cloud_func(con, borough, year_range),
                            )
                        ],
                        className="flex justify-center items-center flex-grow",
                    ),
                ],
                className="shadow-lg rounded-md border p-4 mb-4 mx-auto max-w-7xl",
            ),
        ],
        className="container mx-auto px-4 space-y-5",
    )
