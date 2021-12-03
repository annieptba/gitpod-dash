import dash
from dash import dash_table
from dash import dcc # dash core components
from dash import html
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np

df = pd.read_csv('https://bit.ly/elements-periodic-table')

def identity(x): return x

app = dash.Dash(__name__)

server = app.server

option = list(df.columns)

app.layout = html.Div(
    className="main",
    children=[
        html.H2("Periodic Pivot Table"),
        html.P("Select an Index option from the dropdown"),
        dcc.Dropdown(id = 'index',
                    options=[{'label': i, 'value': i} for i in option],
                    value='Period'),
        html.P("Select a Column option from the dropdown"),
        dcc.Dropdown(id = 'column',
                    options=[{'label': i, 'value': i} for i in option],
                    value='Group'),
        html.P("Select a Value option from the dropdown"),
        dcc.Dropdown(id = 'value',
                    options=[{'label': i, 'value': i} for i in option],
                    value='Symbol'),
        html.Button("Show Pivot Table", id="button"),
        html.Div(id = 'pivot_table')
    ]
)

@app.callback(
    Output(component_id='pivot_table', component_property='children'),
    Input(component_id='button', component_property='n_clicks'),
    State(component_id='index', component_property='value'),
    State(component_id='column', component_property='value'),
    State(component_id='value', component_property='value'),
)
def make_pivot_table(n_clicks, index, column, value):

    selection = {x:x for x in option}

    index = selection[index]
    column = selection[column]
    value = selection[value]

    if index==column or index==value or column==value:
        return "Index, Column, and Value Selections Must Be Different From One Another"

    else:
        df_piv = df.pivot_table(index = index,
                                columns = column,
                                values = value,
                                aggfunc = identity)

        df_piv = df_piv.reset_index(drop = False)

        df_piv = df_piv.rename(columns={df_piv.columns[0]: 'row=' + index + '/' + 'col= ' + column})

        pivot_table = [dash_table.DataTable(
                            id = 'output-table',
                            columns = [{"name": str(i), "id": str(i)}
                                    for i
                                    in df_piv.columns],
                            data = df_piv.to_dict('records')
                            )
                        ]

        return pivot_table

if __name__ == '__main__':
    app.run_server(debug=True)
