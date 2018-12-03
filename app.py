#!/usr/bin/env python
# coding: utf-8

# In[ ]:


### TWO TOGETHER ###
#by Chanelle Bonnici


import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import csv

#CSV Cleaning
df = pd.read_csv('nama_10_gdp_1_Data.csv') #read csv

#remove non single countries from GEO column
df = df[(df.GEO != 'European Union (current composition)') & (df.GEO != 'European Union (without United Kingdom)') & 
        (df.GEO != 'European Union (15 countries)') & 
        (df.GEO != 'Euro area (EA11-2000, EA12-2006, EA13-2007, EA15-2008, EA16-2010, EA17-2013, EA18-2014, EA19)') &
        (df.GEO != 'Euro area (19 countries)') & (df.GEO != 'Euro area (12 countries)')]

#remove things that arent current prices from UNIT column
df = df[(df.UNIT == 'Current prices, million euro')]

#change column names
df.columns = ['TIME','GEO','UNIT','NA_ITEM','VALUE','FF'] #change column names

#replace : with NaN
df.replace(':', np.nan)


app = dash.Dash(__name__)
server = app.server


#css style
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

#indicators for 1
available_indicators = df['NA_ITEM'].unique()

#indicators for 2
item_indicators = df['NA_ITEM'].unique()
geo_indicators=df["GEO"].unique()

#layout for 1
app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            ),
            dcc.RadioItems(
                id='xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Value added, gross'
            ),
            dcc.RadioItems(
                id='yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='indicator-graphic'),

    dcc.Slider(
        id='year--slider',
        min=df['TIME'].min(),
        max=df['TIME'].max(),
        value=df['TIME'].max(),
        step=None,
        marks={str(year): str(year) for year in df['TIME'].unique()}
    ),


#layout for 2

    html.Div([

        html.Div([
            dcc.Dropdown(
                id='country',
                options=[{'label': i, 'value': i} for i in geo_indicators],
                value='France'
            )],
        style={'width': '48%', 'display': 'inline-block'}),


        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in item_indicators],
                value='Value added, gross'
              )],
            style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),


    dcc.Graph(id='indicator-graphic2'),

])

#callback for 1
@app.callback( #for each thing you want to update, you need another callback function (see more in next example)
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('xaxis-type', 'value'),
     dash.dependencies.Input('yaxis-type', 'value'),
     dash.dependencies.Input('year--slider', 'value')])

#update graph for 1
def update_graph(xaxis_column_name, yaxis_column_name, #graph is being updated every time a change is made
                 xaxis_type, yaxis_type,
                 year_value):
    dff = df[df['TIME'] == year_value]
    
    return {
        'data': [go.Scatter(
            x=dff[dff['NA_ITEM'] == xaxis_column_name]['VALUE'],
            y=dff[dff['NA_ITEM'] == yaxis_column_name]['VALUE'],
            text=dff[dff['NA_ITEM'] == yaxis_column_name]['GEO'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }

#callback for 2
@app.callback(
    dash.dependencies.Output('indicator-graphic2', 'figure'),
    [dash.dependencies.Input('country', 'value'),
     dash.dependencies.Input('yaxis-column', 'value')])

#update graph for 2
def update_graph(country_name, yaxis_column_name):
    datax = df[df['GEO'] == country_name]
    
    return {
        'data': [go.Scatter(
            x=datax[datax['NA_ITEM'] == yaxis_column_name]['TIME'],
            y=datax[datax['NA_ITEM'] == yaxis_column_name]['VALUE'],
            text=datax[datax['NA_ITEM'] == yaxis_column_name]['VALUE'],
            mode='lines'
        )],
        'layout': go.Layout(
            xaxis={
                'title': "YEAR",
                'type': 'linear'},
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear'},
            margin={'l': 30, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }


if __name__ == '__main__':
    app.run_server(debug=False)

