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
    if 'csv' in filename:
        try:      
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
            df = df[['Proveedores', 'Clientes', 'Fecha factura', 'Metodo de pago', 'Moneda', 'Tipo de cambio', ' Total ', 'Estatus', ' Saldo insoluto ', 'Estatus pago', 'Deducible']]
        except Exception as e:
            print(e)
            df = pd.DataFrame()  
            return df      
        return df
    
    df = pd.DataFrame()
    return df


#Devolución de llamada para el filename------------------------------------
@callback(
    Output("alerta-inicio", "children"),
    [Input('upload-data', 'contents'),
    Input('upload-data', 'filename')],   
)    
def mensaje_inicio(contents, filename):
    if contents:
        df = parse_data(contents, filename) 
        if df.empty == False:
           return  html.Label('Cargado: '+ filename, style={'textAlign': 'center','font-style': 'italic'})
                           
        else:
            return [
                dbc.Alert(
                        [
                            html.Label('Cargado: '+ filename, style={'textAlign': 'center', 'font-style': 'italic'})                                                
                        ],
                        color = 'danger'      
                        )
            ] 
    else:
        return [
                dbc.Col([ 
                    dbc.Alert(
                        [
                            html.H6('¡Cargue un archivo por favor!')                                                
                        ],
                        color = 'info'      
                        ) 
                ])
            ]


               
 
#Devolución de llamada para el filename------------------------------------
@callback(
    Output("alerta-dropdown", "children"),
    [Input('upload-data', 'contents'),
     Input('upload-data', 'filename'),
    Input('dropdown_empresa_base', 'value')],   
)    
def mensaje_inicio(contents, filename, value):
    if contents:
        df = parse_data(contents, filename) 
        if df.empty == False:
            if value:
                return []
            else:
                return [
                    dbc.Alert([
                            html.H6('¡Seleccione la empresa a analizar!')                                                
                        ],
                        color = 'info'      
                    ) 
            ]
    return []

# Devolución de llamada del date picker range
@callback(
    Output('picker-range', 'min_date_allowed'),
    Output('picker-range', 'max_date_allowed'),
    Output('picker-range', 'initial_visible_month'),
    Output('picker-range', 'start_date'),
    Output('picker-range', 'end_date'),   
    [Input('upload-data', 'contents'),
    Input('upload-data', 'filename')],
    prevent_initial_call=True
)
def update_datepickerrange(contents, filename):
    if contents:
        df = parse_data(contents, filename)
        if df.empty == False:
            min_date = df['Fecha factura'].min()
            max_date = df['Fecha factura'].max()        
            min_date_allowed=min_date
            max_date_allowed=max_date
            initial_visible_month=max_date
            start_date=min_date
            end_date=max_date
            return min_date_allowed, max_date_allowed, initial_visible_month, start_date, end_date 
        else:
            min_date = datetime.date.today()
        max_date = datetime.date.today()        
        min_date_allowed=min_date
        max_date_allowed=max_date
        initial_visible_month=max_date
        start_date=min_date
        end_date=max_date
        return min_date_allowed, max_date_allowed, initial_visible_month, start_date, end_date
    else:    
        min_date = datetime.date.today()
        max_date = datetime.date.today()        
        min_date_allowed=min_date
        max_date_allowed=max_date
        initial_visible_month=max_date
        start_date=min_date
        end_date=max_date
        return min_date_allowed, max_date_allowed, initial_visible_month, start_date, end_date 
    



# Devolución de llamada del dropdown_empresa_base
@callback(
    Output('dropdown_empresa_base', 'options'),
    Output("info-toast", "children"),
    [Input('upload-data', 'contents'),
    Input('upload-data', 'filename'),
    Input('picker-range', 'start_date'),
    Input('picker-range', 'end_date')],
   
)
def update_dropdown_empresa_base(contents, filename, start_date, end_date):
    if contents:
        df = parse_data(contents, filename) 
        if df.empty == False:
            mask = (df['Fecha factura'] >= start_date) & (df['Fecha factura'] <= end_date)        
            dff = df.loc[mask]
            frames = [dff['Proveedores'], dff['Clientes']]
            result = pd.concat(frames)
            empresa_a_analizar = result.unique()
             
            lst =[{'label': 'Seleccionar todo', 'value': 'Seleccionar todo'}] +  [{'label': i, 'value': i} for i in empresa_a_analizar]
            children = [
                dbc.Toast(
                [html.P("¡Cargado con éxito!", className="mb-0")],
                id="toast1",
                header="Éxito",
                dismissable=True,
                duration=1000,
                icon="success",
                is_open=True,
                style={"position": "fixed", "top": 250, "left": 250, "width": 200},
            ),
            ]
            return lst, children
        else:
            children = [
                dbc.Toast(                
                [html.P('Los datos permitidos son en .CSV, las columnas utilizadas son ["Proveedores", "Clientes", "Fecha factura", "Metodo de pago", "Moneda", "Tipo de cambio", " Total ", "Estatus", " Saldo insoluto ", "Estatus pago", "Deducible"].')],
                id="toast2",
                header="¡Error! El archivo no es válido",                
                dismissable=True,
                icon="danger",
                is_open=True,
                style={"position": "fixed", "top": 250, "left": 300, "width": 200},
            ),
            ]
            lst=[]
            return lst, children
    else:
        children = [
                dbc.Toast(
                     id="toast3",
                     header="En este panel cargue un archivo por favor!",
                     icon="info",
                     dismissable=True,
                     is_open=True,
                     style={"position": "fixed", "top": 250, "left": 450, "width": 400}
                    ),
            ]
        lst=[]
        return lst, children

##### Devolución de llamada del dropdown d-clientes #######
@callback(
    Output('d-clientes', 'options'),
    [Input('upload-data', 'contents'),
    Input('upload-data', 'filename'),
    Input('picker-range', 'start_date'),
    Input('picker-range', 'end_date'),
    Input('dropdown_empresa_base', 'value')],   
)
def dropdown_clientes(contents, filename, start_date, end_date, value):
    if value:
        df = parse_data(contents, filename)

        df = df.loc[df['Estatus']=='Vigente']         
     
        mask = (df['Fecha factura'] >= start_date) & (df['Fecha factura'] <= end_date)        
        dff = df.loc[mask] 

        if value =='Seleccionar todo':
            result = dff['Clientes']            
            cliente_a_analizar = result.unique()
             
            lst =[{'label': 'Todos los clientes', 'value': 'Todos los clientes'}] +  [{'label': i, 'value': i} for i in cliente_a_analizar]
            return lst
        else:
            dff = dff.loc[dff['Proveedores']==value] 
            result = dff['Clientes']            
            cliente_a_analizar = result.unique()
             
            lst =[{'label': 'Todos los clientes', 'value': 'Todos los clientes'}] +  [{'label': i, 'value': i} for i in cliente_a_analizar]
            return lst   
 
##### Devolución de llamada del dropdown d-proveedores #######
@callback(
    Output('d-proveedores', 'options'),
    [Input('upload-data', 'contents'),
    Input('upload-data', 'filename'),
    Input('picker-range', 'start_date'),
    Input('picker-range', 'end_date'),
    Input('dropdown_empresa_base', 'value')],   
)
def dropdown_proveedores(contents, filename, start_date, end_date, value):
    if value:
        df = parse_data(contents, filename)

        df = df.loc[df['Estatus']=='Vigente']         
     
        mask = (df['Fecha factura'] >= start_date) & (df['Fecha factura'] <= end_date)        
        dff = df.loc[mask] 

        if value =='Seleccionar todo':
            result = dff['Proveedores']            
            proveedor_a_analizar = result.unique()
             
            lst =[{'label': 'Todos los proveedores', 'value': 'Todos los proveedores'}] +  [{'label': i, 'value': i} for i in proveedor_a_analizar]
            return lst
        else:
            dff = dff.loc[dff['Clientes']==value] 
            result = dff['Proveedores']            
            proveedor_a_analizar = result.unique()
             
            lst =[{'label': 'Todos los proveedores', 'value': 'Todos los proveedores'}] +  [{'label': i, 'value': i} for i in proveedor_a_analizar]
            return lst  



############## Impresión de la tabla  #########
@callback(
    Output('datatable-interactivity', 'data'),
    Output('datatable-interactivity', 'columns'),
    [Input('upload-data', 'contents'),
    Input('upload-data', 'filename'),
    Input('picker-range', 'start_date'),
    Input('picker-range', 'end_date'),
    Input('dropdown_empresa_base', 'value'),
    Input('dropdown_facturas', 'value')]
)
def create_table(contents, filename, start_date, end_date, value, valuev):
    if value :
        df = parse_data(contents, filename) 
        mask = (df['Fecha factura'] >= start_date) & (df['Fecha factura'] <= end_date)        
        dff = df.loc[mask]
        dff['Fecha factura'] = dff['Fecha factura'].dt.date

        if value=='Seleccionar todo':
            if valuev == 'Facturas vigentes':
                dftabla =dff.loc[dff['Estatus']=='Vigente']
            elif valuev == 'Facturas canceladas':
                dftabla =dff.loc[dff['Estatus']=='Cancelada']       
            else:
                dftabla=dff

            data = dftabla.to_dict('records')
            columns = [
            {"name": i, "id": i, "deletable": False, "selectable":False, "hideable": False}
            if i == "Proveedores"or i == "Clientes" or i == " Total " or i == " Saldo insoluto "
            else {"name": i, "id": i, "deletable": False, "selectable": False}
            for i in dftabla.columns
            ] 
            return data, columns         
    
        else:
            dff=dff.loc[(dff['Proveedores'] == value) | (dff['Clientes'] == value)]
            if valuev == 'Facturas vigentes':
                dftabla =dff.loc[dff['Estatus']=='Vigente']
            elif valuev == 'Facturas canceladas':
                dftabla =dff.loc[dff['Estatus']=='Cancelada']       
            else:
                dftabla=dff
            
            data = dftabla.to_dict('records')
            columns = [
            {"name": i, "id": i, "deletable": False, "selectable":False, "hideable": False}
            if i == "Proveedores"or i == "Clientes" or i == " Total " or i == " Saldo insoluto "
            else {"name": i, "id": i, "deletable": False, "selectable": False}
            for i in dftabla.columns
            ] 
            return data, columns 
        
    else:
        return dash.no_update
    


  
####  Devolución de llamada para el summary ###########
@callback(    
    Output('summary', 'children'),
    [Input('datatable-interactivity', "derived_virtual_data"),
    Input('dropdown_empresa_base', 'value')],
    prevent_initial_callbacks=True
)
def update_bar(all_rows_data, value):
    if all_rows_data:
        dff = pd.DataFrame(all_rows_data)
        dff=dff.assign(Facturas=1)

        if value=='Seleccionar todo':
            proveedorest = len(pd.unique(dff['Proveedores']))
            clientest = len(pd.unique(dff['Clientes']))

            facturadot = dff[' Total '].sum()
            facturadot = float("{:.2f}".format(facturadot)) 
            

            saldot = dff[' Saldo insoluto '].sum()
            saldot = float("{:.2f}".format(saldot))
            

            nfacturas = dff['Facturas'].sum()

            children =[
                html.Div([
                     html.Div([
                            html.Label('Proveedores', style={'fontWeight': 'bold','textAlign': 'center','paddingTop': '.3rem'}),
                            html.H4(proveedorest, style={'textAlign': 'center','fontWeight': 'bold', 'color': 'rgb(0 58 115)'})                            
                        ], className="two columns number-stat-box", style={'boxShadow': '0.1em 0.1em 0.3em rgb(0 58 115)'}),
                         html.Div([
                            html.Label('Clientes', style={'fontWeight': 'bold','textAlign': 'center','paddingTop': '.3rem'}),
                            html.H4(clientest, style={'textAlign': 'center','fontWeight': 'bold', 'color': 'rgb(0 114 178)'})                            
                        ], className="two columns number-stat-box", style={'boxShadow': '0.1em 0.1em 0.3em rgb(0 114 178)'}),
                        
                        html.Div([
                            html.Label('Facturado', style={'fontWeight': 'bold','textAlign': 'center','paddingTop': '.3rem'}),
                            html.H4('$'+ f"{facturadot:,}", style={'textAlign': 'center','fontWeight': 'bold', 'color': 'purple'})                            
                        ], className="three columns number-stat-box", style={'boxShadow': '0.1em 0.1em 0.3em purple'}),
                        html.Div([
                            html.Label('Saldo insoluto', style={'fontWeight': 'bold','textAlign': 'center','paddingTop': '.3rem'}),
                            html.H4('$'+ f"{saldot:,}", style={'textAlign': 'center','fontWeight': 'bold', 'color': 'rgb(213 94 0)'})                            
                        ], className="three columns number-stat-box", style={'boxShadow': '0.1em 0.1em 0.3em rgb(213 94 0)'}),
                         html.Div([
                            html.Label('Facturas', style={'fontWeight': 'bold','textAlign': 'center','paddingTop': '.3rem'}),
                            html.H4(nfacturas, style={'textAlign': 'center','fontWeight': 'bold', 'color': '#A21A24'})                            
                        ], className="two columns number-stat-box", style={'boxShadow': '0.1em 0.1em 0.3em #A21A24'}),                 
                ], className="twelve columns",
                style={"background-color": '#DBDBDB','padding':'2rem', 'margin':'1rem','border-radius': '10px', 'marginTop': '1rem'}),
            ]
            

        else:

            # dataframe filtrado por fechas de los proveedores  
            dff_proveedores = dff.loc[dff['Clientes']==value] 
            # dataframe filtrado por fechas de los clientes   
            dff_clientes = dff.loc[dff['Proveedores']==value]

            n_clientes = len(pd.unique(dff_clientes['Clientes']))
            facturadoc = dff_clientes[' Total '].sum()
            facturadoc = float("{:.2f}".format(facturadoc)) 
            

            por_cobrar = dff_clientes[' Saldo insoluto '].sum()
            por_cobrar = float("{:.2f}".format(por_cobrar))
            
            n_proveedores = len(pd.unique(dff_proveedores['Proveedores'])) 
            facturadop = dff_proveedores[' Total '].sum()
            facturadop = float("{:.2f}".format(facturadop)) 
            

            por_pagar = dff_proveedores[' Saldo insoluto '].sum()
            por_pagar = float("{:.2f}".format(por_pagar))
           
           
            children =[
                html.Div([
                    dbc.Row([html.H5("INGRESOS", className='text-center',style={'color': '#004d25','textAlign': 'center','fontWeight': 'bold'})]),
                    dbc.Row([                        
                        html.Div([
                            html.H5(n_clientes, className='text-center', style={'color': '#004d25','textAlign': 'center','fontWeight': 'bold'}),
                            html.Label('Clientes', style={'fontWeight': 'bold','textAlign': 'center','paddingTop': '.3rem'}),
                        ], className="four columns number-stat-box", style={'boxShadow': '0.1em 0.1em 0.5em #06c258'}),
                        html.Div([
                            html.H5('$'+ f"{facturadoc:,}",className='text-center', style={'color': '#004d25','textAlign': 'center','fontWeight': 'bold'}),
                            html.Label('Total facturado', style={'fontWeight': 'bold','textAlign': 'center','paddingTop': '.3rem'}),
                        ], className="four columns number-stat-box", style={'boxShadow': '0.1em 0.1em 0.5em #06c258'}),
                        html.Div([
                            html.H5('$'+ f"{por_cobrar:,}", className='text-center', style={'color': '#004d25', 'textAlign': 'center','fontWeight': 'bold'}),
                            html.Label('Saldo insoluto', style={'fontWeight': 'bold','textAlign': 'center','paddingTop': '.3rem'}),
                        ], className="four columns number-stat-box", style={'boxShadow': '0.1em 0.1em 0.5em #06c258'})
                    ]),
                ], className='six columns', style={"background-color": '#DBDBDB'}),
       
                html.Div([
                    dbc.Row([html.H5("EGRESOS", className='text-center',style={'color': '#004999','textAlign': 'center','fontWeight': 'bold'})]),
                    dbc.Row([
                        html.Div([
                           html.H5(n_proveedores, style={'textAlign': 'center','fontWeight': 'bold','color': '#004999'}),
                           html.Label('Proveedores', style={'fontWeight': 'bold','textAlign': 'center','paddingTop': '.3rem'}),
                        ], className="four columns number-stat-box", style={'boxShadow': '0.1em 0.1em 0.5em #004999'}),
                        html.Div([
                            html.H5('$'+ f"{facturadop:,}", style={'textAlign': 'center','fontWeight': 'bold', 'color': '#004999'}),
                            html.Label('Total facturado', style={'fontWeight': 'bold','textAlign': 'center','paddingTop': '.3rem'}),
                        ], className="four columns number-stat-box", style={'boxShadow': '0.1em 0.1em 0.5em #004999'}),
                        html.Div([
                            html.H5('$'+ f"{por_pagar:,}", style={'textAlign': 'center','fontWeight': 'bold', 'color': '#004999'}),
                            html.Label('Saldo insoluto', style={'fontWeight': 'bold','textAlign': 'center','paddingTop': '.3rem'}),
                        ], className="four columns number-stat-box",style={'boxShadow': '0.1em 0.1em 0.5em #004999'})
                    ]),
                ], className='six columns', style={"background-color": '#DBDBDB'}),
            ]

        return children
    else:
        dash.no_update

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
    Input('dropdown_empresa_base', 'value'),
    Input('d-clientes', 'value')]

)
def create_graph_clientes(contents, filename, start_date, end_date, value,valuec):
    if value:
        df = parse_data(contents, filename)

        df = df.loc[df['Estatus']=='Vigente']         
     
        mask = (df['Fecha factura'] >= start_date) & (df['Fecha factura'] <= end_date)        
        dff = df.loc[mask] 
        dff['Fecha factura'] = dff['Fecha factura'].dt.date

        if value =='Seleccionar todo':
            dff_clientes=dff.assign(Facturas=1)

            #Agrupar los clientes para la tabla
            new_df = (dff_clientes.groupby(["Clientes"])[[" Total ", " Saldo insoluto ",'Facturas']].sum()).reset_index()
            
            #Elegir los 10 mayores por total para graficar
            dff_clientes_max_10 = new_df.nlargest(10, [' Total '])
            
            #Agrupar por fecha para graficas de burbujas y líneas
            new_df2 = (dff_clientes.groupby(["Fecha factura"])[[" Total ", " Saldo insoluto ", 'Facturas']].sum()).reset_index()

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
    
        if valuec=='Todos los clientes':
            #Top 10 mayores clientes     
            fig1 = px.bar( dff_clientes_max_10, x="Clientes", y=" Total ",
                           title=f"<b>Top 10 mayores clientes</b>",
                           text_auto=True,
                           hover_data=['Facturas'])
            fig1.update_yaxes(tickprefix="$", showgrid=True, tickformat=",")
            fig1.update_layout(title_x=0.5)
       
            # Burbujas-Tendencia de facturación en el período      
            fig2 = px.scatter(new_df2, x="Fecha factura", y=" Total ",
                              title=f"<b>Tendencia de facturación en el período</b>",
                              color='Facturas',
                              size='Facturas')
            fig2.update_yaxes(tickprefix="$", showgrid=True, tickformat=",")
            fig2.update_layout( title_x=0.5)

            # Tabla de clientes
            new_df = new_df.rename({' Saldo insoluto ': ' Insoluto'}, axis=1)
            new_df=new_df.round(decimals = 2)
            data= new_df.to_dict('records')  
           
            columns=[
                {"name":'($)'+i, "id": i, "deletable": False, "selectable": True, "hideable": False}
                if i == " Total " or i == " Insoluto"
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
            fig4.update_layout(title_x=0.5)

        else:
                        
            df = dff_clientes.loc[dff_clientes.Clientes == valuec] 
            df = round(df, 2)

            df = (df.groupby(["Fecha factura"])[["Clientes"," Total ", " Saldo insoluto ",'Facturas']].sum()).reset_index()
           
            #Elegir los 10 mayores por total para graficar
            df1 = df.nlargest(10, [' Total '])
            fig1 = px.bar( df1, x="Fecha factura", y=" Total ",
                           title=f"<b>Top 10 días de mayor facturación</b>",
                           text_auto=True,
                           hover_data=['Facturas'])
            fig1.update_yaxes(tickprefix="$", showgrid=True, tickformat=",")
            fig1.update_layout(title_x=0.5)
       
            # Burbujas-Tendencia de facturación en el período      
            fig2 = px.scatter(df, x="Fecha factura", y=" Total ",
                              title=f"<b>Tendencia de facturación en el período</b>",
                              color='Facturas',
                              size='Facturas')
            fig2.update_yaxes(tickprefix="$", showgrid=True, tickformat=",")
            fig2.update_layout( title_x=0.5)

            # Tabla de clientes
            df3 = df.rename({' Saldo insoluto ': ' Insoluto'}, axis=1)
            df3=df3.round(decimals = 2)
            data= df3.to_dict('records')  
           
            columns=[
                {"name":'($)'+i, "id": i, "deletable": False, "selectable": True, "hideable": False}
                if i == " Total " or i == " Insoluto"
                else {"name": i, "id": i, "deletable": False, "selectable": True}
                for i in df3.columns
            ]
        
            #Líneas-Tendencia de cuentas por cobrar
            fig4 = go.Figure(data=[
                go.Line(name='Total', x=df["Fecha factura"], y=df[" Total "]),
                go.Line(name='Saldo insoluto', x=df["Fecha factura"], y=df[" Saldo insoluto "])
            ])
            # Change the bar mode
            fig4.update_layout(barmode='group', title=f"<b>Tendencia de cuentas por cobrar</b>", title_x=0.5)
            fig4.update_yaxes(tickprefix="$", showgrid=True, tickformat=",", title= 'Facturado') 
            fig4.update_xaxes(title='Fecha factura') 
            fig4.update_layout(title_x=0.5)

        
 
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
    if value:
        df = parse_data(contents, filename)
        df = df.loc[df['Estatus']=='Vigente']         
     
        mask = (df['Fecha factura'] >= start_date) & (df['Fecha factura'] <= end_date)        
        dff = df.loc[mask] 

        got_net = Network(directed =True,font_color="white")  
        got_net.barnes_hut()

        if value =='Seleccionar todo':            
            dff_clientes=dff.assign(Cant_Facturas=1)
            got_data = dff_clientes.groupby(["Proveedores", "Clientes"])[[" Total ", " Saldo insoluto ", 'Cant_Facturas']].sum().reset_index()
            media = got_data[' Total '].mean()
            got_data=got_data.assign(Valor_nodo=((got_data[' Total ']/media)+5))
  
            sources = got_data['Proveedores']
            targets = got_data['Clientes']
            weights = got_data['Valor_nodo']
           
            edge_data = zip(sources, targets, weights)

            for e in edge_data:
                            src = e[0]
                            dst = e[1]
                            w = e[2]
   
                            got_net.add_node(src, src, title=src, color='#87C1FF', shape='image', image='https://cdn-icons-png.flaticon.com/512/301/301681.png?w=740&t=st=1680932672~exp=1680933272~hmac=680cc695c234193dad63e907ed80f34866570f045075d316fea2e6dc66bd65d0')
                            got_net.add_node(dst, dst, title=dst, color='lightgreen', shape='image', image='https://cdn-icons-png.flaticon.com/512/846/846398.png?w=740&t=st=1680932405~exp=1680933005~hmac=9cfa44c12263fb9af3730c0ed5168a36e0c38560a4b055faad07d9dee5cb9349')
                            got_net.add_edge(src, dst, value=w)
       
        else:
            for node in got_net.nodes:
                node["value"] = []
            # dataframe filtrado por fechas de los clientes 
            dff_clientes = dff.loc[dff['Proveedores']==value]
            dff_clientes=dff_clientes.assign(Cant_Facturas=1)
            got_data = dff_clientes.groupby(["Proveedores", "Clientes"])[[" Total ", " Saldo insoluto ", 'Cant_Facturas']].sum().reset_index()
            media = got_data[' Total '].mean()
            got_data=got_data.assign(Valor_nodo=((got_data[' Total ']/media)+5)) 

            sources = got_data['Proveedores']
            targets = got_data['Clientes']
            weights = got_data['Valor_nodo']

            edge_data = zip(sources, targets, weights)

            for e in edge_data:
                            src = e[0]
                            dst = e[1]
                            w = e[2]
                    

                            got_net.add_node(src, src, title=src, color='#87C1FF', shape='image', image='https://cdn-icons-png.flaticon.com/512/301/301681.png?w=740&t=st=1680932672~exp=1680933272~hmac=680cc695c234193dad63e907ed80f34866570f045075d316fea2e6dc66bd65d0')
                            got_net.add_node(dst, dst, title=dst, size=w, color='lightgreen', shape='image', image='https://cdn-icons-png.flaticon.com/512/846/846398.png?w=740&t=st=1680932405~exp=1680933005~hmac=9cfa44c12263fb9af3730c0ed5168a36e0c38560a4b055faad07d9dee5cb9349')           
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
            dff_clientes = dff_clientes.groupby(["Clientes"])[[" Total ", " Saldo insoluto ", 'Cant_Facturas']].sum().reset_index()
              

            nclientes = str(dff_clientes['Clientes'].count())
            totalc = dff_clientes[' Total '].sum().round(2)
            saldo_insolutoc = dff_clientes[' Saldo insoluto '].sum().round(2)
            cant_facturasc = str(dff_clientes['Cant_Facturas'].sum())

            dff_proveedores = dff.loc[dff.Clientes == nodo]          
            dff_proveedores=dff_proveedores.assign(Cant_Facturas=1)
            dff_proveedores = dff_proveedores.groupby(["Proveedores"])[[" Total ", " Saldo insoluto ", 'Cant_Facturas']].sum().reset_index()
            

            nproveedores = str(dff_proveedores['Proveedores'].count())
            totalp = dff_proveedores[' Total '].sum().round(2)
            saldo_insolutop = dff_proveedores[' Saldo insoluto '].sum().round(2)
            cant_facturasp = str(dff_proveedores['Cant_Facturas'].sum())

            if x['nodes'][0] != value:
                return [
                    html.Br(),
                    html.H6(nodo),
                    html.Br(),
                    html.Label('Clientes: ' + nclientes),            
                    html.Label('Total: ' + '$' + f"{totalc:,}"), 
                    html.Label('Saldo insoluto: ' + '$' + f"{saldo_insolutoc:,}"),
                    html.Label('Cant. Fact: ' + cant_facturasc),
                    html.Br(),
                    html.Label('Proveedores: ' + nproveedores),                 
                    html.Label('Total: ' + '$' + f"{totalp:,}"),
                    html.Label('Saldo insoluto: ' + '$' + f"{saldo_insolutop:,}"),
                    html.Label('Cant. Fact: ' + cant_facturasp)              
                    ]
            return [ 
                html.Label('Analizada: ' + value)            
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
                    html.Label('Cliente: ' + nodo),                
                    html.Label('Total: ' + '$' + total),
                    html.Label('Saldo insoluto: ' + '$' + saldo_insoluto),
                    html.Label('Cant. Fact: ' + cant_facturas)              
                    ]
            return [ 
                html.H6('Analizada: ' + value)            
                ]
  
    else:
        return [
      html.Label('"Seleccionar nodo proveedor para ver detalles"', style={'textAlign': 'center'})
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
    Input('dropdown_empresa_base', 'value'),
    Input('d-proveedores', 'value')]

)
def create_graph_proveedores(contents, filename, start_date, end_date, value, valuep):
    if value:
        df = parse_data(contents, filename)
        df = df.loc[df['Estatus']=='Vigente']         
     
        mask = (df['Fecha factura'] >= start_date) & (df['Fecha factura'] <= end_date)        
        dff = df.loc[mask] 
        dff['Fecha factura'] = dff['Fecha factura'].dt.date

        if value == 'Seleccionar todo':
            dff_proveedores=dff.assign(Facturas=1)

            #Agrupar los proveedores para la tabla
            new_df = (dff_proveedores.groupby(["Proveedores"])[[" Total ", " Saldo insoluto ",'Facturas']].sum()).reset_index()
            
           
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
        
        if valuep=='Todos los proveedores':
            fig5 = px.bar( dff_proveedores_max_10, x="Proveedores", y=" Total ",                       
                       title=f"<b>Top 10 mayores proveedores</b>",                      
                       text_auto=True,
                       hover_data=['Facturas'])
            fig5.update_yaxes(tickprefix="$", showgrid=True, tickformat=",")
            fig5.update_layout(title_x=0.5)
       
            #Top 10 mayores proveedores----------------------------------------------------
            fig6 = px.scatter(new_df2, x="Fecha factura", y=" Total ",                       
                          title=f"<b>Tendencia de facturación en el período</b>",
                          color='Facturas',
                          size='Facturas')
            fig6.update_yaxes(tickprefix="$", showgrid=True, tickformat=",")
            fig6.update_layout(title_x=0.5)
        
            new_df = new_df.rename({' Saldo insoluto ': ' Insoluto'}, axis=1)
            new_df=new_df.round(decimals = 2)
            data= new_df.to_dict('records')
           
            columns=[
                {"name":'($)'+i, "id": i, "deletable": False, "selectable": True, "hideable": False}
                if i == " Total " or i == " Insoluto"
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
            fig8.update_layout(title_x=0.5) 

        else:
            df = dff_proveedores.loc[dff_proveedores.Proveedores == valuep] 
            df = round(df, 2)
            df = (df.groupby(["Fecha factura"])[["Proveedores"," Total ", " Saldo insoluto ",'Facturas']].sum()).reset_index()
           
            df1 = df.nlargest(10, [' Total '])
            fig5 = px.bar( df1, x="Fecha factura", y=" Total ",                       
                       title=f"<b>Top 10 días de mayor facturación</b>",                      
                       text_auto=True,
                       hover_data=['Facturas'])
            fig5.update_yaxes(tickprefix="$", showgrid=True, tickformat=",")
            fig5.update_layout(title_x=0.5)
       
            #Top 10 mayores proveedores----------------------------------------------------
            fig6 = px.scatter(df, x="Fecha factura", y=" Total ",                       
                          title=f"<b>Tendencia de facturación en el período</b>",
                          color='Facturas',
                          size='Facturas')
            fig6.update_yaxes(tickprefix="$", showgrid=True, tickformat=",")
            fig6.update_layout(title_x=0.5)
        
            df4 = df.rename({' Saldo insoluto ': ' Insoluto'}, axis=1)
            df4=df4.round(decimals = 2)
            data= df4.to_dict('records')
           
            columns=[
                {"name":'($)'+i, "id": i, "deletable": False, "selectable": True, "hideable": False}
                if i == " Total " or i == " Insoluto"
                else {"name": i, "id": i, "deletable": False, "selectable": True}
                for i in df4.columns
                ]

            fig8 = go.Figure(data=[
                   go.Line(name='Total' , x=df["Fecha factura"], y=df[" Total "]),
                   go.Line(name='Saldo insoluto', x=df["Fecha factura"], y=df[" Saldo insoluto "])
                   ])
            # Change the bar mode
            fig8.update_layout(barmode='group', title=f"<b>Tendencia de cuentas por pagar</b>", title_x=0.5)
            fig8.update_yaxes(tickprefix="$", showgrid=True, tickformat=",", title= 'Facturado') 
            fig8.update_xaxes(title='Fecha factura')
            fig8.update_layout(title_x=0.5) 

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

        got_net = Network(directed =True, font_color="white")
        got_net.barnes_hut()
         
        if value =='Seleccionar todo':            
            dff_proveedores=dff.assign(Cant_Facturas=1)
            got_data = dff_proveedores.groupby(["Proveedores", "Clientes"])[[" Total ", " Saldo insoluto ", 'Cant_Facturas']].sum().reset_index()
            media = got_data[' Total '].mean()
            got_data=got_data.assign(Valor_nodo=((got_data[' Total ']/media)+5))

            sources = got_data['Proveedores']
            targets = got_data['Clientes']
            weights = got_data['Valor_nodo']
           
            edge_data = zip(sources, targets, weights)

            for e in edge_data:
                            src = e[0]
                            dst = e[1]
                            w = e[2]
          

                            got_net.add_node(src, src, title=src, color=' #87C1FF', shape='image', image='https://cdn-icons-png.flaticon.com/512/301/301681.png?w=740&t=st=1680932672~exp=1680933272~hmac=680cc695c234193dad63e907ed80f34866570f045075d316fea2e6dc66bd65d0')
                            got_net.add_node(dst, dst, title=dst, color='lightgreen',shape='image', image='https://cdn-icons-png.flaticon.com/512/846/846398.png?w=740&t=st=1680932405~exp=1680933005~hmac=9cfa44c12263fb9af3730c0ed5168a36e0c38560a4b055faad07d9dee5cb9349')
                            got_net.add_edge(src, dst, value=w)

            
        else:
            # dataframe filtrado por fechas de los proveedores 
            dff_proveedores = dff.loc[dff['Clientes']==value]
            dff_proveedores=dff_proveedores.assign(Cant_Facturas=1)
            got_data = dff_proveedores.groupby(["Clientes", "Proveedores"])[[" Total ", " Saldo insoluto ", 'Cant_Facturas']].sum().reset_index()
            media = got_data[' Total '].mean()
            got_data=got_data.assign(Valor_nodo=((got_data[' Total ']/media)+5))
            
            sources = got_data['Proveedores']
            targets = got_data['Clientes']
            weights = got_data['Valor_nodo']
           
            edge_data = zip(sources, targets, weights)

            for e in edge_data:
                            src = e[0]
                            dst = e[1]
                            w = e[2]
          

                            got_net.add_node(src, src, title=src, size=w, color='#87C1FF', shape='image', image='https://cdn-icons-png.flaticon.com/512/301/301681.png?w=740&t=st=1680932672~exp=1680933272~hmac=680cc695c234193dad63e907ed80f34866570f045075d316fea2e6dc66bd65d0')
                            got_net.add_node(dst, dst, title=dst, color='lightgreen', shape='image', image='https://cdn-icons-png.flaticon.com/512/846/846398.png?w=740&t=st=1680932405~exp=1680933005~hmac=9cfa44c12263fb9af3730c0ed5168a36e0c38560a4b055faad07d9dee5cb9349')
                            got_net.add_edge(src, dst, value=w)  

        data = {'nodes': got_net.nodes,
                'edges': [{'id': str(edge['from']) + " __ " + str(edge['to']),
                           'from': edge['from'],
                           'to': edge['to'],
                           'arrows':'to'
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
           dff_clientes = dff.loc[dff.Proveedores == nodo]                      
           dff_clientes=dff_clientes.assign(Cant_Facturas=1)
           dff_clientes = dff_clientes.groupby(["Clientes"])[[" Total ", " Saldo insoluto ", 'Cant_Facturas']].sum().reset_index()
         

           nclientes = str(dff_clientes['Clientes'].count())
           totalc = dff_clientes[' Total '].sum().round(2)
           saldo_insolutoc = dff_clientes[' Saldo insoluto '].sum().round(2)
           cant_facturasc = str(dff_clientes['Cant_Facturas'].sum())

           dff_proveedores = dff.loc[dff.Clientes == nodo]          
           dff_proveedores=dff_proveedores.assign(Cant_Facturas=1)
           dff_proveedores = dff_proveedores.groupby(["Proveedores"])[[" Total ", " Saldo insoluto ", 'Cant_Facturas']].sum().reset_index()
         

           nproveedores = str(dff_proveedores['Proveedores'].count())
           totalp = dff_proveedores[' Total '].sum().round(2)
           saldo_insolutop = dff_proveedores[' Saldo insoluto '].sum().round(2)
           cant_facturasp = str(dff_proveedores['Cant_Facturas'].sum())

           if x['nodes'][0] != value:
               return [
                   html.Br(),
                   html.H6(nodo),                    
                   html.Br(),
                   html.Label('Proveedores: ' + nproveedores),                 
                   html.Label('Total: ' + '$' + f"{totalp:,}"),
                   html.Label('Saldo insoluto: ' + '$' + f"{saldo_insolutop:,}"),
                   html.Label('Cant. Fact: ' + cant_facturasp),
                   html.Br(),
                   html.Label('Clientes: ' + nclientes),            
                   html.Label('Total: ' + '$' + f"{totalc:,}"), 
                   html.Label('Saldo insoluto: ' + '$' + f"{saldo_insolutoc:,}"),
                   html.Label('Cant. Fact: ' + cant_facturasc),               
                   ]
           return [ 
               html.Label('Analizada: ' + value)            
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
                    html.Label('Proveedor: ' + nodo),                
                    html.Label('Total: ' + '$' + total),
                    html.Label('Saldo insoluto: ' + '$' + saldo_insoluto),
                    html.Label('Cant. Fact: ' + cant_facturas)              
                    ]
            return [ 
                html.Label('Analizada: ' + value)            
                ]
  
    else:
        return [
      html.Label('"Seleccionar nodo proveedor para ver detalles"', style={'textAlign': 'center'})
    ]   

def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


# ##########   AYUDA PRINCIPAL ################################
callback(
    Output("modal-body-scroll", "is_open"),
    [
        Input("open-body-scroll", "n_clicks"),
        Input("close-body-scroll", "n_clicks"),
    ],
    [State("modal-body-scroll", "is_open")],
)(toggle_modal)    


# ##########   AYUDA TABLA ################################
callback(
    Output("modal-tabla", "is_open"),
    [
        Input("open-tabla", "n_clicks"),
        Input("close-tabla", "n_clicks"),
    ],
    [State("modal-tabla", "is_open")],
)(toggle_modal)   

# ##########   TOAST ################################
@callback(
    Output("info-toast2", "children"),
    [Input("dropdown_empresa_base", "value"),
    Input('upload-data', 'contents'),
    Input('upload-data', 'filename')]
)
def open_toast(value,contents, filename):
    if contents:
        df = parse_data(contents, filename) 
        if df.empty == False:
            if value:
                return [
                    dbc.Toast(
                    id="toast4",
                    header="¡Empresa seleccionada!",
                    icon="success",
                    duration=1000,
                    dismissable=True,
                    is_open=True,
                   style={"position": "fixed", "top": 230, "right": 350, "width": 200}),
                ]
            
            else:                          
                return [
                   dbc.Toast(
                     id="toast5",
                     header="En el panel principal seleccionar empresa a analizar!!!",
                     icon="info",
                     dismissable=True,
                     is_open=True,
                     style={"position": "fixed", "top": 250, "left": 550, "width": 400}
                    ),
                ]
        
        
    

        
