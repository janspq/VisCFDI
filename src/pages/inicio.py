# Import necessary libraries 
import dash_bootstrap_components as dbc
from dash import html, dcc, html, dash_table
import dash_loading_spinners as dls


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
        html.Label("Tabla interactiva asociada al resumen general", style={'textAlign': 'Left','fontWeight': 'bold'}),         
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

