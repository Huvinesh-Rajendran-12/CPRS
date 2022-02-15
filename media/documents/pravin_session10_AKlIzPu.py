#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 22:47:25 2021

@author: pravinkumar
"""


  
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output, State

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('/Users/pravinkumar/Desktop/Exercise 22/USA_Housing.csv')


def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])


def Address():
    options = []
    address = df['Address']
    for i in address:
        a = {'label':i, 'value':i}
        options.append(a)
    return options

    
app.layout = html.Div(children=[
    html.H4(children='US Housing'),
    html.Label('Address'),
    dcc.Dropdown(id = 'address',
        options = Address(),
    ),
    dcc.Markdown(id = 'price')
])

@app.callback(
    Output(component_id='price', component_property='children'),
    [Input(component_id='address', component_property='value')]
)
    
def update_price(input_value):
    row = df[df['Address'] == input_value]
    price = row['Price']
    return 'Price: {}'.format(float(price))

if __name__ == '__main__':
    app.run_server(debug=True)