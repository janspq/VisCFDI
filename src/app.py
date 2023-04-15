import dash
from dash import html, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import dash_auth
import datetime as datetime
from dash_bootstrap_templates import load_figure_template
from pages import  inicio, analisis_clientes, analisis_proveedores, red_clientes, red_proveedores, no_data

#callbacks
from callbacks.callbacks import parse_data

# Connect the navbar to the index
from components.components import navbar

# Keep this out of source code repository - save in a file or a database
VALID_USERNAME_PASSWORD_PAIRS = {
    'viscfdi': 'msicu2023'
}

load_figure_template("bootstrap")

app = dash.Dash(__name__, 
                title = 'VisCFDI',
                external_stylesheets=[dbc.themes.BOOTSTRAP], 
                external_scripts=["https://cdn.plot.ly/plotly-locale-es-latest.js"],
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
                    navbar
                ], xs=12)  
        ]
    ),
    html.Div([
        html.H3('Herramienta para visualización y análisis de datos fiscales')
    ], style={'textAlign': 'center'}),
    
    html.Div([
        ################### Filter box ###################### 
        html.Div([            
            html.Div([
            dcc.Upload(
                        id='upload-data',
                        children=html.Div([
                            'Arrastrar y soltar ó ',
                            html.A('Seleccionar',
                                  style={'color': 'blue',
                                      'text-decoration-line': 'underline'}),
                                      '(.csv)'
                        ], style ={"background-color":'white'}),
                        style={                 
                            'width': '100%',
                            'height': '60px',
                            'border-color':'#555555',
                            'lineHeight': '50px',
                            'borderWidth': '3px',
                            'borderStyle': 'dashed',
                            'borderRadius': '5px',
                            'textAlign': 'center', 
                            'background-color': 'white',
                            'boxShadow': '0.1em 0.1em 0.3em #9FA6B2'                          
                        },
            ),
            html.Div(id="alerta-inicio", style ={'textAlign': 'center'}),
            ], className="four columns", style ={'textAlign': 'center', "background-color": '#DBDBDB'}),
            html.Div([
            html.Label('Rango de fechas (Día-Mes-Año):', style = {"margin-left":'5rem', 'fontWeight': 'bold',}),
            dcc.DatePickerRange(
                id="picker-range",
                start_date_placeholder_text='Fecha inicio',
                end_date_placeholder_text='Fecha final',
                display_format='DD/MM/YYYY',
                month_format='DD/MM/YYYY',
                show_outside_days=True,
                minimum_nights=0,  
                style = {'boxShadow': '0.1em 0.1em 0.3em #9FA6B2','font-size': '12px','border-radius' : '2px', 'border' : '1px solid #ccc', 'color': '#333', 'border-spacing' : '0', 'border-collapse' :'separate', "margin-left":'5rem'},
                className='date_picker_style'
            ),
            ], className="four columns", style={'textAlign': 'center', "background-color": '#DBDBDB'}),
            html.Div([
            html.Label('Empresa a analizar:', style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='dropdown_empresa_base',
                clearable=False, 
                placeholder='Seleccionar empresa',
                style={'boxShadow': '0.1em 0.1em 0.3em #9FA6B2'}
                                                                           
            ),
            html.Div(id="alerta-dropdown", style ={'textAlign': 'center'}),
            ], className="three columns", style ={'textAlign': 'center', "background-color": '#DBDBDB'})

        ], className="twelve columns",
        style={"background-color": '#DBDBDB','padding':'2rem', 'margin':'1rem', 'boxShadow': '0 0  0 1px rgb(255,255,255)', 'border-radius': '10px', 'marginTop': '1rem'} ),

        ######################################### 
        # Number statistics & number of accidents each day

        html.Div(id='page-content', className="twelve columns",
                style={"background-color": '#DBDBDB','padding':'2rem', 'margin':'1rem', 'boxShadow': '0 0  0 1px rgb(255,255,255)', 'border-radius': '10px', 'marginTop': '1rem'}
                ),

    ]),
    
    html.Div(id='info-toast'),
    html.Div(id='info-toast2'),    
    dcc.Location(id='url', refresh=True)
    
],
fluid=True,
className="dbc",
style={'padding': '2rem',  "background-color": '#f2f2f2'})


# Create the callback to handle mutlipage inputs
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname'),
               Input('upload-data', 'contents'),
               Input('upload-data', 'filename'),
               Input('dropdown_empresa_base', 'value')])
def display_page(pathname,contents, filename, value):
    if value:
        df = parse_data(contents, filename) 
        if df.empty == False:
           if pathname == '/':
               return inicio.layout 
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
               return "¡Error 404! Por favor elige un enlace"
        else:
            return no_data.layout
    else:
        return no_data.layout
 
if __name__ == '__main__':
    app.run_server(debug=False)




