import dash
import dash_bootstrap_components as dbc
from dash import html, Input, Output, callback, State

import base64
import io
import datetime as datetime

import plotly.express as px
import plotly.graph_objects as go
 
from pyvis.network import Network
import pandas as pd
import numpy as np


# Connect the navbar to the index
from components import components

# Define the navbar
modal = components.Modal()

# Función para pasar a float el ' Total ' y ' Saldo insoluto ' según su estructura.
def to_float_from_str_decimal(string):
    try:
        return float(string.replace(',', '').replace('-', '0'))
    except:
        return string

def to_float_from_tipo_cambio_decimal(string):
    try:
        return float(string.replace('$', '').replace('-', '0'))
    except:
        return string

#Función para cargar el dataframe con el dcc.upload.        
def parse_data(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV or TXT file
            df = pd.read_csv(
            io.StringIO(decoded.decode('utf-8')), 
            delimiter=",",
            skip_blank_lines=True,    
            converters={' Total ': to_float_from_str_decimal,
             ' Saldo insoluto ': to_float_from_str_decimal,
             'Tipo de cambio': to_float_from_tipo_cambio_decimal
             })
            df['Fecha factura'] = [datetime.datetime.strptime(x, '%d/%m/%Y') for x in df['Fecha factura'] ]
            df.sort_values(by=['Fecha factura'], inplace=True)

        # elif 'xls' in filename:
        #     # Assume that the user uploaded an excel file
        #     df = pd.read_excel(io.BytesIO(decoded))
        # elif 'txt' or 'tsv' in filename:
        #     # Assume that the user upl, delimiter = r'\s+'oaded an excel file
        #     df = pd.read_csv(
        #         io.StringIO(decoded.decode('utf-8')), delimiter = r'\s+')
    except Exception as e:
        print(e)
        return html.Div([
            'Archivo no válido!'
        ])
    return df

#Devolución de llamada para el filename------------------------------------
@callback(
    Output("alerta-inicio", "children"),
    [Input('upload-data', 'contents'),
    Input('upload-data', 'filename')],   
)    
def mensaje_inicio(contents, filename):
    if contents:              
        return [           
                dbc.Col([
                    html.P('Cargado: '+ filename, style={'textAlign': 'center'})
                ]),           
        ]    
    else:
        return [
                dbc.Alert(
                        [
                            html.H6('¡Cargue un archivo por favor!')                                                
                        ],
                        color = 'danger'      
                        )
            ]
 
#Devolución de llamada para el filename------------------------------------
@callback(
    Output("alerta-dropdown", "children"),
    [Input('upload-data', 'contents'),
    Input('dropdown_empresa_base', 'value')],   
)    
def mensaje_inicio(contents, value):
    if contents:
        if value:
            return []
        else:
            return [
                dbc.Alert(
                        [
                            html.H6('¡Seleccione empresa!')                                                
                        ],
                        color = 'danger'      
                        ) 
            ]

# Devolución de llamada del date picker range
@callback(
    Output('picker-range', 'min_date_allowed'),
    Output('picker-range', 'max_date_allowed'),
    Output('picker-range', 'initial_visible_month'),
    Output('picker-range', 'start_date'),
    Output('picker-range', 'end_date'),   
    [Input('upload-data', 'contents'),
    Input('upload-data', 'filename')]    
)
def update_datepickerrange(contents, filename):
    if contents:
        df = parse_data(contents, filename) 
        min_date = df['Fecha factura'].min()
        max_date = df['Fecha factura'].max()        
        min_date_allowed=min_date
        max_date_allowed=max_date
        initial_visible_month=max_date
        start_date=min_date
        end_date=max_date

        return min_date_allowed, max_date_allowed, initial_visible_month, start_date, end_date 
    else:
        return dash.no_update


# Devolución de llamada del dropdown_empresa_base
@callback(
    Output('dropdown_empresa_base', 'options'),
    [Input('upload-data', 'contents'),
    Input('upload-data', 'filename')]
)
def update_dropdown_empresa_base(contents, filename):
    if contents:
        df = parse_data(contents, filename)         
        frames = [df['Proveedores'], df['Clientes']]
        result = pd.concat(frames)
        empresa_a_analizar = result.unique()
        
        lst =[{'label': 'Seleccionar todo', 'value': 'Seleccionar todo'}] +  [{'label': i, 'value': i} for i in empresa_a_analizar]
       
        return lst
    else:
        return dash.no_update



# #Devolución de llamada del summary------------------------------------
@callback(
    Output("summary", "children"),
    [Input('table', 'data'),   
    Input('dropdown_empresa_base', 'value')]

)    
def create_summary(data, value):
    if data:
        dff = pd.DataFrame(data)
        
        if value=='Seleccionar todo':
            # dataframe filtrado por fechas de los proveedores  
            dff_proveedores = dff
            # dataframe filtrado por fechas de los clientes   
            dff_clientes = dff      
        else:

            # dataframe filtrado por fechas de los proveedores  
            dff_proveedores = dff.loc[dff['Clientes']==value] 
            # dataframe filtrado por fechas de los clientes   
            dff_clientes = dff.loc[dff['Proveedores']==value] 
          
        n_clientes = len(pd.unique(dff_clientes['Clientes']))
        facturado = dff_clientes[' Total '].sum()
        facturado = float("{:.2f}".format(facturado))        
        por_cobrar = dff_clientes[' Saldo insoluto '].sum()
        por_cobrar = float("{:.2f}".format(por_cobrar))


        n_proveedores = len(pd.unique(dff_proveedores['Proveedores'])) 
        pagado = dff_proveedores[' Total '].sum()
        pagado = float("{:.2f}".format(pagado))         
        por_pagar = dff_proveedores[' Saldo insoluto '].sum()
        por_pagar = float("{:.2f}".format(por_pagar))
 
        children = [
            dbc.Row([
                dbc.Col([
                    dbc.Alert(
                        [
                          
                            html.H4(n_clientes, style={'textAlign': 'center'}),
                            html.H6("Clientes", style={'textAlign': 'center'})                                                        
                        ],
                        color="primary",
                    ),
                ]),
                dbc.Col([
                    dbc.Alert(
                        [
                            
                            html.H4('$'+ f"{facturado:,}", style={'textAlign': 'center'}),
                            html.H6("Total", style={'textAlign': 'center'})
                        ],
                        color="primary",
                    ),
                ]),
                dbc.Col([
                    dbc.Alert(
                        [
                            html.H4('$'+ f"{por_cobrar:,}", style={'textAlign': 'center'}),
                            html.H6("Saldo insoluto", style={'textAlign': 'center'})
                           
                        ],
                        color="primary",
                    ),
                ]),
       
                dbc.Col([
                    dbc.Alert(
                        [
                            html.H4(n_proveedores, style={'textAlign': 'center'}),
                            html.H6("Proveedores", style={'textAlign': 'center'})                    
                        ],
                        color="info",
                    ),
                ]),
                dbc.Col([
                    dbc.Alert(
                        [
                            html.H4('$'+ f"{pagado:,}", style={'textAlign': 'center'}),
                            html.H6("Total", style={'textAlign': 'center'})
                           
                        ],
                        color="info",
                    ),
                ]),
                dbc.Col([
                    dbc.Alert(
                        [
                            html.H4('$'+ f"{por_pagar:,}", style={'textAlign': 'center'}),
                            html.H6("Saldo insoluto", style={'textAlign': 'center'})
                           
                        ],
                        color="info",
                    ),
                ]),
            ])
        ] 
        return children   
    else:
        return dash.no_update


# Impresión de la tabla aplicando radioitem y dropdowns
@callback(
    Output('table', 'data'),
    Output('table', 'columns'),
    Output('table_cancelada', 'data'),
    Output('table_cancelada', 'columns'),
    [Input('upload-data', 'contents'),
    Input('upload-data', 'filename'),
    Input('picker-range', 'start_date'),
    Input('picker-range', 'end_date'),
    Input('dropdown_empresa_base', 'value'),
    Input('tipo_empresa_radioitem', 'value'),
    Input('dropdown_cliente_proveedor', 'value')]
)
def create_table(contents, filename, start_date, end_date, value, item, valuecp):

    if value :

        df = parse_data(contents, filename) 
        mask = (df['Fecha factura'] >= start_date) & (df['Fecha factura'] <= end_date)        
        dff = df.loc[mask]
        dff['Fecha factura'] = dff['Fecha factura'].dt.date

        if value=='Seleccionar todo':
            dft = dff

            if item=='Proveedores':
                if valuecp is None:
                    dftabla=dft
                else:
                    dftabla = dft.loc[dft['Proveedores']==valuecp] 

            elif item=='Clientes': 
                if valuecp is None:
                    dftabla=dft                       
                else:
                    dftabla = dft.loc[dft['Clientes']==valuecp]
            else:
                if valuecp is None:
                    dftabla=dft
                else:
                   dftabla = dft.loc[(dft['Proveedores'] == valuecp) | (dft['Clientes'] == valuecp)]
                   

        else:

            dff=dff.loc[(dff['Proveedores'] == value) | (dff['Clientes'] == value)]

            if item=='Proveedores':
                # dataframe filtrado por fechas de los proveedores
                dft = dff.loc[dff['Clientes']==value]

                if valuecp is None:
                    dftabla=dft
                else:
                    dftabla = dft.loc[dft['Proveedores']==valuecp]

            elif item=='Clientes':
                # dataframe filtrado por fechas de los clientes   
                dft = dff.loc[dff['Proveedores']==value]

                if valuecp is None:
                    dftabla=dft                       
                else:
                    dftabla = dft.loc[dft['Clientes']==valuecp]
            
            else:
                dft=dff
                if valuecp is None:
                    dftabla=dft                       
                else:
                    dftabla = dft.loc[(dft['Proveedores'] == valuecp) | (dft['Clientes'] == valuecp)]
        
        
        
        dftabla_vigente =dftabla.loc[df['Estatus']=='Vigente']
        dftabla_cancelada= dftabla.loc[df['Estatus']=='Cancelada'] 

        data_vigente= dftabla_vigente.to_dict('records')
  
        columns_vigente=[
            {"name": i+'($)', "id": i, "deletable": False, "selectable": True, "hideable": False}
            if i == "Tipo de cambio" or i == " Total " or i == " Saldo insoluto "
            else {"name": i, "id": i, "deletable": False, "selectable": True}
            for i in dftabla_vigente.columns
            ]
        data_cancelada= dftabla_cancelada.to_dict('records')
  
        columns_cancelada=[
            {"name": i+'($)', "id": i, "deletable": False, "selectable": True, "hideable": False}
            if i == "Tipo de cambio" or i == " Total " or i == " Saldo insoluto "
            else {"name": i, "id": i, "deletable": False, "selectable": True}
            for i in dftabla_cancelada.columns
            ]    
        return data_vigente, columns_vigente, data_cancelada, columns_cancelada
    else:
        return dash.no_update
  
#Devolución de llamada del dropdown_cliente_proveedor
@callback(
    Output('dropdown_cliente_proveedor', 'options'),
   [Input('upload-data', 'contents'),
    Input('upload-data', 'filename'),
    Input('picker-range', 'start_date'),
    Input('picker-range', 'end_date'),
    Input('tipo_empresa_radioitem', 'value'),
    Input('dropdown_empresa_base', 'value')]   
)
def update_dropdown_cliente_proveedor(contents, filename, start_date, end_date, item, value):
    if value:

        df = parse_data(contents, filename)
        mask = (df['Fecha factura'] >= start_date) & (df['Fecha factura'] <= end_date)        
        dff = df.loc[mask]

        if value =='Seleccionar todo':
            proveedores = dff['Proveedores'].unique()
            clientes = dff['Clientes'].unique()
            todos = np.append(proveedores, clientes)
            todos = np.unique(todos)

            if item=='Proveedores':
                lst = [{'label': i, 'value': i} for i in proveedores]
                return lst
            
            elif item=='Clientes':
                lst = [{'label': i, 'value': i} for i in clientes]
                return lst
            else:
                lst = [{'label': i, 'value': i} for i in todos]
                return lst 
       

        else:
            # dataframe filtrado por fechas de los proveedores  
            dff_proveedores = dff.loc[dff['Clientes']==value] 
            proveedores = dff_proveedores['Proveedores'].unique()

            # dataframe filtrado por fechas de los clientes         
            dff_clientes = dff.loc[dff['Proveedores']==value]
            clientes = dff_clientes['Clientes'].unique()
        
            # listado de proveedores + clientes
            todos = np.append(proveedores, clientes)
            todos = np.unique(todos)

            if item=='Proveedores':
                lst = [{'label': i, 'value': i} for i in proveedores]
                return lst
            
            elif item=='Clientes':
                lst = [{'label': i, 'value': i} for i in clientes]
                return lst
            else:
                lst = [{'label': i, 'value': i} for i in todos]
                return lst 
        
         
    
    else:
        return dash.no_update 

################# Devolución de llamadas de análisis de clientes ############################################ 
@callback(
    Output('line-fig1', 'figure'),
    Output('line-fig2', 'figure'),
    Output('table_clientes', 'data'),
    Output('table_clientes', 'columns'),
    Output('line-fig4', 'figure'),
    [Input('upload-data', 'contents'),
    Input('upload-data', 'filename'),
    Input('picker-range', 'start_date'),
    Input('picker-range', 'end_date'),
    Input('dropdown_empresa_base', 'value')]

)
def create_graph_clientes(contents, filename, start_date, end_date, value):
    if value:
        df = parse_data(contents, filename)
        df = df.loc[df['Estatus']=='Vigente']         
     
        mask = (df['Fecha factura'] >= start_date) & (df['Fecha factura'] <= end_date)        
        dff = df.loc[mask] 

        if value =='Seleccionar todo':
            dff_clientes=dff.assign(Facturas=1)

            #Agrupar los clientes para la tabla
            new_df = (dff_clientes.groupby(["Clientes"])[" Total ", " Saldo insoluto ",'Facturas'].sum()).reset_index()
            
            #Elegir los 10 mayores por total para graficar
            dff_clientes_max_10 = new_df.nlargest(10, [' Total '])
            
            #Agrupar por fecha para graficas de burbujas y líneas
            new_df2 = (dff_clientes.groupby(["Fecha factura"])[" Total ", " Saldo insoluto ", 'Facturas'].sum()).reset_index()

        else:
            # dataframe filtrado por fechas de los clientes   
            dff_mask_clientes=dff['Proveedores']==value
            dff_clientes = dff[dff_mask_clientes]
            dff_clientes=dff_clientes.assign(Facturas=1)
        
            #Agrupar los clientes para la tabla
            new_df = (dff_clientes.groupby(["Clientes"])[" Total ", " Saldo insoluto ",'Facturas'].sum()).reset_index()
            new_df = round(new_df, 2)
            
            #Elegir los 10 mayores por total para graficar
            dff_clientes_max_10 = new_df.nlargest(10, [' Total '])
        
            #Agrupar por fecha para graficas de burbujas y líneas
            new_df2 = (dff_clientes.groupby(["Fecha factura"])[" Total ", " Saldo insoluto ", 'Facturas'].sum()).reset_index() 
    
        #Top 10 mayores clientes     
        fig1 = px.bar( dff_clientes_max_10, x="Clientes", y=" Total ",
                       title=f"<b>Top 10 mayores clientes</b>",
                       text_auto=True,
                       hover_data=['Facturas'])
        fig1.update_yaxes(tickprefix="$", showgrid=True, tickformat=",")
        fig1.update_layout(margin = dict(t=30, l=30, r=30, b=30, ), title_x=0.5)
       
        # Burbujas-Tendencia de facturación en el período      
        fig2 = px.scatter(new_df2, x="Fecha factura", y=" Total ",
                          title=f"<b>Tendencia de facturación en el período</b>",
                          color='Facturas',
                          size='Facturas')
        fig2.update_yaxes(tickprefix="$", showgrid=True, tickformat=",")
        fig2.update_layout(margin = dict(t=30, l=30, r=30, b=30), title_x=0.5)

        # Tabla de clientes
        data= new_df.to_dict('records')  
           
        columns=[
            {"name": i+'($)', "id": i, "deletable": False, "selectable": True, "hideable": False}
            if i == " Total " or i == " Saldo insoluto "
            else {"name": i, "id": i, "deletable": False, "selectable": True}
            for i in new_df.columns
            ]
        
        #Líneas-Tendencia de cuentas por cobrar
        fig4 = go.Figure(data=[
            go.Line(name='Total', x=new_df2["Fecha factura"], y=new_df2[" Total "]),
            go.Line(name='Saldo insoluto', x=new_df2["Fecha factura"], y=new_df2[" Saldo insoluto "])
        ])
        # Change the bar mode
        fig4.update_layout(barmode='group', title=f"<b>Tendencia de cuentas por cobrar</b>", title_x=0.5)
        fig4.update_yaxes(tickprefix="$", showgrid=True, tickformat=",", title= 'Facturado') 
        fig4.update_xaxes(title='Fecha factura') 
        fig4.update_layout(margin = dict(t=30, l=30, r=30, b=30), title_x=0.5)
 
        return fig1, fig2, data, columns, fig4
    else:
        return dash.no_update  



######################### Devolución de la red de clientes para visdcc ###############################
@callback(
    Output('net-clientes', 'data'),
    [Input('upload-data', 'contents'),
    Input('upload-data', 'filename'),
    Input('picker-range', 'start_date'),
    Input('picker-range', 'end_date'),
    Input('dropdown_empresa_base', 'value')],
   
)
def create_net_clientes(contents, filename, start_date, end_date, value):
    data = []
    if value:
        df = parse_data(contents, filename)
        df = df.loc[df['Estatus']=='Vigente']         
     
        mask = (df['Fecha factura'] >= start_date) & (df['Fecha factura'] <= end_date)        
        dff = df.loc[mask] 

        if value =='Seleccionar todo':            
            dff_clientes=dff.assign(Cant_Facturas=1)
            got_data = dff_clientes.groupby(["Proveedores", "Clientes"])[[" Total ", " Saldo insoluto ", 'Cant_Facturas']].sum().reset_index()
            media = got_data[' Total '].mean()
            got_data=got_data.assign(Valor_nodo=((got_data[' Total ']/media)+5))
                    
            
        
        else:
            # dataframe filtrado por fechas de los clientes 
            dff_clientes = dff.loc[dff['Proveedores']==value]
            dff_clientes=dff_clientes.assign(Cant_Facturas=1)
            got_data = dff_clientes.groupby(["Proveedores", "Clientes"])[[" Total ", " Saldo insoluto ", 'Cant_Facturas']].sum().reset_index()
            media = got_data[' Total '].mean()
            got_data=got_data.assign(Valor_nodo=((got_data[' Total ']/media)+5))     
       
        got_net = Network(directed =True,font_color="white")
  
        got_net.barnes_hut()

        sources = got_data['Proveedores']
        targets = got_data['Clientes']
        weights = got_data[' Total ']
        size = got_data['Valor_nodo']
        

        edge_data = zip(sources, targets, weights, size)

        for e in edge_data:
            src = e[0]
            dst = e[1]
            w = e[2]
            s = e[3]           

            got_net.add_node(src, src, title=src)
            got_net.add_node(dst, dst, title=dst, size=s)           
            got_net.add_edge(src, dst, value=w)
      
        data = {'nodes': got_net.nodes,
                
                'edges': [{'from': edge['from'],
                           'to': edge['to'],
                           'id': str(edge['from']) + " __ " + str(edge['to']),
                           'arrows':'to'                                                
                           }
                          for edge in got_net.edges]
                }
        
       
        return data
    else:
        return dash.no_update  

######################### Devolución de la posición del nodo selecionado red de clientes ###############################
@callback(
    Output('select-node-clientes', 'children'),
    [Input('net-clientes', 'selection'),
    Input('upload-data', 'contents'),
    Input('upload-data', 'filename'),
    Input('picker-range', 'start_date'),
    Input('picker-range', 'end_date'),
    Input('dropdown_empresa_base', 'value')]    
)
def statsfunc(x, contents, filename, start_date, end_date, value): 

    if len(x['nodes']) > 0:
        nodo = x['nodes'][0]
        
        df = parse_data(contents, filename)
        df = df.loc[df['Estatus']=='Vigente']         
     
        mask = (df['Fecha factura'] >= start_date) & (df['Fecha factura'] <= end_date)        
        dff = df.loc[mask] 
         
        if value =='Seleccionar todo':  
            dff_clientes = dff.loc[dff.Proveedores == nodo]          
            dff_clientes=dff_clientes.assign(Cant_Facturas=1)
            dff_clientes = dff_clientes.groupby(["Proveedores", "Clientes"])[[" Total ", " Saldo insoluto ", 'Cant_Facturas']].sum().reset_index()
                
            nclientes = str(dff_clientes['Clientes'].count())
            total = str(dff_clientes[' Total '].sum().round(2))
            saldo_insoluto = str(dff_clientes[' Saldo insoluto '].sum().round(2))
            cant_facturas = str(dff_clientes['Cant_Facturas'].sum())

            if x['nodes'][0] != value:
                return [
                    html.H6('Proveedor: ' + nodo),
                    html.H6('Clientes: ' + nclientes),                 
                    html.H6('Total: ' + '$' + total),
                    html.H6('Saldo insoluto: ' + '$' + saldo_insoluto),
                    html.H6('Cant. Fact: ' + cant_facturas)              
                    ]
            return [ 
                html.H6('Analizada: ' + value)            
                ]
            
        else:
            # dataframe filtrado por fechas de los clientes 
            dff_clientes = dff.loc[dff['Proveedores']==value]
            dff_clientes=dff_clientes.assign(Cant_Facturas=1)
            df_node = dff_clientes.groupby(["Proveedores", "Clientes"])[" Total ", " Saldo insoluto ", 'Cant_Facturas'].sum().reset_index()

            #filtar dataframe por un cliente seleccionado
            df_node = df_node[df_node.Clientes==x['nodes'][0]]
     
            df_node[[' Total ', ' Saldo insoluto ']] = df_node[[' Total ', ' Saldo insoluto ']].apply(
                lambda series: series.apply(lambda value: f"{value:,.2f}"))
            df_node[['Cant_Facturas']] = df_node[['Cant_Facturas']].apply(
                lambda series: series.apply(lambda value: f"{value:,.0f}"))        
        
            total = (df_node[' Total '])
            saldo_insoluto = (df_node[' Saldo insoluto '])
            cant_facturas = (df_node['Cant_Facturas'])
  
            if x['nodes'][0] != value:
                return [
                    html.H6('Cliente: ' + nodo),                
                    html.H6('Total: ' + '$' + total),
                    html.H6('Saldo insoluto: ' + '$' + saldo_insoluto),
                    html.H6('Cant. Fact: ' + cant_facturas)              
                    ]
            return [ 
                html.H6('Analizada: ' + value)            
                ]
  
    else:
        return [
      html.H6('"Seleccionar nodo proveedor para ver detalles"', style={'textAlign': 'center'})
    ]

###################### Devolución de llamadas de análisis de proveedores ###################################
@callback(
    Output('line-fig5', 'figure'),
    Output('line-fig6', 'figure'),
    Output('table_proveedores', 'data'),
    Output('table_proveedores', 'columns'),
    Output('line-fig8', 'figure'),
    [Input('upload-data', 'contents'),
    Input('upload-data', 'filename'),
    Input('picker-range', 'start_date'),
    Input('picker-range', 'end_date'),
    Input('dropdown_empresa_base', 'value')]

)
def create_graph_proveedores(contents, filename, start_date, end_date, value):
    if value:
        df = parse_data(contents, filename)
        df = df.loc[df['Estatus']=='Vigente']         
     
        mask = (df['Fecha factura'] >= start_date) & (df['Fecha factura'] <= end_date)        
        dff = df.loc[mask] 

        if value == 'Seleccionar todo':
            dff_proveedores=dff.assign(Facturas=1)

            #Agrupar los proveedores para la tabla
            new_df = (dff_proveedores.groupby(["Proveedores"])[[" Total ", " Saldo insoluto ",'Facturas']].sum()).reset_index()
            new_df = round(new_df, 2)
           
            #Elegir los 10 mayores por total para graficar
            dff_proveedores_max_10 = new_df.nlargest(10, [' Total '])
            
            #Agrupar por fecha para graficas de burbujas y líneas
            new_df2 = (dff_proveedores.groupby(["Fecha factura"])[[" Total ", " Saldo insoluto ", 'Facturas']].sum()).reset_index()
            
        else:
            
            # dataframe filtrado por fechas de los proveedores   
            dff_mask_proveedores=dff['Clientes']==value
            
            dff_proveedores = dff[dff_mask_proveedores]
            dff_proveedores=dff_proveedores.assign(Facturas=1)
        
            #Agrupar los proveedores para la tabla
            new_df = (dff_proveedores.groupby(["Proveedores"])[[" Total ", " Saldo insoluto ", 'Facturas']].sum()).reset_index()
        
            #Elegir los 10 mayores por total para graficar
            dff_proveedores_max_10 = new_df.nlargest(10, [' Total '])
            
            #Agrupar por fecha para graficas de burbujas y líneas
            new_df2 = (dff_proveedores.groupby(["Fecha factura"])[[" Total ", " Saldo insoluto ", 'Facturas']].sum()).reset_index() 
        
        
        fig5 = px.bar( dff_proveedores_max_10, x="Proveedores", y=" Total ",                       
                       title=f"<b>Top 10 mayores proveedores</b>",                      
                       text_auto=True,
                       hover_data=['Facturas'])
        fig5.update_yaxes(tickprefix="$", showgrid=True, tickformat=",")
        fig5.update_layout(margin = dict(t=30, l=30, r=30, b=30), title_x=0.5)
       
        #Top 10 mayores proveedores----------------------------------------------------
        fig6 = px.scatter(new_df2, x="Fecha factura", y=" Total ",                       
                          title=f"<b>Tendencia de facturación en el período</b>",
                          color='Facturas',
                          size='Facturas')
        fig6.update_yaxes(tickprefix="$", showgrid=True, tickformat=",")
        fig6.update_layout(margin = dict(t=30, l=30, r=30, b=30), title_x=0.5)
  
        data= new_df.to_dict('records')
           
        columns=[
            {"name": i+'($)', "id": i, "deletable": False, "selectable": True, "hideable": False}
            if i == " Total " or i == " Saldo insoluto "
            else {"name": i, "id": i, "deletable": False, "selectable": True}
            for i in new_df.columns
            ]

        fig8 = go.Figure(data=[
            go.Line(name='Total' , x=new_df2["Fecha factura"], y=new_df2[" Total "]),
            go.Line(name='Saldo insoluto', x=new_df2["Fecha factura"], y=new_df2[" Saldo insoluto "])
        ])
        # Change the bar mode
        fig8.update_layout(barmode='group', title=f"<b>Tendencia de cuentas por pagar</b>", title_x=0.5)
        fig8.update_yaxes(tickprefix="$", showgrid=True, tickformat=",", title= 'Facturado') 
        fig8.update_xaxes(title='Fecha factura')
        fig8.update_layout(margin = dict(t=30, l=30, r=30, b=30), title_x=0.5) 

        return fig5, fig6, data, columns, fig8
    else:
        return dash.no_update  

#############################3 Devolución de llamadas para Red de proveedores ###############################
@callback(
    Output('net-proveedores', 'data'),
    [Input('upload-data', 'contents'),
    Input('upload-data', 'filename'),
    Input('picker-range', 'start_date'),
    Input('picker-range', 'end_date'),
    Input('dropdown_empresa_base', 'value')],
   
)
def create_net_proveedores(contents, filename, start_date, end_date, value):
    if value:
        df = parse_data(contents, filename)
        df = df.loc[df['Estatus']=='Vigente']         
     
        mask = (df['Fecha factura'] >= start_date) & (df['Fecha factura'] <= end_date)        
        dff = df.loc[mask] 
         
        if value =='Seleccionar todo':            
            dff_proveedores=dff.assign(Cant_Facturas=1)
            got_data = dff_proveedores.groupby(["Clientes", "Proveedores"])[[" Total ", " Saldo insoluto ", 'Cant_Facturas']].sum().reset_index()
            media = got_data[' Total '].mean()
            got_data=got_data.assign(Valor_nodo=((got_data[' Total ']/media)+5))

        else:
            # dataframe filtrado por fechas de los proveedores 
            dff_proveedores = dff.loc[dff['Clientes']==value]
            dff_proveedores=dff_proveedores.assign(Cant_Facturas=1)
            got_data = dff_proveedores.groupby(["Clientes", "Proveedores"])[[" Total ", " Saldo insoluto ", 'Cant_Facturas']].sum().reset_index()
            media = got_data[' Total '].mean()
            got_data=got_data.assign(Valor_nodo=((got_data[' Total ']/media)+5))
        

        got_net = Network(directed =True, font_color="white")
        got_net.barnes_hut()
       
        sources = got_data['Clientes']
        targets = got_data['Proveedores']
        weights = got_data[' Total ']
        size = got_data['Valor_nodo']

        edge_data = zip(sources, targets, weights, size)

        for e in edge_data:
            src = e[0]
            dst = e[1]
            w = e[2]
            s = e[3]

            got_net.add_node(src, src, title=src)
            got_net.add_node(dst, dst, title=dst, size=s)
            got_net.add_edge(src, dst, value=w)

        
        data = {'nodes': got_net.nodes,
                'edges': [{'id': str(edge['from']) + " __ " + str(edge['to']),
                           'from': edge['from'],
                           'to': edge['to'],
                           'arrows':'from'                           
                           }
                          for edge in got_net.edges]
                }
      
        return data
    else:
        return dash.no_update  

######################### Devolución de la posición del nodo selecionado red de proveedores ###############################
@callback(
    Output('select-node-proveedores', 'children'),
    [Input('net-proveedores', 'selection'),
    Input('upload-data', 'contents'),
    Input('upload-data', 'filename'),
    Input('picker-range', 'start_date'),
    Input('picker-range', 'end_date'),
    Input('dropdown_empresa_base', 'value')]    
)
def statsfunc(x, contents, filename, start_date, end_date, value): 

    if len(x['nodes']) > 0:
        nodo = x['nodes'][0]
        
        df = parse_data(contents, filename)
        df = df.loc[df['Estatus']=='Vigente']         
     
        mask = (df['Fecha factura'] >= start_date) & (df['Fecha factura'] <= end_date)        
        dff = df.loc[mask] 
         
        if value =='Seleccionar todo':  
            dff_proveedores = dff.loc[dff.Clientes == nodo]          
            dff_proveedores=dff_proveedores.assign(Cant_Facturas=1)
            dff_proveedores = dff_proveedores.groupby(["Proveedores", "Clientes"])[[" Total ", " Saldo insoluto ", 'Cant_Facturas']].sum().reset_index()
                
            nproveedores = str(dff_proveedores['Proveedores'].count())
            total = str(dff_proveedores[' Total '].sum().round(2))
            saldo_insoluto = str(dff_proveedores[' Saldo insoluto '].sum().round(2))
            cant_facturas = str(dff_proveedores['Cant_Facturas'].sum())

            if x['nodes'][0] != value:
                return [
                    html.H6('Cliente: ' + nodo),
                    html.H6('Proveedores: ' + nproveedores),                 
                    html.H6('Total: ' + '$' + total),
                    html.H6('Saldo insoluto: ' + '$' + saldo_insoluto),
                    html.H6('Cant. Fact: ' + cant_facturas)              
                    ]
            return [ 
                html.H6('Analizada: ' + value)            
                ]
            
        else:
            # dataframe filtrado por fechas de los proveedores 
            dff_proveedores = dff.loc[dff['Clientes']==value]
            dff_proveedores=dff_proveedores.assign(Cant_Facturas=1)
            df_node = dff_proveedores.groupby(["Proveedores", "Clientes"])[" Total ", " Saldo insoluto ", 'Cant_Facturas'].sum().reset_index()

            #filtar dataframe por un cliente seleccionado
            df_node = df_node[df_node.Proveedores==x['nodes'][0]]
     
            df_node[[' Total ', ' Saldo insoluto ']] = df_node[[' Total ', ' Saldo insoluto ']].apply(
                lambda series: series.apply(lambda value: f"{value:,.2f}"))
            df_node[['Cant_Facturas']] = df_node[['Cant_Facturas']].apply(
                lambda series: series.apply(lambda value: f"{value:,.0f}"))        
        
            total = (df_node[' Total '])
            saldo_insoluto = (df_node[' Saldo insoluto '])
            cant_facturas = (df_node['Cant_Facturas'])
  
            if x['nodes'][0] != value:
                return [
                    html.H6('Proveedor: ' + nodo),                
                    html.H6('Total: ' + '$' + total),
                    html.H6('Saldo insoluto: ' + '$' + saldo_insoluto),
                    html.H6('Cant. Fact: ' + cant_facturas)              
                    ]
            return [ 
                html.H6('Analizada: ' + value)            
                ]
  
    else:
        return [
      html.H6('"Seleccionar nodo proveedor para ver detalles"', style={'textAlign': 'center'})
    ]   

def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open



callback(
    Output("modal-body-scroll", "is_open"),
    [
        Input("open-body-scroll", "n_clicks"),
        Input("close-body-scroll", "n_clicks"),
    ],
    [State("modal-body-scroll", "is_open")],
)(toggle_modal)    