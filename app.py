import dash_bootstrap_components as dbc
from dash import Dash
from header import header, filter

app = Dash(
    external_stylesheets=[dbc.themes.DARKLY],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)

app.title = "NYC Vehicle Collisions Analysis"


app.layout = (
    dbc.Container(
        children=[header(), filter()],
        fluid=True,
    ),
)


if __name__ == "__main__":
    app.run(debug=True)
