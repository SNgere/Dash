import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, html
from header import header, filter
from kpi import kpi
import duckdb
from line_word import row


con = duckdb.connect("crashes.duckdb", read_only=True)

app = Dash(
    external_stylesheets=[dbc.themes.DARKLY],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
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
    ],
)
def update_app(borough, year_range):
    return [kpi(con, borough, year_range), row(con, borough, year_range)]


if __name__ == "__main__":
    app.run(debug=True)
