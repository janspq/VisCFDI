from dash import html
import dash_bootstrap_components as dbc
import visdcc
import dash_loading_spinners as dls

# Define the page layout
layout = dls.Pulse([
    html.Center(html.H3("Red de Clientes")),    
    dbc.Row([   
        dbc.Col([
                html.P('Provedores', style={'textAlign': 'center', 'color':'#54B4D3'}), 
                html.P('--->', style={'textAlign': 'center'}),
                html.P('Clientes', style={'textAlign': 'center', 'color':'orange'}),
                html.Div(id = 'select-node-clientes')
            ], xs=12, md=2), #parrafo de select nodes        
        dbc.Col(
                visdcc.Network(id = 'net-clientes',
                               selection = {'nodes':[], 'edges':[]},
                               style={'background-color': "#222222"}, 
                               options = dict(height= '750px',
                                                width= '100%',
                                                interaction = dict(hover= True),
                                                physics = {'barnesHut': {'gravitationalConstant': -8000,
                                                                          'springConstant': 0.01, 'springLength': 100}},
                                                
                                                                                                 
                                              )
                ), xs=12, md=10),    
            
        ])
], 
color="#0275d8",
speed_multiplier=1,
margin =4,
width=60,
fullscreen=True, 
fullscreen_style={'opacity': '0.7'}
)
