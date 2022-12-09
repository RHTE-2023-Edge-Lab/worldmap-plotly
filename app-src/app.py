import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State

import dash_extendable_graph as deg

import random
import pandas as pd

# Some random coordinates
df = pd.DataFrame([], columns=["dev","lat","lon"])
coord = {
    'paris': '48.862725,2.287592',
    'london': '51.5073219,-0.1276474',
    'berlin': '52.5170365,13.3888599',
    'vienna': "48.2083537,16.3725042",
    'brno': "49.1922443,16.6113382",
    'milan': "45.4641943,9.1896346",
    'barcelonne': '41.3828939,2.1774322'
}

# Number of devices
NB_DEV = 2

# Define app global settings
app = dash.Dash(__name__)
app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

# Define Plotly Figure and Intervals
app.layout = html.Div([
    deg.ExtendableGraph(
        id='extendablegraph_example',
        figure=dict(
            # List of dict of size = NB_DEV
            data=[{'lon': [],
                   'lat': [],
                   'mode':'lines+markers',
                   'type': 'scattermapbox',
                   'marker': {"size": 15},
                   'line': {'width': 5},
                   'name': 'DEVICE' # TODO: make it dynamic
                   }] * NB_DEV,
            # Style of the Figure
            layout={
                "mapbox": {
                    "style": "stamen-terrain", 
                    'zoom': 4, 
                    'center': {'lat': 48.2083537, 'lon': 16.3725042}}, 
                "margin": {"r": 0, "t": 0, "l": 0, "b": 10}, 
                "height": "1000",
                }
        )
    ),
    dcc.Interval(
        id='interval_extendablegraph_update',
        interval=2000,
        n_intervals=0,
        max_intervals=len(coord)-1),
    html.Div(id='output')
])

# Callback to update the current graph
@app.callback(Output('extendablegraph_example', 'extendData'),
              [Input('interval_extendablegraph_update', 'n_intervals')],
              [State('extendablegraph_example', 'figure')])
def update_extendData(n_intervals, existing):
    city = list(coord.items())[n_intervals]
    lat, lon = city[1].split(",")
    df.loc[len(df)] = ["esp1", float(lat), float(lon)]
    if (n_intervals % 2) == 0:
        return [dict(lon=[lon], lat=[lat])], [0]
    return [dict(lon=[lon], lat=[lat])], [1]

# Run server
if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=8080)
