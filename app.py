import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, html
from header import header, filter
from kpi import kpi
import duckdb
from row1 import row
from row2 import row2
from row3 import row3
from dash_bootstrap_templates import ThemeSwitchAIO

external_scripts = [
    {'src': 'https://cdn.tailwindcss.com'}
]


con = duckdb.connect("crashes.duckdb", read_only=True)

app = Dash(
    external_stylesheets=[dbc.themes.DARKLY],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
    external_scripts=external_scripts,
)

app.title = "NYC Vehicle Collisions Analysis"


app.layout = (
    dbc.Container(
        children=[header(), filter(), html.Div(id="content")],
        fluid=True,
    ),
)


@app.callback(
    Output("content", "children"),
    [
        Input("borough-checklist", "value"),
        Input("year-range", "value"),
        Input(ThemeSwitchAIO.ids.switch("theme"), "value"),
    ],
)
def update_app(borough, year_range, toggle):
    template = "flatly" if toggle else "darkly"
    return [
        kpi(borough, year_range, template, con),
        row(borough, year_range, template, con),
        row2(borough, year_range, template, con),
        row3(borough, year_range, template, con),
    ]


if __name__ == "__main__":
    app.run(debug=True)
