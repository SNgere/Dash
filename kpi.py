from dash import html

kpi_query = """
    SELECT 
        COUNT(*) AS total_collisions, 
        SUM(PERSONS_KILLED) AS persons_killed, 
        SUM(PERSONS_INJURED) AS persons_injured
    FROM crashes
    WHERE BOROUGH IN ? AND YEAR BETWEEN ? AND ?                       
"""


def kpi_card(graphic, label, value, color):
    return html.Div(
        [
            html.I(className=f"fa {graphic} fa-1x text-[#ff0000]"),
            html.Small(label, className="text-[.9em] font-bold"),
            html.H2(
                f"{value:,}",
                className=f"text-{color}-700 font-extrabold text-md md:text-lg lg:text-xl",
            ),
        ],
        className="border rounded-xl shadow-lg p-3 w-[30vw] text-center flex flex-col justify-center",
    )


def kpi(borough, year_range, template, con):
    start_year, end_year = year_range

    if not borough:
        borough = ["QUEENS", "BROOKLYN", "MANHATTAN", "BRONX", "STATEN ISLAND"]

    params = (borough, start_year, end_year)

    total_crashes, persons_killed, persons_injured = map(
        int, con.execute(kpi_query, parameters=params).fetchone()
    )

    return html.Section(
        [
            html.Div(
                [
                    kpi_card("fa-car-burst", "Total Crashes", total_crashes, "white"),
                    kpi_card(
                        "fa-user-injured", "Total Injured", persons_injured, "white"
                    ),
                    kpi_card(
                        "fa-skull-crossbones", "Total Killed", persons_killed, "white"
                    ),
                ],
                className="flex justify-center gap-3 text-center",
            )
        ],
        className="mx-auto max-w-3xl mt-3",
    )
