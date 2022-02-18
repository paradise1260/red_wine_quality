from turtle import title
from dash import Dash, html, Input, Output, dcc
import pandas as pd
import altair as alt

data = pd.read_csv("winequality-red.csv")
data.loc[data["quality"] == 3, "quality"] = 4
data.loc[data["quality"] == 8, "quality"] = 7
data.loc[data["quality"] == 9, "quality"] = 7
data["quality"] = data["quality"].map(str)


app = Dash(
    __name__,
    title="Individual Assignment 1",
    external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"],
)
app.layout = html.Div(
    [
        html.H2("Red Wine Quality"),
        html.Iframe(
            id="scatter",
            style={"border-width": "0", "width": "100%", "height": "400px"},
        ),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.P("Select x axis:"),
        dcc.Dropdown(
            id="xcol",
            value="fixed acidity",
            options=[
                {"label": i, "value": i}
                for i in list(data.select_dtypes(include="number").columns)
            ],
        ),
        html.Br(),
        html.P("Select y axis:"),
        dcc.Dropdown(
            id="ycol",
            value="residual sugar",
            options=[
                {"label": i, "value": i}
                for i in list(data.select_dtypes(include="number").columns)
            ],
        ),
    ]
)


@app.callback(
    Output("scatter", "srcDoc"), Input("xcol", "value"), Input("ycol", "value")
)
def plot_altair(xcol, ycol):
    chart = (
        alt.Chart(data)
        .mark_bar()
        .encode(
            alt.X(xcol),
            alt.Y(ycol),
            alt.Color("quality", title="Quality"),
            alt.Tooltip(xcol),
        )
        .interactive()
        .facet("quality", columns=4)
    )
    return chart.to_html()


if __name__ == "__main__":
    app.run_server(debug=True)
