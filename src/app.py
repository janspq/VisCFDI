import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, html, Input, Output, State
from pages import  inicio, analisis_clientes, analisis_proveedores, red_clientes, red_proveedores
import dash_auth
from dash_bootstrap_templates import load_figure_template
from callbacks import callbacks
import datetime as datetime

# Connect the navbar to the index
from components import components

# Keep this out of source code repository - save in a file or a database
VALID_USERNAME_PASSWORD_PAIRS = {
    'viscfdi': 'msicu2023'
}

load_figure_template("bootstrap")

# Define the navbar
nav = components.Navbar()

app = dash.Dash(__name__, 
                title = 'VisCFDI',
                external_stylesheets=[dbc.themes.BOOTSTRAP], 
                meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1.0"}],
                suppress_callback_exceptions=True)
server = app.server

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)                

app.layout = dbc.Container([
   
    dbc.Row(
        [
            dbc.Col(
                [
                    nav
                ], xs=12)  
        ]
    ),
    dbc.Row(
        [
        dbc.Col(dcc.Location(id='url', refresh=True))   
        ]
    ),
    dbc.Row([
        dbc.Col([
            html.H3("Herramienta para visualización y análisis de datos de CFDI", style={'textAlign': 'center'})
        ], xs = 12)
    ]),   
    html.Hr(),   
       
    dbc.Row([            
        dbc.Col([
            dcc.Upload(
                        id='upload-data',                    
                        className='control-upload',
                        children=html.Div([
                            'Arrastrar y soltar ó ',
                            html.A('Seleccione archivo',
                                  style={'color': 'blue',
                                      'text-decoration-line': 'underline'}),
                                      '(.csv)'
                        ]),
                        style={                            
                            'width': '100%',
                            'height': '60px',
                            'lineHeight': '50px',
                            'borderWidth': '3px',
                            'borderStyle': 'dashed',
                            'borderRadius': '5px',
                            'textAlign': 'center', 
                            'background-color': 'white'                          
                        },
            ),
            html.Div(id="alerta-inicio", style ={'textAlign': 'center'}) 
        ], xs=12, md=5),            

        dbc.Col([
            html.H6("Rango de fechas:"),
            dcc.DatePickerRange(
                id="picker-range",
                display_format='DD/MM/YYYY',
                minimum_nights=0, 
                start_date_placeholder_text='Fecha inicio',
                end_date_placeholder_text='Fecha final',
                style = {'font-size': '12px','display': 'inline-block', 'border-radius' : '2px', 'border' : '1px solid #ccc', 'color': '#333', 'border-spacing' : '0', 'border-collapse' :'separate'},
                className='date_picker_style'                        
            )
        ], xs=6, md={"size": 3, "offset": 1}),  

        dbc.Col([
            html.Div(id='info-toast'),
            html.Div(id='info-toast2'),
            html.H6("Empresa a analizar:"),
            dcc.Dropdown(
                id='dropdown_empresa_base',
                clearable=False, 
                placeholder='Seleccionar empresa',                                                  
                className="dropdown"                                                                         
            ),
            html.Div(id="alerta-dropdown", style ={'textAlign': 'center'})                            
        ], xs=6, md=2)
             
    ]),
    
    html.Hr(),    
        
    dbc.Row(
        [            
           html.Div(id='page-content', children=[])
        ]
    )
], 
fluid=True,
className="dbc"
)

# Create the callback to handle mutlipage inputs
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/inicio':
        return inicio.layout 
    if pathname == '/analisis_clientes':
        return analisis_clientes.layout
    if pathname == '/red_clientes':
        return red_clientes.layout
    if pathname == '/analisis_proveedores':
        return analisis_proveedores.layout
    if pathname == '/red_proveedores':
        return red_proveedores.layout

    else: # if redirected to unknown link
        return inicio.layout #"404 Page Error! Please choose a link"



# Run the app on localhost:8050
if __name__ == '__main__':
    app.run_server(debug=False)

