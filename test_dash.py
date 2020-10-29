import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import json


# CARICAMENTO DEL FOGLIO DI STILE ESTERNO
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# CONFIGGURAZIONE DELLA APP DASH
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# per creare il server
# server = app.server

# dati = pd.read_csv('dpc-covid19-ita-andamento-nazionale.csv')

# URL dei dati aggiornati giornalmente
url = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv'

# Lettura dei dati dall'url
dati = pd.read_csv(url, error_bad_lines=False)

# Salvataggio dei dati in locale
dati.to_csv('dpc-covid19-ita-andamento-nazionale.csv')

url = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv'
dati_regioni = pd.read_csv(url, error_bad_lines=False)
dati_regioni.to_csv('dpc-covid19-ita-regioni.csv')

regioni = json.load(open('regioni.geojson','r'))

etichette = {
    'terapia_intensiva' : 'Terapia Intensiva',
    'totale_ospedalizzati' : 'Totale Ospedalizzati',
    'nuovi_positivi' : 'Nuovi Positivi',
    'totale_positivi' : 'Totale Positivi',
    'variazione_totale_positivi' : 'Variazione Totale Positivi',
    'deceduti' : 'Deceduti',
    'ricoverati_con_sintomi' : 'Ricoverati con sintomi',
    'isolamento_domiciliare' : 'Isolamento domiciliare',
    'dimessi_guariti' : 'Dimessi guariti',
    'casi_da_sospetto_diagnostico' : 'Casi da sospetto diagnostico',
    'casi_da_screening' : 'Casi da screening',
    'totale_casi' : 'Totale Casi',
    'tamponi' : 'Tamponi',
    'casi_testati' : 'Casi testati',
}

scelte=[
    {'label': 'Terapie Intensive', 'value': 'terapia_intensiva'},
    {'label': 'Ricoverati con sintomi', 'value': 'ricoverati_con_sintomi'},
    {'label': 'Totale Ospedalizzati', 'value': 'totale_ospedalizzati'},
    {'label': 'Isolamento domiciliare', 'value': 'isolamento_domiciliare'},
    {'label': 'Nuovi Positivi', 'value': 'nuovi_positivi'},
    {'label': 'Totale Positivi', 'value': 'totale_positivi'},
    {'label': 'Variazione Totale Positivi', 'value': 'variazione_totale_positivi'},
    {'label': 'Deceduti', 'value': 'deceduti'},
    {'label': 'Dimessi guariti', 'value': 'dimessi_guariti'},
    {'label': 'Casi da sospetto diagnostico', 'value': 'casi_da_sospetto_diagnostico'},
    {'label': 'Casi da screening', 'value': 'casi_da_screening'},
    {'label': 'Totale Casi', 'value': 'totale_casi'},
    {'label': 'Tamponi', 'value': 'tamponi'},
    {'label': 'Casi testati', 'value': 'casi_testati'},
]

# Estrazione delle date dal DataFrame per le etichette dello slider
marks_date = {}
giorni = []
for index, data in enumerate(dati.data):
    if index % 10 == 0:
        giorno = data.split('T')[0].split('-')
        giorni.append(giorno[2] + '/' + giorno[1] + '/' + giorno[0])
        marks_date[index] = giorno[2] + '/' + giorno[1] + '/' + giorno[0]

giorno = dati.data.tail(1)
# data_ultimo_aggiornamento = giorno[2] + '/' + giorno[1] + '/' + giorno[0]

# Generzione delle etichette per gli slider della stima
marks_range = {}

valori = np.arange(-5,1)

for valore in valori:
    marks_range[valore]=str(valore)

marks_previsione = {}

for i in range(1,61):
    marks_previsione[i]=str(i)

### LAYOUT DELLA APP

app.layout = html.Div(children=[
    html.H1(children='Visualizzazione e analisi dei dati Covid 19'),
    # html.H2(children='Dati aggiornati al ' + giorni[-1]),
    dcc.Tabs([
        dcc.Tab(label='Visualizzazione dati', children=[

            dcc.Dropdown(
                id='selettore_andamento',
                options=scelte,
                value='terapia_intensiva',
                clearable=False

            ),

            dcc.Graph(
                id='grafico_andamento'
            ),

            dcc.RangeSlider(
                id='slider_periodo',
                min=0,
                max=dati.shape[0],
                step=1,
                value=[0,dati.shape[0]],
                marks = marks_date
            ),
        ]),

        dcc.Tab(label='Stima dati', children=[

            dcc.Dropdown(
                id='selettore_stima',
                options=scelte,
                value='terapia_intensiva',
                clearable=False

            ),

            dcc.Graph(
                id='grafico_stima'
            ),

            dcc.RangeSlider(
                id='slider_periodo_stima',
                min=-30,
                max=0,
                step=1,
                value=[-10,0],
                marks = {
                    -30 : '-30',
                    -29 : '-29',
                    -28 : '-28',
                    -27 : '-27',
                    -26 : '-26',
                    -25 : '-25',
                    -24 : '-24',
                    -23 : '-23',
                    -22 : '-22',
                    -21 : '-21',
                    -20 : '-20',
                    -19 : '-19',
                    -18 : '-18',
                    -17 : '-17',
                    -16 : '-16',
                    -15 : '-15',
                    -14 : '-14',
                    -13 : '-13',
                    -12 : '12',
                    -11 : '-11',
                    -10 : '-10',
                    -9 : '-9',
                    -8 : '-8',
                    -7 : '-7',
                    -6 : '-6',
                    -5 : '-5',
                    -4 : '-4',
                    -3 : '-3',
                    -2 : '-2',
                    -1 : '-1',
                    0 : '0',
                }
            ),
            dcc.Slider(
                id='slider_periodo_previsione',
                min=1,
                max=60,
                step=1,
                value=20,
                marks = marks_previsione
            ),
        ]),
        dcc.Tab(label='Regioni ', children=[
            dcc.Dropdown(
                id='selettore_andamento_regioni',
                options=scelte,
                value='terapia_intensiva',
                clearable=False
            ),

            html.Br(),

            dcc.Slider(
                id='slider_periodo_regioni',
                min=0,
                max=dati.shape[0]-1,
                step=1,
                value=dati.shape[0]-1,
                marks = marks_date
            ),

            dcc.Graph(
                id='grafico_regioni'
            ),

        ]),

    ])
])

@app.callback(
    [
        Output(component_id='grafico_andamento', component_property='figure'),
        Output(component_id='grafico_stima', component_property='figure'),
        Output(component_id='grafico_regioni', component_property='figure'),
    ],
    [
        Input(component_id='selettore_andamento', component_property='value'),
        Input(component_id='slider_periodo', component_property='value'),
        Input(component_id='selettore_stima', component_property='value'),
        Input(component_id='slider_periodo_stima', component_property='value'),
        Input(component_id='slider_periodo_previsione', component_property='value'),
        Input(component_id='selettore_andamento_regioni', component_property='value'),
        Input(component_id='slider_periodo_regioni', component_property='value'),
    ]
)

def update_figure(dato_grafico, date, dato_stima, range_stima, previsione, dato_regioni, data_regione):
    dati_grafico = dati[date[0]:date[1]+1]
    fig_andamento = px.bar(dati_grafico, x="data", y=dato_grafico)

    y = dati[dato_stima][range_stima[0]:range_stima[1]] if range_stima[1]<0 else dati[dato_stima][range_stima[0]:]
    # y = dati[dato_stima][range_stima[0]:]
    x = np.arange(range_stima[0]+1,1+range_stima[1]) if range_stima[1]<0 else np.arange(range_stima[0]+1,1)
    # x = np.arange(range_stima[0]+1,1)
    [a, b], res1 = curve_fit(lambda x1,a,b: a*np.exp(b*x1),  x,  y)
    y = dati[dato_stima][range_stima[0]:]
    x = np.arange(range_stima[0]+1,1)
    fig_stima = go.Figure()
    fig_stima.add_trace(go.Scatter(x=x, y=y,
                    mode='markers',
                    name='Dati attuali'))

    # y1 = a * np.exp(b * x)
    # y = dati[dato_stima][-N:]
    x = np.arange(range_stima[0]+1,previsione+1)
    y1 = a * np.exp(b * x)

    fig_stima.add_trace(go.Scatter(x=x, y=y1,
                    mode='lines',
                    name='Stima'))

    fig_stima.update_layout(height=800)


    # grafico regioni


    dati_ridotti_regioni = dati_regioni.loc[dati_regioni.data == dati.data[data_regione]]
    
    dati_ridotti_regioni = dati_ridotti_regioni[['denominazione_regione', dato_regioni]]

    data = {'denominazione_regione':  ['Trentino-Alto Adige'],
        dato_regioni: [(dati_ridotti_regioni.loc[dati_ridotti_regioni.denominazione_regione == 'P.A. Bolzano', dato_regioni].item()
        + dati_ridotti_regioni.loc[dati_ridotti_regioni.denominazione_regione == 'P.A. Trento', dato_regioni]).item()],
        }

    df = pd.DataFrame (data, columns = ['denominazione_regione',dato_regioni])

    dati_ridotti_regioni = dati_ridotti_regioni.append(df)

    fig_regioni = px.choropleth(dati_ridotti_regioni, geojson=regioni, color=dato_regioni,
                        locations="denominazione_regione", featureidkey="properties.NOME_REG",
                        center = {'lat' : 41.9109,
                                'lon' : 12.4818},
                        scope="europe",
                        color_continuous_scale="Viridis",
                        projection="mercator",
                        # width=1200,
                        height=900,
                        title = etichette[dato_regioni] + ' del ' + dati.data[data_regione]
                    )

    fig_regioni.update_layout(width=900)
    fig_regioni.update_geos(fitbounds="locations", visible=False)

    return (fig_andamento, fig_stima, fig_regioni)


if __name__ == '__main__':
    # app.run_server(debug=False, host = '0.0.0.0')
    app.run_server(debug=True)