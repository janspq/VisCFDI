from dash import html
import dash_bootstrap_components as dbc
import visdcc
import dash_loading_spinners as dls

# Define the page layout
layout = dls.Fade([
    dbc.Row(
        dbc.Col(html.H4("Red de Clientes",
                        className='text-center'),
                        width = 12)
    ),  
    dbc.Row([   
        dbc.Col([
            html.Br(),
            html.Label('Provedores', style={'textAlign': 'center', 'color':'#3d97e9'}), 
            html.Label('--->', style={'textAlign': 'center'}),
            html.Label('Clientes', style={'textAlign': 'center', 'color':'#48bf53'}),
            html.Div(id = 'select-node-clientes')
        ], xs=12, md=2), #parrafo de select nodes        
        dbc.Col([
            html.Div([
                visdcc.Network(
                       id = 'net-clientes',
                               selection = {'nodes':[], 'edges':[]},
                               style={'background-color': "#222222"}, 
                               options = dict(height= '750px',
                                                width= '100%',
                                                physics = {'barnesHut': {'gravitationalConstant': -8000,
                                                                          'springConstant': 0.01, 'springLength': 100}},
                                            )
                )
            ], className="twelve columns", style={'padding':'.3rem', 'marginTop':'1rem', 'marginLeft':'1rem', 'boxShadow': '0.1em 0.1em 0.5em #9FA6B2', 'border-radius': '10px', 'backgroundColor': 'white' })    
            ], xs=12, md=10),             
    ])
], 
color="#3B71CA",
fullscreen=True
)
