# Import necessary libraries 
import dash_bootstrap_components as dbc
from dash import html, dcc, html, dash_table
import dash_loading_spinners as dls


ayuda = html.Div(
    [
        dbc.Button("?", id="open-tabla", n_clicks=0, outline=True, size="lg"),
       
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Filtros de la tabla")),
                dbc.ModalBody([html.P('Una nota rápida sobre el filtrado. Hemos definido nuestra propia sintaxis para realizar operaciones de filtrado:'),
                               html.P('Los filtros se realizan con operadores = < > >='), 
                               html.P('Escriba en la casilla en blanco y presione ENTER para ejecutar un filtrado'),
                               html.P('Pueden concurrir varios filtros a la vez'),
                               html.Br(), 
                               html.P('La filas pueden ser eliminadas solo de la representación visual, no afecta los datos si se ejecuta nuevamente otro filtro principal en la aplicación '), 
                               html.Br(),                               
                               html.P('Ejemplo, filtrar valores iguales a 4536.17 en la columna Total Facturado:'),  
                               html.P(' escriba =4536.17 en la casilla bajo el nombre de columna  y presione ENTER '),
                               html.Br(), 
                               html.P('Para eliminar filtros deje en blanco en la casilla bajo el nombre de columna  y presione ENTER '),
                               
                                               
                              ]

                              ),
                              
                dbc.ModalFooter(
                    dbc.Button(
                        "Close",
                        id="close-tabla",
                        size="xl",
                        n_clicks=0,
                    )
                ),
            ],
            id="modal-tabla",
            scrollable=True,
            is_open=False,
            size="xl",
            class_name="modal-style"
        ),
    ]
)

# Define the page layout
layout = dls.Fade([  
    dbc.Row(
        dbc.Col(html.H4("Resumen general y tabla de datos interactiva ",
                        className='text-center'),
                        width = 12)
    ),  

    dbc.Row([
        html.Div(id='summary')     
    ]),
    html.Br(),
    
    dbc.Row([
       
       html.Div([ 
        dbc.Row([
           dbc.Col([
                html.Label("Tabla interactiva asociada al resumen general", style={'textAlign': 'Left','fontWeight': 'bold'}),
            ], xs=5, md=9),
           dbc.Col([
                    dcc.Dropdown(
                            id='dropdown_facturas',
                            options={
                                     'Facturas vigentes': 'Facturas vigentes',
                                     'Facturas canceladas': 'Facturas canceladas',
                                     'Vigentes + Canceladas': 'Vigentes + Canceladas',
                                    }, 
                            value = 'Facturas vigentes',  
                            clearable=False,                                                               
                            className="dropdown"                                             
                        )
            ], xs=5, md=2),
            dbc.Col([
                ayuda
            ], xs=2, md=1),
        ]),                 
        dash_table.DataTable(
        id='datatable-interactivity',        
        editable=True,              # allow editing of data inside all cells
        filter_action="native",     # allow filtering of data by user ('native') or not ('none')
        sort_action="native",       # enables data to be sorted per-column by user or not ('none')
        sort_mode="single",         # sort across 'multi' or 'single' columns
        filter_options={"placeholder_text": "Filtro > =< >= ..."},
        column_selectable="multi",  # allow users to select 'multi' or 'single' columns
        # row_selectable="multi",     # allow users to select 'multi' or 'single' rows
        row_deletable=True,         # choose if user can delete a row (True) or not (False)
        selected_columns=[],        # ids of columns that user selects
        selected_rows=[],           # indices of rows that user selects
        page_action="native",       # all data is passed to the table up-front or not ('none')
        page_current=0,             # page number that user is on
        page_size=15,                # number of rows visible per page
        style_cell={                # ensure adequate header width when text is shorter than cell's text
            'minWidth': 95, 'maxWidth': 95, 'width': 95
        },
        style_cell_conditional=[    # align text columns to left. By default they are aligned to right
            {
                'if': {'column_id': c},
                'textAlign': 'left'
            } for c in ['country', 'iso_alpha3']
        ],
        style_data={                # overflow cells' content into multiple lines
            'whiteSpace': 'normal',
            'height': 'auto',
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

        ], className="twelve columns number-stat-box")

    ]),

], 
color="#3B71CA",
fullscreen=True
)

