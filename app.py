import dash
from dash import dash_table
from dash import dcc # dash core components
from dash import html

from dash.dependencies import Input, Output # interactivity

import pandas as pd

df = pd.read_csv('https://bit.ly/elements-periodic-table')

app = dash.Dash(__name__)

app.layout = dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in df.columns],
    data=df.to_dict('records'),
)

app.run_server(debug=True, host="0.0.0.0")