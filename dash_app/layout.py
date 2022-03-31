import dash_bootstrap_components as dbc
from dash import dcc, html

import pandas as pd

import json

df1 = pd.read_csv(
    '../datasets/business-demographics-updated.csv')
df2 = pd.read_csv(
    '../datasets/business-survival-rates-updated.csv')

# This json file is sourced from the London Data Store
# https://data.london.gov.uk/dataset/statistical-gis-boundary-files-london?resource=9ba8c833-6370-4b11-abdc-314aa020d5e0

f = open(
    '../datasets/london_boroughs.json')

geoj = json.load(f)


layout = dbc.Container(fluid=True, children=[
        dcc.Location(id='url', refresh=False),
        html.Br(),
        dbc.Row(
            dbc.Col(html.H1("Choropleth Map")
                    , id='title')
        ),

        dbc.Row(
            dbc.Col(
                html.H5("Select the year on the dropdown menu that you want to explore and click on the boroughs to "
                        "learn more about the businesses there!"), className='text-muted')
        ),
        dbc.Row(
            dcc.Dropdown(id='slct_yr',
                         options=[
                             {"label": "2004", "value": 2004},
                             {"label": "2005", "value": 2005},
                             {"label": "2006", "value": 2006},
                             {"label": "2007", "value": 2007},
                             {"label": "2008", "value": 2008},
                             {"label": "2009", "value": 2009},
                             {"label": "2010", "value": 2010},
                             {"label": "2011", "value": 2011},
                             {"label": "2012", "value": 2012},
                             {"label": "2013", "value": 2013},
                             {"label": "2014", "value": 2014},
                             {"label": "2015", "value": 2015},
                             {"label": "2016", "value": 2016},
                             {"label": "2017", "value": 2017},
                             {"label": "2018", "value": 2018},
                             {"label": "2019", "value": 2019},
                         ],
                         multi=False,
                         value=2004,
                         clearable=False,
                         style={"width": "40%", "color": "black"}
                         )
        ),
        html.Em(children=[
            '*Data after 2019 is not available.*'
        ]
        ),
        dbc.Row(children=[
            dbc.Col(children=[
                dcc.Graph(id='surv-graph')
            ], style={'margin': '0'}, xs=12, sm=12, md=10, lg=10, xl=5),
            dbc.Col(children=[
                dcc.Graph(id='map')
            ], style={'margin': '0'}, xs=12, sm=12, md=10, lg=10, xl=7)
        ])
    ])

