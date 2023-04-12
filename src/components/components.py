# Import necessary libraries
from dash import html
import dash_bootstrap_components as dbc


# Define the navbar




modal = html.Div(
    [
        dbc.Button("?", id="open-body-scroll", n_clicks=0, outline=True, color="info", size="lg"),
        
       
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Ayuda")),
                dbc.ModalBody([html.H4('Objetivo:'),
                              html.P('Aplicación web interactiva para visualización y análisis de datos de CFDI (carácter educativo).'),
                              html.H4('Estructura:'),
                              html.H6('Barra de navegación (Nombre, enlaces y ayuda).'),
                              html.H6('Panel de control. '),
                              html.H6('Páginas de la aplicación: Inicio, Clientes (Análisis de Clientes, Red de Clientes), Proveedores (Análisis de Proveedores-Red de Proveedores)).'),
                              html.H5('Barra de navegación'),
                              html.P('A la izquierda la barra de navegación con nombre de la aplicación, a la derecha enlaces a las páginas de la aplicación Inicio, Clientes (Análisis de Clientes, Red de Clientes), Proveedores (Análisis de Proveedores-Red de Proveedores), y ayuda (?).'),
                              html.H5('Panel de control'),
                              html.H6('Carga de datos'),
                              html.P('Se puede accionar en el enlace para carga de datos o arrastrar y soltar sobre el componente de carga, los datos permitidos son en .CSV, las columnas utilizadas son ["Proveedores", "Clientes", "Fecha factura", "Metodo de pago", "Moneda", "Tipo de cambio", " Total ", "Estatus", " Saldo insoluto ", "Estatus pago", "Deducible"].'),
                              html.H6('Selector de rango de fechas: '),
                              html.P('Al cargar los datos analiza la fecha inicial y final de los datos cargados y los refleja en el selector que es modificable según necesidad. Al modificar selector solo permite elegir dentro del rango de fechas detectado.'),
                              html.H6('Selector de empresa a analizar'),
                              html.P('Al cargar los datos detecta las empresas presentes en los datos y los muestra en el selector, se puede seleccionar una o elegir todas.'),
                              html.H5('Páginas'),
                              html.H6('Inicio:'),
                              html.P('Al cargar los datos y seleccionar empresa a analizar crea una tabla en la parte inferior con la relación de facturas vigentes y canceladas presentes en los datos. El resumen de la tabla se muestra en la parte superior de la tabla dividido en Clientes(izquierda) y Proveedores(derecha).'
                                      ' Los selectores de radio y de nombre de empresa afectan directamente a la tabla y el resumen y se utilizan para crear filtros y relaciones deseadas en comparación con la empresa analizada seleccionada en Panel de Control.'
                                      ' La tabla es dinámica y puede realizarse filtros con >, <, =,  =!, >=, entre otros. Esto no afecta los datos presentes en la tabla dinámica ni el resumen superior.'),
                              html.H6('Análisis de Clientes:'),
                              html.P('Gráfico de barras (Muestra los 10 mayores clientes).' 
                                    ' Gráfico de burbujas (Muestra la agrupación de facturas a clientes por día en un periodo de tiempo).' 
                                    ' Tabla dinámica (Muestra toda la relación de clientes de acuerdo con la empresa a analizar seleccionada en el Panel de Control). Gráfico de líneas (Muestra la relación entre Facturado y Saldo Insoluto en el transcurso del tiempo analizado).'),
                              html.H6('Red de Clientes: '), 
                              html.P('Muestra la red de clientes con relación a la empresa analizada. En caso de seleccionar todo muestra toda la red.'
                                     ' Al seleccionar un nodo muestra nombre del Proveedor, cantidad de Clientes, Total facturado, Saldo insoluto y Cantidad de Facturas realizadas.'
                                     ' Al iniciar, la red se extiende antes de contraerse, puede ver completamente haciendo ZOOM IN con el scroll del mouse o el touchpad.'), 
                              html.H6('Análisis de Proveedores: '),
                              html.P('Gráfico de barras (Muestra los 10 mayores proveedores).'
                                     ' Gráfico de burbujas (Muestra la agrupación de facturas a clientes por día en un periodo de tiempo).'
                                     ' Tabla dinámica (Muestra toda la relación de proveedores de acuerdo con la empresa a analizar seleccionada en el Panel de Control).'
                                     ' Gráfico de líneas (Muestra la relación entre Facturado y Saldo Insoluto de los clientes en el transcurso del tiempo analizado).'),
                              html.H6('Red de Proveedores: '), 
                              html.P('Muestra la red de proveedores con relación a la empresa analizada. En caso de seleccionar todo en empresa analizada empresas muestra toda la red.'
                                     ' Al iniciar, la red se extiende antes de contraerse, puede ver completamente haciendo ZOOM IN con el scroll del mouse o el touchpad.'
                                     ' Al seleccionar un nodo muestra nombre del Cliente, cantidad de Proveedores, Total facturado, Saldo insoluto y Cantidad de Facturas realizadas.'),
                              
                              ]

                              ),
                              
                dbc.ModalFooter(
                    dbc.Button(
                        "Close",
                        id="close-body-scroll",
                        size="xl",
                        n_clicks=0,
                    )
                ),
            ],
            id="modal-body-scroll",
            scrollable=True,
            is_open=False,
            size="xl",
            class_name="modal-style"
        ),
    ])



# Define the navbar structure
navbar= layout = html.Div([
        dbc.NavbarSimple(
            children=[               
                dbc.NavItem(dbc.NavLink("Inicio", href="/inicio", active='exact')),
                dbc.DropdownMenu(
                    children=[
                        dbc.DropdownMenuItem("Análisis de Clientes", href="/analisis_clientes"),
                        dbc.DropdownMenuItem("Red de Clientes", href="/red_clientes"),
                    ],
                    nav=True,
                    in_navbar=True,
                    label="Clientes",
                ),
                dbc.DropdownMenu(
                    children=[
                        dbc.DropdownMenuItem("Análisis de Proveedores", href="/analisis_proveedores"),
                        dbc.DropdownMenuItem("Red de Proveedores", href="/red_proveedores"),
                    ],
                    nav=True,
                    in_navbar=True,
                    label="Proveedores",
                ),
                dbc.Col(modal, width={"size": 1, "offset": 3},  align="center"),

            ] ,
            brand="VisCFDI",
            brand_href="/inicio",
            color="primary",
            dark=True,
        ), 
    ])

