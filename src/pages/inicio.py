# Import necessary libraries 
import dash_bootstrap_components as dbc
from dash import html, dcc, html, dash_table
import dash_loading_spinners as dls


# Define the page layout
layout = dls.Pulse([    
    dbc.Row([
        dbc.Col(html.H3("CFDI emitidos o recibidos",
                        className='text-center')
        , width = 12)
    ]),
    html.Br(),

    dbc.Row([
        html.Div(id="summary")
    ]),
    
    dbc.Row([
        dbc.Col([
            html.H6("Relación con empresa analizada:"),
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

        ]),
        dbc.Col([
                    html.H6("Nombre:", style={'textAlign': 'center'}),
                    dcc.Dropdown(
                            id='dropdown_cliente_proveedor',                                                          
                            className="dropdown"                                             
                        )
                ], width = 2) 
    ]),
    html.Br(),
     
    dbc.Row([
       dbc.Col([
    dbc.Label("Facturas vigentes:", style={"font-weight": "bold"}),
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

    html.Hr(),
     
    dbc.Row([
       dbc.Col([
        dbc.Label("Facturas canceladas:", style={"font-weight": "bold"}),
        dash_table.DataTable(
            id='table_cancelada',           
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
            page_size=5,                # number of rows visible per page
         
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
    ])            
], 
color="#0275d8",
speed_multiplier=1,
margin =4,
width=60,
fullscreen=True, 
fullscreen_style={'opacity': '0.7'},
)

    
         