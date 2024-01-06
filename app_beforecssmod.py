#importar librerias
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
from dash import dash_table
import glob
import os
import plotly.express as px
import sqlite3

from dash.exceptions import PreventUpdate


# Connect to database
conn = sqlite3.connect('progreso.db')

# Query everything from movimientos table
query = 'SELECT * FROM movimientos'
df = pd.read_sql_query(query, conn)

#convertir la columna FECHAS a formato datetime
df['fecha'] = pd.to_datetime(df['fecha'])
df['Ano'] = df['fecha'].dt.year
df['Mes'] = df['fecha'].dt.month
df['Dia'] = df['fecha'].dt.day
df['Hora'] = df['fecha'].dt.hour
df['NombreDia'] = df['fecha'].dt.day_name()


# ***--- Begin DASH APP ---***

font_awesome = "https://use.fontawesome.com/releases/v5.10.2/css/all.css"
meta_tags = [{"name":"viewport", "content":"width=device-width, initial-scale=1"}]
external_stylesheets = [meta_tags, font_awesome]

app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

app.title = "Progreso"

server = app.server

app.layout = html.Div([

    # Div 1 Begins
    html.Div([

        #1.1 DIV Logo
        html.Div([
                html.Img(src=app.get_asset_url('log_prog.png'),
                style = {
                        'max-width':'100%',
                        'height':'auto',
                        },
                ),
        ],  className='one-half column', 
            style={'border-width':'1px',
                    'border-style':'solid',
                    'border-color':'black',
                    }
        ),

        #1.2 DIV Titulo
        html.Div([
                #html.Img(src=app.get_asset_url('log_prog.png'),
                html.H5('Cuadro de Control Gerencial', id='title',
                style = {
                        'max-width':'100%',
                        'height':'auto',
                        },
                        
                ),
        ],  className='one-half column', 
            style={'border-width':'1px',
                    'border-style':'solid',
                    'border-color':'black',
                    #'font-size':'162.5%',
                    #'font-weight':'bold',
                    }
        ),

    ],className='column', 
      style={'border-width':'2px',
            'border-color':'red',
            'border-style':'solid',}),
    # Div 1 Ends
    
    # Div 2 BEGINS SLIDERS
    html.Div([
        
        # 2.1 Slider para escojer el año
        html.Div([
            html.P('Año'),
            dcc.Slider(id = 'select_years',
                       included=False,
                       updatemode='drag',
                       tooltip={'always_visible':True},
                       min = 2022,
                       max = 2023,
                       step = 1,
                       value = 2023,
                       marks={
                           2022: '2022',
                           2023: '2023',
                       },
                       #className='dcc_compon'),
                       )
        ],className='one-half column',
                style={'border-width':'2px',
                    'border-color':'blue',
                    'border-style':'solid',}),

        # Div 2.1 ends

        # 2.2 Slider para escojer Mes
        html.Div([
            html.P('Mes'),
            dcc.Slider(id='select_months',
                       included=False,
                       updatemode='drag',
                       tooltip={'always_visible':True},
                       min = 1,
                       max = 12,
                       step = 1, 
                       # change this value to latest month
                       value=12,

                       marks={
                           1: 'Ene',
                           2: 'Feb',
                           3: 'Mar',
                           4: 'Abr',
                           5: 'May',
                           6: 'Jun',
                           7: 'Jul',
                           8: 'Ago',
                           9: 'Sep',
                           10: 'Oct',
                           11: 'Nov',
                           12: 'Dic',
                       },
            ),
        ], className='one-half column',
                style={'border-width':'2px',
                    'border-color':'blue',
                    'border-style':'solid',
                }
            ),
        
        #Div 2.2 ends

    
    ]   ,style={'border-width':'2px',
            'border-color':'green',
            'border-style':'solid',
        
        }
    ,className='container column'),
    # Div 2 SLIDERS Ends





    # DIV 3 BEGINS CHARTS SUCURSALES

    html.Div([

        html.Div([
            html.P('Oficina Central',
                   style = {
                       'color':'black',
                       'fontSize':'14',
                       'font-weight':'Bold',
                       'text-align':'center',
                       'text-decoration':'underline',
                   }),


            html.Div([
                html.Div([
                    html.Div(id='sucursal1_diferencia_captaciones', className='card_size'),
                    html.Div(id='sucursal1_diferencia_colocaciones', className='card_size'),
                    html.Div(id='sucursal1_diferencia_captaciones_vs_colocaciones', className='card_size_2'),
                ],className='flex_item_1'),

                html.Div([
                    dcc.Graph(
                        id='sucursal1_chart',
                        style={
                            'width':'100%',
                            'height':'100%',
                        }
                    )
                ],className='flex_item_2'),
            ],className='flex_row'),

        ], className='one-half column apply_border'),



        html.Div([
            html.P('La Guardia',
                   style = {
                       'color':'black',
                       'fontSize':'14',
                       'font-weight':'Bold',
                       'text-align':'center',
                       'text-decoration':'underline',
                   }),


            html.Div([
                html.Div([
                    html.Div(id='sucursal2_diferencia_captaciones', className='card_size'),
                    html.Div(id='sucursal2_diferencia_colocaciones', className='card_size'),
                    html.Div(id='sucursal2_diferencia_captaciones_vs_colocaciones', className='card_size_2'),
                ],className='flex_item_1'),

                html.Div([
                    dcc.Graph(
                        id='sucursal2_chart',
                        style={
                            'width':'100%',
                            'height':'100%',
                        }
                    )
                ],className='flex_item_2'),
            ],className='flex_row'),

        ], className='one-half column apply_border')
    ],className='column apply_border'),
    # Div 3 Ends

    # Div 4 Begins
    html.Div([

        # Div 3.1 Begins Sucursal dropdown
        html.Div([
            dcc.Dropdown(
                id='sucursal_dropdown',
                options = df['sucursal'].unique(),
                value = 'Oficina Central',
            )
        ], className='one-third column'),
        # Div 3.1 Ends

        # Div 3.2 Begins - Movimiento
        html.Div([
            dcc.Dropdown(
                id='movimiento_dropdown',
                options = df['movimiento'].unique(),
                value = 'Colocaciones',
            )
        ], className='one-third column'),
        # Div 3.2 Ends

        # Div 3.3 Begins - Tipo de Movimiento
        html.Div([
            dcc.Dropdown(
                id='tipo_de_movimiento_dropdown',
                options = df['tipo_de_movimiento'].unique(),
                value = 'Microcreditos',
            )
        ], className='one-third column'),
        # Div 3.3 Ends
    ],className='container column'),
    # Div 4 Ends

    # Div 5 Begins
    html.Div([

        # Div 4.1 Graph 3 INPUT 1 OUTPUT TEST
        html.Div([
            dcc.Graph(
                id='sucursales_charts',
                style={
                    'width':'100%',
                    'height':'100%',
                }
            )
        ])
    ],className='container column'),
    # Div 5 ENDS


# Main Div endss
#],  className='container')
],)

# END OF HTML






# *** CALLBACKS *** CALLBACKS *** CALLBACKS ***




##### CALLBACK SUCURSALES ####

### SUCURSAL 1 OFICINA CENTRAL ###

# CB 1.1.1 LINE CHART Oficina Central

@app.callback(
    Output('sucursal1_chart', 'figure'),
    [Input('select_years', 'value'),
    Input('select_months', 'value')]
)

def update_branch_chart(select_years, select_months):

    # Crear df con la sucursal 'Oficina Central'
    df_1 = df[df['sucursal']=='Oficina Central']

    # Agrupar df con las columnas selleccionadas
    df_2 = df_1.groupby(['Ano', 'Mes', 'Dia', 'movimiento'])['monto'].sum().reset_index()
      
    # Crear df de acuerdo al año y mes seleccionados
    df_3 = df_2[(df_2['Ano'] == select_years) & (df_2['Mes'] == select_months)]

    fig = px.line(

        df_3,
        x='Dia',
        y='monto',
        color='movimiento',
        #title='Oficina Central',
        markers=True,
        line_dash_sequence=None,
        symbol_sequence=None,
    )

    fig.update_layout(
        legend=dict(
            title_text='',
            orientation="h",
            entrywidth=50, 
            yanchor="bottom", 
            y=1.00, 
            xanchor="right", 
            x=1.0,
            font=dict(
                size=9
            )
        ),
        margin=dict(
            b=10,
            l=0,
            r=10,
            t=10,
        )
    )
    fig.update_xaxes(title_text='')
    fig.update_yaxes(title_text='')

    return fig


# CB 1.1.2 CALLBACK CAPTACIONES Oficina Central
@app.callback(
    Output('sucursal1_diferencia_captaciones', 'children'),
    [Input('select_years', 'value'),
    Input('select_months', 'value')]
)

def update_text(select_years, select_months):
    if select_months is None:
        raise PreventUpdate
    else:

        # Crear df con la sucursal 'Oficina Central'
        df_1 = df[df['sucursal']=='Oficina Central']

        # Agrupar df con las columnas selleccionadas por dia
        df_2 = df_1.groupby(['Ano', 'Mes', 'Dia', 'movimiento'])['monto'].sum().reset_index()
      
        # Crear df de acuerdo al año y mes seleccionados
        df_3 = df_2[(df_2['Ano'] == select_years) & (df_2['Mes'] == select_months)]


        ### Total Captaciones
        # query total captaciones
        captaciones = df_3.loc[df_3['movimiento'] == 'Captaciones', 'monto'].sum()



        ### Calcular diferencia con el mes anterior ###
        # Agrupar df con las columnas selleccionadas por mes
        df_by_month = df_1.groupby(['Ano', 'Mes', 'movimiento'])['monto'].sum().reset_index()
     

        ### CAPTACIONES
        # df Diferencia captaciones con el mes anterior
        df_by_month_captaciones = df_by_month[(df_by_month['movimiento'] == 'Captaciones') & ('monto' in df_by_month.columns)].groupby(['Ano', 'Mes']).sum()   
        df_by_month_captaciones = df_by_month_captaciones.reset_index()

        # Crear columna que Calcula el la diferencia con el mes anterior en captaciones
        df_by_month_captaciones['diferencia_mes_anterior'] = df_by_month_captaciones['monto'].diff()

        ### Calcular cambio de porcentaje entre dos meses en captaciones
        df_by_month_captaciones['diferencia_pct'] = (df_by_month_captaciones['monto'].pct_change()) * 100

        # Filtrar captaciones por mes
        filter_month_captaciones = df_by_month_captaciones[(df_by_month_captaciones['Ano'] == select_years) & (df_by_month_captaciones['Mes'] == select_months)]

        # Diferencia del monto con el mes anterior filtrado
        captaciones_diferencia_monto_filtrado = filter_month_captaciones['diferencia_mes_anterior'].iloc[0]

        # Diferencia de porcentaje con el mes anterior filtrado
        captaciones_diferencia_pct_filtrado = filter_month_captaciones['diferencia_pct'].iloc[0]



        ### COLOCACIONES
        # df Diferencia colocaciones con el mes anterior
        df_by_month_colocaciones = df_by_month[(df_by_month['movimiento'] == 'Colocaciones') & ('monto' in df_by_month.columns)].groupby(['Ano', 'Mes']).sum()  
        df_by_month_colocaciones = df_by_month_colocaciones.reset_index()
      
        
        # Crear columna que Calcula el la diferencia con el mes anterior en colocaciones
        df_by_month_colocaciones['diferencia_mes_anterior'] = df_by_month_colocaciones['monto'].diff()

        ### Calcular cambio de porcentaje entre dos meses en colocaciones
        df_by_month_colocaciones['diferencia_pct'] = (df_by_month_colocaciones['monto'].pct_change()) * 100

        # Filtrar colocaciones por mes
        filter_month_colocaciones = df_by_month_colocaciones[(df_by_month_colocaciones['Ano'] == select_years) & (df_by_month_colocaciones['Mes'] == select_months)]


        # Diferencia del monto con el mes anterior filtrado
        colocaciones_diferencia_monto_filtrado = filter_month_colocaciones['diferencia_mes_anterior'].iloc[0]

        # Diferencia de porcentaje con el mes anterior filtrado
        colocaciones_diferencia_pct_filtrado = filter_month_colocaciones['diferencia_pct'].iloc[0]



        if captaciones_diferencia_monto_filtrado > 0:
            return [
                # Inicio Div Container
                html.Div([

                    # Total Captaciones Mes TEXT
                    html.P('Total Captaciones Mes:',
                        style = {
                                'color':'#046e27',
                                'fontSize':13,
                                'font-weight':'bold',  
                                'text-align':'center',  
                        }
                    ),

                    html.Div([
                        # Total Captaciones MONTO
                        html.Div([
                            html.P('Bs {0:,.0f}'.format(captaciones),
                                style={
                                    'color': '#000000',
                                    'fontSize': 13,
                                    'font-weight':'bold',
                                    'text-align':'center',
                                })
                        ]),
                        # Green Arrow up
                        html.Div([
                            html.I(className = "fas fa-caret-up",
                                style = {"font-size": "25px",
                                        'color': '#00cc00'},
                           ),
                        ], className = 'value_indicator'),
                    ], className = 'value_and_indicator'),

                    # VS mes anterior text
                    html.Div([
                        html.P('vs mes anterior:',
                               style = {
                                   'color':'#333333',
                                   'fontSize':12,
                                   'font-weight':'bold',
                                   'text-align':'center',
                               }
                        )
                    ], className = 'vs_mes_anterior'),

                    # Div ROW holder for monto diferencia en captaciones y pct en captaciones
                    html.Div([
                        # Div holder for monto diferencia en captaciones
                        html.Div([
                            html.P('Bs {0:,.2f}'.format(captaciones_diferencia_monto_filtrado),
                                   style={
                                       'color': '#00cc00',
                                       'fontSize': 12,
                                   }
                            )
                        ], className='monthly_difference_value'),
                        # Div holder for monto porcentaje en captaciones
                        html.Div([
                            html.P('{0:,.1f}%'.format(captaciones_diferencia_pct_filtrado),
                                    style={
                                       'color': '#00cc00',
                                       'fontSize': 12,
                                   }
                            ),    
                        ],className='monthly_difference_value'),
                    ], className='difference_value_row'),

                # FIN DEL DIV Container
                ]),

            ]
        elif captaciones_diferencia_monto_filtrado < 0:
            return [
                # Inicio Div Container
                html.Div([
                    # Total Captaciones Mes TEXT
                    html.P('Total Captaciones Mes:',
                        style = {
                                'color':'#046e27',
                                'fontSize':13,
                                'font-weight':'bold',  
                                'text-align':'center',  
                        }
                    ),

                    html.Div([
                        # Total Captaciones MONTO
                        html.Div([
                            html.P('Bs {0:,.0f}'.format(captaciones),
                                style={
                                    'color': '#000000',
                                    'fontSize': 13,
                                    'font-weight':'bold',
                                    'text-align':'center',
                                })
                        ]),
                        # Red Arrow Down
                        html.Div([
                            html.I(className = "fas fa-caret-down",
                                style = {"font-size": "25px",
                                        'color': '#EC1E3D'},
                           ),
                        ], className = 'value_indicator'),
                    ], className = 'value_and_indicator'),

                    # Vs Mes anterior
                    html.Div([
                        html.P('vs mes anterior:',
                               style = {
                                   'color':'#333333',
                                   'fontSize':12,
                                   'font-weight':'bold',
                                   'text-align':'center',
                               }
                        )
                    ], className = 'vs_mes_anterior'),

                    # Div ROW holder for monto diferencia en captaciones y pct en captaciones
                    html.Div([
                        # Div holder for monto diferencia en captaciones
                        html.Div([
                            html.P('Bs {0:,.2f}'.format(captaciones_diferencia_monto_filtrado),
                                   style={
                                       'color': '#EC1E3D',
                                       'fontSize': 12,
                                   }
                            )
                        ], className='monthly_difference_value'),
                        # Div holder for monto porcentaje en captaciones
                        html.Div([
                            html.P('{0:,.1f}%'.format(captaciones_diferencia_pct_filtrado),
                                    style={
                                       'color': '#EC1E3D',
                                       'fontSize': 12,
                                   }
                            ),    
                        ],className='monthly_difference_value'),
                    ], className='difference_value_row'),

                # FIN DEL DIV Container
                ]),

            ]



### CB 1.1.3 CALLBACK COLOCACIONES Oficina Central
@app.callback(
    Output('sucursal1_diferencia_colocaciones', 'children'),
    [Input('select_years', 'value'),
    Input('select_months', 'value')]
)

def update_text(select_years, select_months):
    if select_months is None:
        raise PreventUpdate
    else:

        # Crear df con la sucursal 'Oficina Central'
        df_1 = df[df['sucursal']=='Oficina Central']

        # Agrupar df con las columnas selleccionadas por dia
        df_2 = df_1.groupby(['Ano', 'Mes', 'Dia', 'movimiento'])['monto'].sum().reset_index()
      
        # Crear df de acuerdo al año y mes seleccionados
        df_3 = df_2[(df_2['Ano'] == select_years) & (df_2['Mes'] == select_months)]

        ### Colocaciones y Captaciones
        # query total colocaciones
        colocaciones = df_3.loc[df_3['movimiento'] == 'Colocaciones', 'monto'].sum()

        # query total captaciones
        captaciones = df_3.loc[df_3['movimiento'] == 'Captaciones', 'monto'].sum()

        # Diferencia de colocaciones con captaciones
        diferencia_movimiento = colocaciones - captaciones

        ### Calcular diferencia con el mes anterior ###
        # Agrupar df con las columnas selleccionadas por mes
        df_by_month = df_1.groupby(['Ano', 'Mes', 'movimiento'])['monto'].sum().reset_index()


        ### COLOCACIONES
        # df Diferencia colocaciones con el mes anterior
        df_by_month_colocaciones = df_by_month[(df_by_month['movimiento'] == 'Colocaciones') & ('monto' in df_by_month.columns)].groupby(['Ano', 'Mes']).sum()  
        df_by_month_colocaciones = df_by_month_colocaciones.reset_index()
      
        
        # Crear columna que Calcula el la diferencia con el mes anterior en colocaciones
        df_by_month_colocaciones['diferencia_mes_anterior'] = df_by_month_colocaciones['monto'].diff()

        ### Calcular cambio de porcentaje entre dos meses en colocaciones
        df_by_month_colocaciones['diferencia_pct'] = (df_by_month_colocaciones['monto'].pct_change()) * 100

        # Filtrar colocaciones por mes
        filter_month_colocaciones = df_by_month_colocaciones[(df_by_month_colocaciones['Ano'] == select_years) & (df_by_month_colocaciones['Mes'] == select_months)]


        # Diferencia del monto con el mes anterior filtrado
        colocaciones_diferencia_monto_filtrado = filter_month_colocaciones['diferencia_mes_anterior'].iloc[0]

        # Diferencia de porcentaje con el mes anterior filtrado
        colocaciones_diferencia_pct_filtrado = filter_month_colocaciones['diferencia_pct'].iloc[0]



        if colocaciones_diferencia_monto_filtrado > 0:
            return [
                html.Div([

                    # Total Colocaciones Mes TEXT
                    html.P('Total Colocaciones Mes:',
                        style = {
                                'color':'#046e27',
                                'fontSize':13,
                                'font-weight':'bold',  
                                'text-align':'center',  
                        }
                    ),

                    html.Div([
                        # Total Colocaciones MONTO
                        html.Div([
                            html.P('Bs {0:,.0f}'.format(colocaciones),
                                style={
                                    'color': '#000000',
                                    'fontSize': 13,
                                    'font-weight':'bold',
                                    'text-align':'center',
                                })
                        ]),
                        # Green Arrow up
                        html.Div([
                            html.I(className = "fas fa-caret-up",
                                style = {"font-size": "25px",
                                        'color': '#00cc00'},
                           ),
                        ], className = 'value_indicator'),
                    ], className = 'value_and_indicator'),

                    # VS mes anterior text
                    html.Div([
                        html.P('vs mes anterior:',
                               style = {
                                   'color':'#333333',
                                   'fontSize':12,
                                   'font-weight':'bold',
                                   'text-align':'center',

                               }   )
                    ], className = 'vs_mes_anterior'),

                    # Div ROW holder for monto diferencia en captaciones y pct en captaciones
                    html.Div([
                        # Div holder for monto diferencia en captaciones
                        html.Div([
                            html.P('Bs {0:,.2f}'.format(colocaciones_diferencia_monto_filtrado),
                                   style={
                                       'color': '#00cc00',
                                       'fontSize': 12,
                                   }
                            )
                        ], className='monthly_difference_value'),
                        # Div holder for monto porcentaje en captaciones
                        html.Div([
                            html.P('{0:,.1f}%'.format(colocaciones_diferencia_pct_filtrado),
                                    style={
                                       'color': '#00cc00',
                                       'fontSize': 12,
                                   }
                            ),    
                        ],className='monthly_difference_value'),
                    ], className='difference_value_row'),
            
                # FIN DEL DIV
                ]),
            ]
        elif colocaciones_diferencia_monto_filtrado < 0:
            return [
                html.Div([

                    # Total Colocaciones Mes TEXT
                    html.P('Total Colocaciones Mes:',
                        style = {
                                'color':'#046e27',
                                'fontSize':13,
                                'font-weight':'bold',  
                                'text-align':'center',  
                        }
                    ),

                    html.Div([
                        # Total Colocaciones MONTO
                        html.Div([
                            html.P('Bs {0:,.0f}'.format(colocaciones),
                                style={
                                    'color': '#000000',
                                    'fontSize': 13,
                                    'font-weight':'bold',
                                    'text-align':'center',
                                })
                        ]),
                        # Red Arrow Down
                        html.Div([
                            html.I(className = "fas fa-caret-down",
                                style = {"font-size": "25px",
                                        'color': '#EC1E3D'},
                           ),
                        ], className = 'value_indicator'),
                    ], className = 'value_and_indicator'),


                    # Vs Mes anterior
                    html.Div([
                        html.P('vs mes anterior:',
                               style = {
                                   'color':'#333333',
                                   'fontSize':12,
                                   'font-weight':'bold',
                                   'text-align':'center',

                               }   )
                    ], className = 'vs_mes_anterior'),

                    # Div ROW holder for monto diferencia en captaciones y pct en captaciones
                    html.Div([
                        # Div holder for monto diferencia en captaciones
                        html.Div([
                            html.P('Bs {0:,.2f}'.format(colocaciones_diferencia_monto_filtrado),
                                   style={
                                       'color': '#EC1E3D',
                                       'fontSize': 12,
                                   }
                            )
                        ], className='monthly_difference_value'),
                        # Div holder for monto porcentaje en captaciones
                        html.Div([
                            html.P('{0:,.1f}%'.format(colocaciones_diferencia_pct_filtrado),
                                    style={
                                       'color': '#EC1E3D',
                                       'fontSize': 12,
                                   }
                            ),    
                        ],className='monthly_difference_value'),
                    ], className='difference_value_row'),
            
                # FIN DEL DIV
                ]),
            ]
    

### CB 1.1.4 CALLBACK DIFERENCIA COLOCACIONES VS CAPTACIONES - Oficina Central
@app.callback(
    Output('sucursal1_diferencia_captaciones_vs_colocaciones', 'children'),
    [Input('select_years', 'value'),
    Input('select_months', 'value')]
)

def update_text(select_years, select_months):
    if select_months is None:
        raise PreventUpdate
    else:

        # Crear df con la sucursal 'Oficina Central'
        df_1 = df[df['sucursal']=='Oficina Central']

        # Agrupar df con las columnas selleccionadas por dia
        df_2 = df_1.groupby(['Ano', 'Mes', 'Dia', 'movimiento'])['monto'].sum().reset_index()
      
        # Crear df de acuerdo al año y mes seleccionados
        df_3 = df_2[(df_2['Ano'] == select_years) & (df_2['Mes'] == select_months)]


        ### Colocaciones y Captaciones
        # query total colocaciones
        colocaciones = df_3.loc[df_3['movimiento'] == 'Colocaciones', 'monto'].sum()

        # query total captaciones
        captaciones = df_3.loc[df_3['movimiento'] == 'Captaciones', 'monto'].sum()

        # Diferencia de colocaciones con captaciones
        diferencia_movimiento = colocaciones - captaciones



        if diferencia_movimiento > 0:
            return[

                # Inicio Div Container
                html.Div([

                    html.P('Diferencia de Movimientos:' ,
                        style = {
                            'color':'#046e27',
                            'fontSize':12,
                            'font-weight':'bold',
                            'text-align':'center',
                            
                       }
                    ),

                    
                    html.P('Bs {0:,.0f}'.format(diferencia_movimiento),
                        style={
                            'color':'#00cc00',
                            'fontSize': 12,
                            'font-weight': 'bold',
                            'text-align':'center',
                            'margin-top': '-10px',
                            }
                    ),
                ])
            ]
        
        elif diferencia_movimiento < 0:
            return[

                # Inicio Div Container
                html.Div([

                    # Diferencia de Movimientos
                    html.P('Diferencia de Movimientos:',
                        style = {
                            'color':'#046e27',
                            'fontSize':12,
                            'font-weight':'bold',
                            'text-align':'center',
                            
                       }
                    ),

                    
                    html.P('Bs {0:,.0f}'.format(diferencia_movimiento),
                        style={
                            'color':'#EC1E3D',
                            'fontSize': 12,
                            'font-weight': 'bold',
                            'text-align':'center',
                            'margin-top': '-10px',
                            }
                    ),
                ])
            ]
        
#### FIN DE CALLBACK SUCURSAL 1 ####



### SUCURSAL 2 LA GUARDIA ###

# CB 1.2.1 LINE CHART La Guardia

@app.callback(
    Output('sucursal2_chart', 'figure'),
    [Input('select_years', 'value'),
    Input('select_months', 'value')]
)

def update_branch_chart(select_years, select_months):

    # Crear df con la sucursal 'La Guardia'
    df_1 = df[df['sucursal']=='La Guardia']

    # Agrupar df con las columnas selleccionadas
    df_2 = df_1.groupby(['Ano', 'Mes', 'Dia', 'movimiento'])['monto'].sum().reset_index()
      
    # Crear df de acuerdo al año y mes seleccionados
    df_3 = df_2[(df_2['Ano'] == select_years) & (df_2['Mes'] == select_months)]

    fig = px.line(
        df_3,
        x='Dia',
        y='monto',
        color='movimiento',
        #title='Oficina Central',
        markers=True,
        line_dash_sequence=None,
        symbol_sequence=None,
    )

    fig.update_layout(
        legend=dict(
            title_text='',
            orientation="h",
            entrywidth=50, 
            yanchor="bottom", 
            y=1.00, 
            xanchor="right", 
            x=1,
            font=dict(
                size=9
            )
        ),
        margin=dict(
            b=10,
            l=0,
            r=10,
            t=10,
        )
    )
    fig.update_xaxes(title_text='')
    fig.update_yaxes(title_text='')

    return fig


# CB 1.2.2 CALLBACK CAPTACIONES La Guardia
@app.callback(
    Output('sucursal2_diferencia_captaciones', 'children'),
    [Input('select_years', 'value'),
    Input('select_months', 'value')]
)

def update_text(select_years, select_months):
    if select_months is None:
        raise PreventUpdate
    else:

        # Crear df con la sucursal 'La Guardia'
        df_1 = df[df['sucursal']=='La Guardia']

        # Agrupar df con las columnas selleccionadas por dia
        df_2 = df_1.groupby(['Ano', 'Mes', 'Dia', 'movimiento'])['monto'].sum().reset_index()
      
        # Crear df de acuerdo al año y mes seleccionados
        df_3 = df_2[(df_2['Ano'] == select_years) & (df_2['Mes'] == select_months)]


        ### Total Captaciones
        # query total captaciones
        captaciones = df_3.loc[df_3['movimiento'] == 'Captaciones', 'monto'].sum()



        ### Calcular diferencia con el mes anterior ###
        # Agrupar df con las columnas selleccionadas por mes
        df_by_month = df_1.groupby(['Ano', 'Mes', 'movimiento'])['monto'].sum().reset_index()
        

        ### CAPTACIONES
        # df Diferencia captaciones con el mes anterior
        df_by_month_captaciones = df_by_month[(df_by_month['movimiento'] == 'Captaciones') & ('monto' in df_by_month.columns)].groupby(['Ano', 'Mes']).sum()   
        df_by_month_captaciones = df_by_month_captaciones.reset_index()

        # Crear columna que Calcula el la diferencia con el mes anterior en captaciones
        df_by_month_captaciones['diferencia_mes_anterior'] = df_by_month_captaciones['monto'].diff()

        ### Calcular cambio de porcentaje entre dos meses en captaciones
        df_by_month_captaciones['diferencia_pct'] = (df_by_month_captaciones['monto'].pct_change()) * 100

        # Filtrar captaciones por mes
        filter_month_captaciones = df_by_month_captaciones[(df_by_month_captaciones['Ano'] == select_years) & (df_by_month_captaciones['Mes'] == select_months)]

        # Diferencia del monto con el mes anterior filtrado
        captaciones_diferencia_monto_filtrado = filter_month_captaciones['diferencia_mes_anterior'].iloc[0]

        # Diferencia de porcentaje con el mes anterior filtrado
        captaciones_diferencia_pct_filtrado = filter_month_captaciones['diferencia_pct'].iloc[0]



        ### COLOCACIONES
        # df Diferencia colocaciones con el mes anterior
        df_by_month_colocaciones = df_by_month[(df_by_month['movimiento'] == 'Colocaciones') & ('monto' in df_by_month.columns)].groupby(['Ano', 'Mes']).sum()  
        df_by_month_colocaciones = df_by_month_colocaciones.reset_index()
      
        
        # Crear columna que Calcula el la diferencia con el mes anterior en colocaciones
        df_by_month_colocaciones['diferencia_mes_anterior'] = df_by_month_colocaciones['monto'].diff()

        ### Calcular cambio de porcentaje entre dos meses en colocaciones
        df_by_month_colocaciones['diferencia_pct'] = (df_by_month_colocaciones['monto'].pct_change()) * 100

        # Filtrar colocaciones por mes
        filter_month_colocaciones = df_by_month_colocaciones[(df_by_month_colocaciones['Ano'] == select_years) & (df_by_month_colocaciones['Mes'] == select_months)]


        # Diferencia del monto con el mes anterior filtrado
        colocaciones_diferencia_monto_filtrado = filter_month_colocaciones['diferencia_mes_anterior'].iloc[0]

        # Diferencia de porcentaje con el mes anterior filtrado
        colocaciones_diferencia_pct_filtrado = filter_month_colocaciones['diferencia_pct'].iloc[0]



        if captaciones_diferencia_monto_filtrado > 0:
            return [
                # Inicio Div Container
                html.Div([

                    # Total Captaciones Mes TEXT
                    html.P('Total Captaciones Mes:',
                        style = {
                                'color':'#046e27',
                                'fontSize':13,
                                'font-weight':'bold',  
                                'text-align':'center',  
                        }
                    ),

                    html.Div([
                        # Total Captaciones MONTO
                        html.Div([
                            html.P('Bs {0:,.0f}'.format(captaciones),
                                style={
                                    'color': '#000000',
                                    'fontSize': 13,
                                    'font-weight':'bold',
                                    'text-align':'center',
                                })
                        ]),
                        # Green Arrow up
                        html.Div([
                            html.I(className = "fas fa-caret-up",
                                style = {"font-size": "25px",
                                        'color': '#00cc00'},
                           ),
                        ], className = 'value_indicator'),
                    ], className = 'value_and_indicator'),

                    # VS mes anterior text
                    html.Div([
                        html.P('vs mes anterior:',
                               style = {
                                   'color':'#333333',
                                   'fontSize':12,
                                   'font-weight':'bold',
                                   'text-align':'center',
                               }
                        )
                    ], className = 'vs_mes_anterior'),

                    # Div ROW holder for monto diferencia en captaciones y pct en captaciones
                    html.Div([
                        # Div holder for monto diferencia en captaciones
                        html.Div([
                            html.P('Bs {0:,.2f}'.format(captaciones_diferencia_monto_filtrado),
                                   style={
                                       'color': '#00cc00',
                                       'fontSize': 12,
                                   }
                            )
                        ], className='monthly_difference_value'),
                        # Div holder for monto porcentaje en captaciones
                        html.Div([
                            html.P('{0:,.1f}%'.format(captaciones_diferencia_pct_filtrado),
                                    style={
                                       'color': '#00cc00',
                                       'fontSize': 12,
                                   }
                            ),    
                        ],className='monthly_difference_value'),
                    ], className='difference_value_row'),

                # FIN DEL DIV Container
                ]),

            ]
        elif captaciones_diferencia_monto_filtrado < 0:
            return [
                # Inicio Div Container
                html.Div([
                    # Total Captaciones Mes TEXT
                    html.P('Total Captaciones Mes:',
                        style = {
                                'color':'#046e27',
                                'fontSize':13,
                                'font-weight':'bold',  
                                'text-align':'center',  
                        }
                    ),

                    html.Div([
                        # Total Captaciones MONTO
                        html.Div([
                            html.P('Bs {0:,.0f}'.format(captaciones),
                                style={
                                    'color': '#000000',
                                    'fontSize': 13,
                                    'font-weight':'bold',
                                    'text-align':'center',
                                })
                        ]),
                        # Red Arrow Down
                        html.Div([
                            html.I(className = "fas fa-caret-down",
                                style = {"font-size": "25px",
                                        'color': '#EC1E3D'},
                           ),
                        ], className = 'value_indicator'),
                    ], className = 'value_and_indicator'),

                    # Vs Mes anterior
                    html.Div([
                        html.P('vs mes anterior:',
                               style = {
                                   'color':'#333333',
                                   'fontSize':12,
                                   'font-weight':'bold',
                                   'text-align':'center',
                               }
                        )
                    ], className = 'vs_mes_anterior'),

                    # Div ROW holder for monto diferencia en captaciones y pct en captaciones
                    html.Div([
                        # Div holder for monto diferencia en captaciones
                        html.Div([
                            html.P('Bs {0:,.2f}'.format(captaciones_diferencia_monto_filtrado),
                                   style={
                                       'color': '#EC1E3D',
                                       'fontSize': 12,
                                   }
                            )
                        ], className='monthly_difference_value'),
                        # Div holder for monto porcentaje en captaciones
                        html.Div([
                            html.P('{0:,.1f}%'.format(captaciones_diferencia_pct_filtrado),
                                    style={
                                       'color': '#EC1E3D',
                                       'fontSize': 12,
                                   }
                            ),    
                        ],className='monthly_difference_value'),
                    ], className='difference_value_row'),

                # FIN DEL DIV Container
                ]),

            ]



### CB 1.2.3 CALLBACK COLOCACIONES La Guardia
@app.callback(
    Output('sucursal2_diferencia_colocaciones', 'children'),
    [Input('select_years', 'value'),
    Input('select_months', 'value')]
)

def update_text(select_years, select_months):
    if select_months is None:
        raise PreventUpdate
    else:

        # Crear df con la sucursal 'La Guardia'
        df_1 = df[df['sucursal']=='La Guardia']

        # Agrupar df con las columnas selleccionadas por dia
        df_2 = df_1.groupby(['Ano', 'Mes', 'Dia', 'movimiento'])['monto'].sum().reset_index()
      
        # Crear df de acuerdo al año y mes seleccionados
        df_3 = df_2[(df_2['Ano'] == select_years) & (df_2['Mes'] == select_months)]

        ### Colocaciones y Captaciones
        # query total colocaciones
        colocaciones = df_3.loc[df_3['movimiento'] == 'Colocaciones', 'monto'].sum()

        # query total captaciones
        captaciones = df_3.loc[df_3['movimiento'] == 'Captaciones', 'monto'].sum()

        # Diferencia de colocaciones con captaciones
        diferencia_movimiento = colocaciones - captaciones

        ### Calcular diferencia con el mes anterior ###
        # Agrupar df con las columnas selleccionadas por mes
        df_by_month = df_1.groupby(['Ano', 'Mes', 'movimiento'])['monto'].sum().reset_index()
 


        ### COLOCACIONES
        # df Diferencia colocaciones con el mes anterior
        df_by_month_colocaciones = df_by_month[(df_by_month['movimiento'] == 'Colocaciones') & ('monto' in df_by_month.columns)].groupby(['Ano', 'Mes']).sum()  
        df_by_month_colocaciones = df_by_month_colocaciones.reset_index()
      
        
        # Crear columna que Calcula el la diferencia con el mes anterior en colocaciones
        df_by_month_colocaciones['diferencia_mes_anterior'] = df_by_month_colocaciones['monto'].diff()

        ### Calcular cambio de porcentaje entre dos meses en colocaciones
        df_by_month_colocaciones['diferencia_pct'] = (df_by_month_colocaciones['monto'].pct_change()) * 100

        # Filtrar colocaciones por mes
        filter_month_colocaciones = df_by_month_colocaciones[(df_by_month_colocaciones['Ano'] == select_years) & (df_by_month_colocaciones['Mes'] == select_months)]


        # Diferencia del monto con el mes anterior filtrado
        colocaciones_diferencia_monto_filtrado = filter_month_colocaciones['diferencia_mes_anterior'].iloc[0]

        # Diferencia de porcentaje con el mes anterior filtrado
        colocaciones_diferencia_pct_filtrado = filter_month_colocaciones['diferencia_pct'].iloc[0]



        if colocaciones_diferencia_monto_filtrado > 0:
            return [
                html.Div([

                    # Total Colocaciones Mes TEXT
                    html.P('Total Colocaciones Mes:',
                        style = {
                                'color':'#046e27',
                                'fontSize':13,
                                'font-weight':'bold',  
                                'text-align':'center',  
                        }
                    ),

                    html.Div([
                        # Total Colocaciones MONTO
                        html.Div([
                            html.P('Bs {0:,.0f}'.format(colocaciones),
                                style={
                                    'color': '#000000',
                                    'fontSize': 13,
                                    'font-weight':'bold',
                                    'text-align':'center',
                                })
                        ]),
                        # Green Arrow up
                        html.Div([
                            html.I(className = "fas fa-caret-up",
                                style = {"font-size": "25px",
                                        'color': '#00cc00'},
                           ),
                        ], className = 'value_indicator'),
                    ], className = 'value_and_indicator'),

                    # VS mes anterior text
                    html.Div([
                        html.P('vs mes anterior:',
                               style = {
                                   'color':'#333333',
                                   'fontSize':12,
                                   'font-weight':'bold',
                                   'text-align':'center',

                               }   )
                    ], className = 'vs_mes_anterior'),

                    # Div ROW holder for monto diferencia en captaciones y pct en captaciones
                    html.Div([
                        # Div holder for monto diferencia en captaciones
                        html.Div([
                            html.P('Bs {0:,.2f}'.format(colocaciones_diferencia_monto_filtrado),
                                   style={
                                       'color': '#00cc00',
                                       'fontSize': 12,
                                   }
                            )
                        ], className='monthly_difference_value'),
                        # Div holder for monto porcentaje en captaciones
                        html.Div([
                            html.P('{0:,.1f}%'.format(colocaciones_diferencia_pct_filtrado),
                                    style={
                                       'color': '#00cc00',
                                       'fontSize': 12,
                                   }
                            ),    
                        ],className='monthly_difference_value'),
                    ], className='difference_value_row'),
            
                # FIN DEL DIV
                ]),
            ]
        elif colocaciones_diferencia_monto_filtrado < 0:
            return [
                html.Div([

                    # Total Colocaciones Mes TEXT
                    html.P('Total Colocaciones Mes:',
                        style = {
                                'color':'#046e27',
                                'fontSize':13,
                                'font-weight':'bold',  
                                'text-align':'center',  
                        }
                    ),

                    html.Div([
                        # Total Colocaciones MONTO
                        html.Div([
                            html.P('Bs {0:,.0f}'.format(colocaciones),
                                style={
                                    'color': '#000000',
                                    'fontSize': 13,
                                    'font-weight':'bold',
                                    'text-align':'center',
                                })
                        ]),
                        # Red Arrow Down
                        html.Div([
                            html.I(className = "fas fa-caret-down",
                                style = {"font-size": "25px",
                                        'color': '#EC1E3D'},
                           ),
                        ], className = 'value_indicator'),
                    ], className = 'value_and_indicator'),


                    # Vs Mes anterior
                    html.Div([
                        html.P('vs mes anterior:',
                               style = {
                                   'color':'#333333',
                                   'fontSize':12,
                                   'font-weight':'bold',
                                   'text-align':'center',

                               }   )
                    ], className = 'vs_mes_anterior'),

                    # Div ROW holder for monto diferencia en captaciones y pct en captaciones
                    html.Div([
                        # Div holder for monto diferencia en captaciones
                        html.Div([
                            html.P('Bs {0:,.2f}'.format(colocaciones_diferencia_monto_filtrado),
                                   style={
                                       'color': '#EC1E3D',
                                       'fontSize': 12,
                                   }
                            )
                        ], className='monthly_difference_value'),
                        # Div holder for monto porcentaje en captaciones
                        html.Div([
                            html.P('{0:,.1f}%'.format(colocaciones_diferencia_pct_filtrado),
                                    style={
                                       'color': '#EC1E3D',
                                       'fontSize': 12,
                                   }
                            ),    
                        ],className='monthly_difference_value'),
                    ], className='difference_value_row'),
            
                # FIN DEL DIV
                ]),
            ]
    

### CB 1.2.4 CALLBACK DIFERENCIA COLOCACIONES VS CAPTACIONES - La Guardia
@app.callback(
    Output('sucursal2_diferencia_captaciones_vs_colocaciones', 'children'),
    [Input('select_years', 'value'),
    Input('select_months', 'value')]
)

def update_text(select_years, select_months):
    if select_months is None:
        raise PreventUpdate
    else:

        # Crear df con la sucursal 'La Guardia'
        df_1 = df[df['sucursal']=='La Guardia']

        # Agrupar df con las columnas selleccionadas por dia
        df_2 = df_1.groupby(['Ano', 'Mes', 'Dia', 'movimiento'])['monto'].sum().reset_index()
      
        # Crear df de acuerdo al año y mes seleccionados
        df_3 = df_2[(df_2['Ano'] == select_years) & (df_2['Mes'] == select_months)]


        ### Colocaciones y Captaciones
        # query total colocaciones
        colocaciones = df_3.loc[df_3['movimiento'] == 'Colocaciones', 'monto'].sum()

        # query total captaciones
        captaciones = df_3.loc[df_3['movimiento'] == 'Captaciones', 'monto'].sum()

        # Diferencia de colocaciones con captaciones
        diferencia_movimiento = colocaciones - captaciones



        if diferencia_movimiento > 0:
            return[

                # Inicio Div Container
                html.Div([

                    html.P('Diferencia de Movimientos:' ,
                        style = {
                            'color':'#046e27',
                            'fontSize':12,
                            'font-weight':'bold',
                            'text-align':'center',
                            
                       }
                    ),

                    
                    html.P('Bs {0:,.0f}'.format(diferencia_movimiento),
                        style={
                            'color':'#00cc00',
                            'fontSize': 12,
                            'font-weight': 'bold',
                            'text-align':'center',
                            'margin-top': '-10px',
                            }
                    ),
                ])
            ]
        
        elif diferencia_movimiento < 0:
            return[

                # Inicio Div Container
                html.Div([

                    # Diferencia de Movimientos
                    html.P('Diferencia de Movimientos:',
                        style = {
                            'color':'#046e27',
                            'fontSize':12,
                            'font-weight':'bold',
                            'text-align':'center',
                            
                       }
                    ),

                    
                    html.P('Bs {0:,.0f}'.format(diferencia_movimiento),
                        style={
                            'color':'#EC1E3D',
                            'fontSize': 12,
                            'font-weight': 'bold',
                            'text-align':'center',
                            'margin-top': '-10px',
                            }
                    ),
                ])
            ]
        
#### FIN DE CALLBACK SUCURSAL 2 ####





#### FIN DE CALLBACK SUCURSALES ####



# CB 2.1 LINE CHARTS FOR SUCURSALES

@app.callback(
    Output('sucursales_charts', 'figure'),
    [Input('sucursal_dropdown', 'value'),
    Input('movimiento_dropdown', 'value'),
    Input('tipo_de_movimiento_dropdown', 'value'),
    Input('select_years', 'value'),
    Input('select_months', 'value')]
)

def update_line_charts(sucursal_dropdown, movimiento_dropdown, tipo_de_movimiento_dropdown, select_years, select_months):
    
    
    df_sucursal= df[df['sucursal']==sucursal_dropdown]

    df_1 = df_sucursal.groupby(['Ano', 'Mes', 'Dia', 'movimiento', 'tipo_de_movimiento'])['monto'].sum().reset_index()
    df_2 = df_1[(df_1['Ano'] == select_years) & (df_1['Mes'] == select_months)]

    df_3 = df_2[(df_2['movimiento'] == movimiento_dropdown) & (df_2['tipo_de_movimiento'] == tipo_de_movimiento_dropdown)]

    fig = px.line(
        df_3,
        x='Dia',
        y='monto',
        title = 'sucursal'
    )

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)