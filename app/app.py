# Bringing in libraries
from dash.dependencies import Output, Input, State
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash import html
import plotly.express as px
from flask import Flask
import flask
import pandas as pd
import dash
from datetime import timedelta
import pickle
import json
import requests
from pytz import timezone
from datetime import date
from dotenv import load_dotenv
import os
from dash.exceptions import PreventUpdate
import numpy as np
from sqlalchemy import create_engine
import geojson
import plotly.graph_objects as go

import warnings
warnings.filterwarnings(action='ignore', category=FutureWarning)

# Initializing Flask server and Dash App
server = Flask(__name__)
app = dash.Dash(server=server, url_base_pathname='/mrv-carbon-emissions/', external_stylesheets=[dbc.themes.FLATLY], prevent_initial_callbacks=True)
app.title = 'mrv-carbon-emissions'

# Other
df = pd.read_csv('2014_world_gdp_with_codes.csv')

fig = go.Figure(data=go.Choropleth(
        locations=df['CODE'],
        z=df['GDP (BILLIONS)'],
        text=df['COUNTRY'],
        colorscale='Blues',
        autocolorscale=False,
        reversescale=True,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_tickprefix='$',
        colorbar_title='GDP<br>Billions US$'))

fig.update_layout(
    title_text='CO2 Total Emissions by Country of Origin',
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'
    )
)

# Main app content
app.layout = dbc.Container([
        dbc.Row(dbc.Col([
                         html.H2("EU CO2 Emissions from Maritime Transport"),
        html.Div(id='airport-specific-charts-1'),
        dcc.Graph(figure=fig),
        html.P("Select Year"),
        dcc.Checklist(
            ['2018', '2019', '2020'], inline=True),
        html.P("Select Ship Types"),
        dcc.Checklist(
            ['One', 'Two', 'Three'], inline=True),
        html.Button('Generate Report', id='submit-val', style={'background-color': '#4681f4', 'color': 'white', 'border':'2px solid #4681f4', 'width': '100%'})
                         ]))])
# Callbacks
@app.callback(dash.dependencies.Output('airport-specific-charts-1', 'children'),
               dash.dependencies.Input('submit-val', 'value'))
def get_destination_options(origin):
    three = origin
    return three

@server.route('/mrv-carbon-emissions', methods=['GET'])
def index():
    return flask.redirect('/mrv-carbon-emissions')

if __name__ == '__main__':
    server.run(debug=True)