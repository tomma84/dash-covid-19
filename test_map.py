import json
import plotly.express as px
import pandas as pd

url = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv'
dati_regioni = pd.read_csv(url, error_bad_lines=False)
dati_regioni.to_csv('dpc-covid19-ita-regioni.csv')

regioni = json.load(open('regioni.geojson','r'))

dati = dati_regioni.loc[dati_regioni.data == '2020-10-27T17:00:00']

dati = dati[['denominazione_regione', 'terapia_intensiva']]

data = {'denominazione_regione':  ['Trentino-Alto Adige'],
        'terapia_intensiva': [(dati.loc[dati.denominazione_regione == 'P.A. Bolzano', 'terapia_intensiva'].item()
    + dati.loc[dati.denominazione_regione == 'P.A. Trento', 'terapia_intensiva']).item()],
        }

df = pd.DataFrame (data, columns = ['denominazione_regione','terapia_intensiva'])

dati = dati.append(df)
print(dati)

fig = px.choropleth(dati, geojson=regioni, color="terapia_intensiva",
                    locations="denominazione_regione", featureidkey="properties.NOME_REG",
                    center = {'lat' : 41.9109,
                            'lon' : 12.4818},
                    scope="europe",
                    color_continuous_scale="Viridis",
                    projection="mercator",
                   )

fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.update_geos(fitbounds="locations", visible=False)

fig.show()
