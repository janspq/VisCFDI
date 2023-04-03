# Import necessary libraries 
import dash_bootstrap_components as dbc
from dash import html, dcc, html, dash_table
import dash_loading_spinners as dls


# Define the page layout
layout = dls.Pulse([  
    dbc.Row(
        dbc.Col(html.H4("Resumen general y tabla de datos",
                        className='text-center'),
                        width = 12)
    ),  

    dbc.Row([
        html.Div([
           dbc.Row([html.H5("INGRESOS", className='text-center',style={'textAlign': 'center','fontWeight': 'bold'})]),
           dbc.Row([
               html.Div([
               html.H5(id='clientes', style={'textAlign': 'center','fontWeight': 'bold'}),
               html.Label('Clientes', style={'textAlign': 'center','paddingTop': '.3rem'}),
            ], className="four columns number-stat-box", style={'background-color': '#abf7b1'}),
               html.Div([
               html.Div(id='clientesFact'),
               html.Label('Total facturado', style={'textAlign': 'center','paddingTop': '.3rem'}),
            ], className="four columns number-stat-box", style={'background-color': '#abf7b1'}),
               html.Div([
               html.Div(id='clientesSal', style={'fontWeight': 'bold'}),
               html.Label('Saldo insoluto', style={'textAlign': 'center','paddingTop': '.3rem'}),
            ], className="four columns number-stat-box", style={'background-color': '#abf7b1'})
           ]),
        ], className="six columns",
         style={"background-color": '#f2f2f2', 'padding':'2rem', 'margin':'1rem', 'boxShadow': '0.2em 0.2em 1em rgba(0,0,0,0.1)', 'border-radius': '10px', 'marginTop': '1rem'} ),
       
        html.Div([
           dbc.Row([html.H5("EGRESOS", className='text-center',style={'textAlign': 'center','fontWeight': 'bold'})]),
           dbc.Row([
               html.Div([
               html.H5(id='proveedores', style={'textAlign': 'center','fontWeight': 'bold'}),
               html.Label('Proveedores', style={'textAlign': 'center','paddingTop': '.3rem'}),
            ], className="four columns number-stat-box", style={'background-color': 'lightblue'}),
             html.Div([
               html.Div(id='proveedoresFact', style={'fontWeight': 'bold'}),
               html.Label('Total facturado', style={'textAlign': 'center','paddingTop': '.3rem'}),
            ], className="four columns number-stat-box", style={'background-color': 'lightblue'}),
             html.Div([
               html.Div(id='proveedoresSal', style={'fontWeight': 'bold'}),
               html.Label('Saldo insoluto', style={'textAlign': 'center','paddingTop': '.3rem'}),
            ], className="four columns number-stat-box", style={'background-color': 'lightblue'})
           ]),
        ], className="six columns",
         style={"background-color": '#f2f2f2', 'padding':'2rem', 'margin':'1rem', 'boxShadow': '0.2em 0.2em 1em rgba(0,0,0,0.1)', 'border-radius': '10px', 'marginTop': '1rem'} ),
      
    ]),


    dbc.Row([
        dbc.Col([
            html.H6("Clientes o proveedores:"),
            dcc.RadioItems(
                id='tipo_empresa_radioitem',
                options=[ 
                    {'label': '        Clientes', 'value': 'Clientes'},                   
                    {'label': '        Provedores', 'value': 'Proveedores'},                    
                    {'label': '        Todos', 'value': 'Todos'},
                ],
                value='Todos',
                labelStyle={'display': 'block'}                
            )

        ], xs=6, md=3),
        dbc.Col([
                    html.Label("# cliente o proveedor:", style={'textAlign': 'center'}),
                    dcc.Dropdown(
                            id='dropdown_cliente_proveedor',                                                          
                            className="dropdown"                                             
                        )
                ], xs=6, md={"size": 2, "offset": 7}) 
    ]),
    html.Br(),
     
    dbc.Row([
       dbc.Col([
        html.Div([
           dbc.Col([
                    dcc.Dropdown(
                            id='dropdown_facturas',
                            options={
                                     'Facturas vigentes': 'Facturas vigentes',
                                     'Facturas canceladas': 'Facturas canceladas',
                                    }, 
                            value = 'Facturas vigentes',  
                            clearable=False,                                                               
                            className="dropdown"                                             
                        )
                ], xs=6, md=2)
        ]),
        dash_table.DataTable(
            id='table',           
            editable=False,             # allow editing of data inside all cells
            filter_action="native",       # allow filtering of data by user ('native') or not ('none') no incluido el resumen
            sort_action="native",       # enables data to be sorted per-column by user or not ('none')
            filter_options={"placeholder_text": "Filtro >,=<,>=,..."},
            sort_mode="single",         # sort across 'multi' or 'single' columns
            # # column_selectable="multi",  # allow users to select 'multi' or 'single' columns
            # # row_selectable="multi",     # allow users to select 'multi' or 'single' rows
            row_deletable=True,         # choose if user can delete a row (True) or not (False)
            # selected_columns=[],        # ids of columns that user selects
            # selected_rows=[],           # indices of rows that user selects
            page_action="native",       # all data is passed to the table up-front or not ('none')
            page_current=0,             # page number that user is on
            page_size=15,                # number of rows visible per page
         
           style_cell_conditional=[
               {
                    'if': {'column_id': c},
                    'textAlign': 'left'
               } for c in ['Date', 'Region']
            ],
            style_data={
                'color': 'black',
                'backgroundColor': 'white'
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(220, 220, 220)',
                }
            ],
            style_header={
                'backgroundColor': 'rgb(210, 210, 210)',
                'color': 'black',
                'fontWeight': 'bold'
            }               
            ),
        
       ])
    ]),

], 
color="#0275d8",
speed_multiplier=1,
margin =4,
width=60,
fullscreen=False, 
fullscreen_style={'opacity': '0.7'},
)

    
         