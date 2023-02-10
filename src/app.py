#Importar librerías
import dash
import pandas as pd
# from dash_html_components as html
import plotly.graph_objs as go
from dash import dcc
from dash import html
from dash.dependencies import Input, Output


app = dash.Dash()
server=app.server

# CARGA DE DATOS
df_sp500 = pd.read_excel(r'bdmanananerasfinal.xlsx')

# DEFINICIÓN LAYOUT
app.layout = html.Div([
                    html.Div([
                    html.Label('Selección'),
                    dcc.Dropdown(id='selector',
                        options=[
                            {'label': 'Número de Visualizaciones', 'value': 'viewCount'},
                            {'label': 'Número de Likes', 'value': 'likeCount'},

                        ],
                        value='viewCount',
                        clearable=True)
                    ],style={'width': '48%', 'display': 'inline-block'}),

                    html.Div([
                    html.Label('Rango fechas'),
                    dcc.DatePickerRange(id='selector_fecha',
                                        start_date=df_sp500["publishedAt"].min(),
                                        end_date=df_sp500["publishedAt"].max(),
                                        clearable=False),
                    ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),

                    dcc.Graph(id='lineplot'),

                    dcc.Graph(id='barplot')])

# CREACIÓN DE GRÁFICOS E INTERACTIVIDAD
#Callback para actualizar gráfico de cotización en función del dropdown eligiendo apertura o cierre de sesión y según selector de fechas
@app.callback(Output('lineplot', 'figure'),
              [Input('selector_fecha', 'start_date'),
               Input('selector_fecha', 'end_date'),
               Input('selector', 'value')])
def actualizar_graph_line(fecha_min, fecha_max, seleccion):
    filtered_df = df_sp500[(df_sp500["publishedAt"]>=fecha_min) & (df_sp500["publishedAt"]<=fecha_max)]

    if seleccion == "viewCount":
        return{
            'data': [go.Scatter(x=filtered_df["publishedAt"],
                                y=filtered_df["viewCount"],
                                mode='lines',
                                text= df_sp500['videoTitle'],
                                line=dict(color='#621132',width=1),
                                marker=dict(size=3),
                                )],
            'layout': go.Layout(
                title="Mañaneras",
                xaxis={'title': " "},
                yaxis={'title': "Visualizaciones"},
                hovermode='closest',
                height=500,
            )}

    else:
        return{
            'data': [go.Scatter(x=filtered_df["publishedAt"],
                                y=filtered_df["likeCount"],
                                mode="lines",
                                text=df_sp500['videoTitle'],
                                line=dict(color='#13322B',width=1))],

            'layout': go.Layout(
                title="Mañaneras",
                xaxis={'title': " "},
                yaxis={'title': "Likes"},
                hovermode='closest'
                )
    }

#Callback para actualizar gráfico de volumen según selector de fechas
@app.callback(Output('barplot', 'figure'),
              [Input('selector_fecha', 'start_date'),Input('selector_fecha', 'end_date')])
def actualizar_graph_bar(fecha_min, fecha_max):
    filtered_df = df_sp500[(df_sp500["publishedAt"]>=fecha_min) & (df_sp500["publishedAt"]<=fecha_max)]
    return{
        'data': [go.Bar(x=filtered_df["publishedAt"],
                        y=filtered_df["commentCount"],
                        base='text',
                        text=df_sp500['videoTitle'],
                        marker=dict(color='#285C4D'))],

        'layout': go.Layout(title="Número de comentarios",
                        xaxis=dict(title=" "),

                        yaxis=dict(title="Comentarios",
                        hoverformat='closest',
                        ))
            }

#Sentencias para abrir el servidor al ejecutar este script
if __name__ == '__main__':
    app.run_server(debug=True)
