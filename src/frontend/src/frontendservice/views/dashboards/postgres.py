# -*- coding: utf-8 -*-
import logging

import dash
from dash import dash_table, dcc, html
from dash.dependencies import Input, Output

import flask
import httpx
import pandas as pd

from opentelemetry import trace

tracer = trace.get_tracer(__name__)
logger = logging.getLogger(__name__)

layout = html.Div([
    html.Div('Fakenames (Table)'), html.Br(),
    dcc.Input(id='input_text'), html.Br(), html.Br(),
    html.Div(id='target')
])

@tracer.start_as_current_span('postgres/dashboard')
def create_dash_app(requests_pathname_prefix: str, args: object) -> dash.Dash:
    """Create a Plotly Dash dashboard."""
    server = flask.Flask(__name__)

    app = dash.Dash(__name__,
                    server=server,
                    requests_pathname_prefix=requests_pathname_prefix,
                    external_stylesheets=["/static/css/styles.css",
                                          "https://fonts.googleapis.com/css?family=Lato"])

    headers = {'Accept': 'application/json',
               'Content-Type': 'application/json'}

    with httpx.Client(trust_env=False) as client:
        r = client.get(url=f'{args.backend_api_url}/v1/fakenames',
                       headers=headers)
        logger.debug(r.text)
        df = pd.DataFrame.from_dict(r.json())

    @app.callback(
        Output('desc', 'children'),
        Input('full-input-boxes', 'value'))
    def refresh_desc(df):
        # ...
        return df

    # Create Layout
    # app.scripts.config.serve_locally = False
    app.layout = html.Div(
        children=[
            dcc.Graph(
                id="histogram-graph",
                figure={
                    "data": [
                        {
                            "x": df["cctype"],
                            "y": df["statefull"],
                            # "text": df["State"],
                            # "customdata": df["CountryFull"],
                            # "name": "Fakenames",
                            "type": "histogram"
                        }
                    ],
                    "layout": {
                        "title": "Identities credit cards",
                        "height": 500,
                        "padding": 150
                    },
                },
            ),
            create_data_table(df)
        ],
        id="dash-container"
    )

    return app


def create_data_table(df):
    """
    Create Dash datatable from Pandas DataFrame.
    """
    table = dash_table.DataTable(
        id="dataset-table",
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("records"),
        sort_action="native",
        sort_mode="native",
        page_size=300,
    )

    return table
