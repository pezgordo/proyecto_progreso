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

app = dash.Dash(
    meta_tags=[
        {"name":"viewport", "content":"width=device-width, initial-scale=1"}
    ]
)

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
    
    # Div 2 Begins
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
    ,className='container column offset-by-one'),
    # Div 2 Ends

    # Div 3 Begins
    html.Div([

        # Div 3.1 Begins Sucursal dropdown
        html.Div([
            dcc.Dropdown(
                id='sucursal_dropdown',
                options = df['sucursal'],
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

    # Div 3 Ends
    ]),

    # Div 4 Begins
    html.Div([

        # Div 4.1 Graph
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

# Main Div endss
#],  className='container')
],)

# END OF HTML


# *** CALLBACKS *** CALLBACKS *** CALLBACKS ***

# CB 1.1 LINE CHARTS FOR SUCURSALES
@app.callback(
    Output('sucursales_charts', 'figure'),
    Input('sucursal_dropdown', 'value'),
    Input('movimiento_dropdown', 'value'),
    Input('tipo_de_movimiento_dropdown', 'value'),
    Input('select_years', 'value'),
    Input('select_months', 'value'),
)

def update_line_charts(sucursal_dropdown, movimiento_dropdown, tipo_de_movimiento_dropdown, select_years, select_months):
    
    df_sucursal= df[(df['sucursal']==sucursal_dropdown)]
    #df_1= df[(df['sucursal']==sucursal_dropdown)]
    #df_1 = df_sucursal.groupby(['Ano', 'Mes', 'Dia'])['monto'].sum().reset_index()
    df_1 = df_sucursal.groupby(['Ano', 'Mes', 'Dia', 'movimiento', 'tipo_de_movimiento'])['monto'].sum().reset_index()
    df_2 = df_1[(df_1['Ano'] == select_years) & (df_1['Mes'] == select_months)]
    #df_2 = df_1[(df_1['Ano'] == select_years)]
    df_3 = df_2[(df_2['movimiento'] == movimiento_dropdown) & (df_2['tipo_de_movimiento'] == tipo_de_movimiento_dropdown)]

    #for sucursales in df_sucursal:
    #    sucursal_chart=px.line(
    #                x = 'fecha',
    #                y = 'monto',
    #                title = f'{sucursales} Sucursal',
    #)

    fig = px.line(
        df_3,
        x='Dia',
        y='monto',
        title = 'sucursal'
    )

    return fig




if __name__ == '__main__':
    app.run_server(debug=True)