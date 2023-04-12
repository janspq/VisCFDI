# Import necessary libraries 
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import dash_loading_spinners as dls



# Define the page layout
layout = dls.Fade([

    dbc.Row(
        dbc.Col(html.H4("Análisis de Clientes",
                        className='text-center'),
                        width = 12)
    ),

    dbc.Row([
        
        dbc.Col([
           
            dcc.Graph(id='line-fig1', figure={}, config={"locale": 'es'}, className='twelve columns number-stat-box', style={'boxShadow': '0.1em 0.1em 0.5em #9FA6B2'})            
        ], xs=12, md=6),
        
        dbc.Col([
          
            dcc.Graph(id='line-fig2', figure={}, config={"locale": 'es'}, className='twelve columns number-stat-box', style={'boxShadow': '0.1em 0.1em 0.5em #9FA6B2'})
            
        ], xs=12, md=6)
    ]),
    html.Br(),

   dbc.Row([

        dbc.Col([
         html.Div([
            dbc.Label('Distribución de facturación por clientes y recurrencia', style={"font-weight": "bold"}),
            dash_table.DataTable(
            id='table_clientes',           
            editable=False,             # allow editing of data inside all cells
            filter_action="native",       # allow filtering of data by user ('native') or not ('none') no incluido el resumen
            sort_action="native",       # enables data to be sorted per-column by user or not ('none')
            filter_options={"placeholder_text": "Filtro >,=<,>=,..."},
            sort_mode="single",         # sort across 'multi' or 'single' columns
            # # column_selectable="multi",  # allow users to select 'multi' or 'single' columns
            # # row_selectable="multi",     # allow users to select 'multi' or 'single' rows
            row_deletable=False,         # choose if user can delete a row (True) or not (False)
            # selected_columns=[],        # ids of columns that user selects
            # selected_rows=[],           # indices of rows that user selects
            page_action="native",       # all data is passed to the table up-front or not ('none')
            page_current=0,             # page number that user is on
            page_size=10,                # number of rows visible per page
         
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
        ], className='twelve columns number-stat-box', style={'boxShadow': '0.1em 0.1em 0.5em #9FA6B2'})       
       ], xs=12, md=6),

        dbc.Col([
            dcc.Graph(id='line-fig4', figure={}, config={"locale": 'es'}, className='twelve columns number-stat-box', style={'boxShadow': '0.1em 0.1em 0.5em #9FA6B2'})

        ], xs=12, md=6)
    ])
], 
color="#3B71CA",
fullscreen=True
)




