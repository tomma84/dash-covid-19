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


# URL dei dati aggiornati giornalmente
url = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv'

# Lettura dei dati dall'url
dati = pd.read_csv(url, error_bad_lines=False)

