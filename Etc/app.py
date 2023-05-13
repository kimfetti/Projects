import dash
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff
from dash.dependencies import Input, Output, State
from dash import dash_table, no_update, dcc, html
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc

import pandas as pd
import numpy as np

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.SKETCHY]
)

app.layout = html.Div(
    [
        html.H1(
            ("Exploring F", html.Sub(1),  "- and F", html.Sub('\u03B2'), "-Scores through Precision and Recall"),  
            style={'margin': '50px', 'fontSize':'60px'}
            ),
        dmc.Space(h=10),
        dmc.Grid(
            children=[
                dmc.Col(
                    children=[
                        html.Div(
                            [
                                dmc.RadioGroup(
                                    [
                                        dmc.Radio(('F',html.Sub(0.25)), value='f025'),
                                        dmc.Radio(('F',html.Sub(0.5)), value='f050'),
                                        dmc.Radio(('F',html.Sub(1)), value='f100'),
                                        dmc.Radio(('F',html.Sub(2)), value='f200'),
                                        dmc.Radio(('F',html.Sub(3)), value='f300'),
                                    ],
                                    value='f100',
                                    size='xl',
                                    offset=10,
                                    id='f-radio'
                                )
                            ],
                            style={"transform": "scale(2)"}
                        )
                    ],
                    span=5,
                    style={'display':'flex','justifyContent':'center'}
                )
            ],
            justify='center',
            align='center'
        ),
        dmc.Space(h=100),
        dmc.Grid(
            children = [
                dmc.Col(
                    children=[
                        html.Div(
                            [
                                dmc.Text(id='precision-text'),
                                dcc.Slider(
                                    id='precision-slider', 
                                    value=0.5, min=0, max=1, step=0.05, 
                                    marks=None,
                                   # tooltip={"placement": "bottom", "always_visible": True}
                                )
                            ],
                            style={"transform": "scale(2)"}
                        ),
                        dmc.Space(h=100),
                        html.Div(
                            [
                                dmc.Text(id='recall-text'),
                                dcc.Slider(
                                    id='recall-slider', 
                                    value=0.5, min=0, max=1, step=0.05, 
                                    marks=None,
                                   # tooltip={"placement": "bottom", "always_visible": True}
                                )
                            ],
                            style={"transform": "scale(2)"}
                        )
                    ],
                    span=2,
                    offset=1
                ),
                dmc.Col(
                    children=[
                        html.P(id="f-text", style={"fontSize": '96px', 'vertical-align': 'middle'}),
                    ],
                    span=4,
                    offset=2
                )
            ],
            justify='center',
            align='center',
        ),
        dmc.Space(h=100),
        dmc.Grid(
            children=[
                dmc.Col(
                    children=[
                        html.H1(id='f-figure-header', style={"font-size": '40px'}),
                        html.Br(),
                        dcc.Graph(id='f-figure', figure={}), 
                    ],
                    span=7,
                    style={'display':'flex','justifyContent':'center'}
                )
            ],
            justify='center',
            align='center'
        )
        
    ]
)

@app.callback(
    Output('precision-text', 'children'),
    Output('recall-text', 'children'),
    Input('precision-slider', 'value'),
    Input('recall-slider', 'value')
)
def make_slider_tooltip(p, r):
    return f"Precision: {p:.2f}", f"Recall: {r:.2f}"


@app.callback(
    Output(component_id='f-text', component_property='children'),
    Input(component_id='precision-slider', component_property='value'),
    Input(component_id='recall-slider', component_property='value'),
    Input(component_id='f-radio', component_property='value')
)
def compute_f1(prec, recall, radio='f100'):
    beta = float(radio[1:])/100
    f_value = ((1 + beta**2) * (prec * recall)) / ((beta**2 * prec) + recall + 1e-8)
    return ("F", html.Sub(beta), f"={f_value:.3f}")


@app.callback(
    Output(component_id='f-figure', component_property='figure'),
    Output(component_id='f-figure-header', component_property='children'),
    Input(component_id='precision-slider', component_property='value'),
    Input(component_id='recall-slider', component_property='value'),
    Input(component_id='f-radio', component_property='value')
)
def plot_f1(slider_prec, slider_rec, radio='f100'):
    def fbeta(p, r, beta=1):
        return ((1 + beta**2) * (p * r)) / ((beta**2 * p) + r + 1e-8)

    beta = float(radio[1:])/100
    
    prec = rec = np.arange(0, 1.05, 0.05)
    P, R = np.meshgrid(prec, rec)
    fvals = np.array(fbeta(np.ravel(P), np.ravel(R), beta))
    F = fvals.reshape(P.shape)

    fig = go.Figure(data=[
            go.Contour(
                z=F, x=prec, y=rec, 
                colorscale='Blues',
                hovertemplate = 
                    '<b>Precision</b>: %{x:.2f}' +
                    '<br>Recall: %{y:.2f}' +
                    '<br>F-Score: %{z:.2f}' +
                    '<extra></extra>',
                )
        ]
    )
    fig.add_trace(
        go.Scatter(
            x=[slider_prec],
            y=[slider_rec],
            marker={
                'color': 'DarkSlateGray',
                'size': 30,
                'line': {
                    'color': 'black',
                    'width': 3
                },
            },
            hoverinfo='skip'
        )
    )

    fig.update_xaxes(range=[0,1])
    fig.update_yaxes(range=[0,1])
    fig.update_layout(
        autosize=False,
        width=850,
        height=650,
        xaxis_title='Precision',
        yaxis_title='Recall',
        font={'size': 18}
    )

    header=("F", html.Sub(beta), " Contour Map")

    return fig, header



if __name__ == '__main__':
    app.run_server(debug=True)
