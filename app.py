# ----------------------------------Structure--------------------------------- #

# -*- coding: utf-8 -*-

from dash import Dash, dcc, html, Input, Output
import os
import pandas as pd
import plotly.express as px



# ---------------------------Logica de los datos--------------------------------- #

#Selección de los datos
df = pd.read_csv('https://media.githubusercontent.com/media/JorgeHdzRiv/Defunciones-en-Guanajuato-y-Municipios/main/data/mortalidad/conjunto_de_datos/evmor_11_valor.csv')

# Filtro para datos municipio y defunciones generales
df_mun = df[(df['cve_municipio'] != 0) & (df['cve_municipio'] != 996)]

df_mun_g = df_mun[(df_mun['id_indicador'] == 1002000030)]

df_mun_h = df_mun[(df_mun['id_indicador'] == 1002000031)]

df_mun_m = df_mun[(df_mun['id_indicador'] == 1002000032)]

# Nueva linea de prueba

# Probando filtro nuevo para defunciones en cada municipio
df_mun_all = df_mun[(df_mun['id_indicador'] >= 1002000030) & (df_mun['id_indicador'] <= 1002000038)]

#Variables
available_indicators = df_mun_all['indicador'].unique()
available_indicadores = df_mun_all['indicador'].unique()
available_municipios = df_mun_all['desc_municipio'].unique()

#Scatter plot sencilla para ejemplo
fig = px.scatter(df_mun_g, x="año", y="valor")
#fig.show()

# Line charts sencilla para ejemplo
fig_line = px.line(df_mun_g, x="año", y="valor", title='Defunciones en los municipios de Guanajuato', color='desc_municipio')
#fig_line.show()

# -------------------------- App-------------------------------------- #

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)#, external_stylesheets=external_stylesheets)

#Linea para app.py
server = app.server

app.layout = html.Div(children=[
    html.H1(children='Defunciones en el estado de Guanajuato'), 
  
    html.H2(children= 'Defunciones generales'),

    html.H3(children= 'Scatter de defunciones'),

    html.Div(children='''
        Facilmente podemos observar las defunciones generales
        a lo largo del tiempo en el estado de Guanajuato.
    '''),

    html.Div(children='''
        Respondiendo a la pregunta:
        Cual es el año con mas registros de defunciones?
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    ),

    # Grafica circular de defunciones en general con deslizador
    html.H3(children= 'Grafica circular de defunciones a lo largo del tiempo en cada municipio'),

     html.Div(children='''
         Se puede observar a lo largo de un deslizador de tiempo la variacion y el porcentaje 
         de cada Municipio en defunciones generales.
    '''),

    dcc.Graph(id='pie-with-slider'),
    
    dcc.Slider(
        id='year-slider',
        min=df_mun_g['año'].min(),
        max=df_mun_g['año'].max(),
        value=df_mun_g['año'].min(),
        marks={str(año): str(año) for año in df_mun_g['año'].unique()},
        step=None
    ),

    html.H2(children='Subdivisión por municipios'),

    # Grafica lineal sobre el tiempo
    html.H3(children='Grafica linear por municipio a lo largo del tiempo'),

    html.Div(children='''
         Aqui podemos responder una de las preguntas iniciales:
         Que municipio tiene mas defunciones?

    '''),

    
    dcc.Graph(
        id='example-graph2',
        figure=fig_line
    ),

    #Implementacion grafica circular
    html.H3(children='Grafica circular de categorias por municipio a lo largo del tiempo'),

    html.Div(children='''
         Aqui podemos observar la variacion de defunciones por categoria del Dataset:
    '''),

    html.Div([

        html.Div([
            dcc.Dropdown(
                id='indicator',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Defunciones generales'
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),
    ]),

    dcc.Graph(id='indicator-graphic'),

    dcc.Slider(
        id='year--slider',
        min=df_mun_all['año'].min(),
        max=df_mun_all['año'].max(),
        value=df_mun_all['año'].max(),
        marks={str(year): str(year) for year in df_mun_all['año'].unique()},
        step=None
    ),

    #Implementacion de grafica de barras
    html.H3(children='Grafica de barras por categorias y por municipio a lo largo del tiempo'),

    html.Div(children='''
         Aqui podemos observar la variacion de defunciones por categoria y municipio
         del Dataset de una manera individual para un mejor analisis
    '''),

    html.Div([

        html.Div([
            dcc.Dropdown(
                id='indicador',
                options=[{'label': i, 'value': i} for i in available_indicadores],
                value='Defunciones generales'
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='municipio',
                options=[{'label': i, 'value': i} for i in available_municipios],
                value='Abasolo'
            )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='bar-graphic'),

    # Descarga del mapa
    html.H3(children='Descarga del mapa interactivo de defunciones generales'),

    html.Div(children='''
         Probado en Google Chrome, Firefox y Microsoft Edge
    '''),

    html.Button("Descargar Mapa", id="btn_map"),
    dcc.Download(id="download-map"),

    # Redes sociales
    html.H3(children='Redes sociales'),

    html.Div(children='''
         Este proyecto seguira en constante cambio y mejoras te invito a visitar
         mis redes
    '''),

    html.A(html.Button('Repositorio Proyecto', className='three columns'),
    href='https://github.com/JorgeHdzRiv/Defunciones-en-Guanajuato-y-Municipios', target="_blank"),

    html.A(html.Button('Github', className='three columns'),
    href='https://github.com/JorgeHdzRiv', target="_blank"),

    html.A(html.Button('Linkedin', className='three columns'),
    href='https://www.linkedin.com/in/jorhdzriv/', target="_blank")

], style={'background-color': '#FFF0B1'})

# ---------------------------------------Callbacks -------------------------- #

@app.callback(
    Output('pie-with-slider', 'figure'),
    Input('year-slider', 'value'))

def update_figure(selected_year):
    filtered_df = df_mun_g[df_mun_g.año == selected_year]

    filtered_df.loc[filtered_df['valor'] < 200, 'desc_municipio'] = 'Otros' # Represent only large countries
    fig = px.pie(filtered_df, values='valor', names='desc_municipio', title='Defunciones en general en el estado de guanajuato')                

    fig.update_layout(transition_duration=500)

    return fig

@app.callback(
    Output('indicator-graphic', 'figure'),
    Input('indicator', 'value'),
    Input('year--slider', 'value'))

def update_graph(xaxis_column_name,selected_year):

    # Aquí filtramos por año
    filtered_df = df_mun_all[df_mun_all.año == selected_year]

    # Aquí hacemos el scatter
    #filtered_df.loc[filtered_df['valor'] < 200, 'desc_municipio'] = 'Otros' # Represent only large countries

    fig = px.pie(filtered_df, values=filtered_df[filtered_df['indicador']== xaxis_column_name]['valor'],
                 names=filtered_df[filtered_df['indicador']== xaxis_column_name]['desc_municipio'], title='Defunciones en el estado de guanajuato por categoria')                

    fig.update_layout(transition_duration=500)

    
    return fig

@app.callback(
    Output('bar-graphic', 'figure'),
    Input('indicador', 'value'),
    Input('municipio', 'value'))

def update_grafico(indicador,municipio):
    #Filtrado por municipio
    filtro = df_mun_all[(df_mun_all['indicador'] == indicador)]
    filtro_final = filtro[(filtro['desc_municipio'] == municipio)]
    
    # Grafica de barras
    fig = px.bar(filtro_final, x='año', 
                 y='valor')
    
    # Aquí se actualiza la gráfica con los datos filtrados
    fig.update_layout(transition_duration=500)
    
    return fig

@app.callback(
    Output("download-map", "data"),
    Input("btn_map", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_file(
        "./file/kepler_map.html"
    )

if __name__ == '__main__':
    app.run_server(debug=True)
    
