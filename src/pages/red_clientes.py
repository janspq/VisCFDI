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
            html.Label('Provedores', style={'textAlign': 'center', 'color':'#87C1FF'}), 
            html.Label('--->', style={'textAlign': 'center'}),
            html.Label('Clientes', style={'textAlign': 'center', 'color':'lightgreen'}),
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
            ], className="twelve columns", style={'padding':'.3rem', 'marginTop':'1rem', 'marginLeft':'1rem', 'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px', 'backgroundColor': 'white' })    
            ], xs=12, md=10),             
    ])
], 
color="#3B71CA",
fullscreen=True
)
