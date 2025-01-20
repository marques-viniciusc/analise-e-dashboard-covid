"""
Análise e Dashboard - Covid-19
--------------------------------------
O código do arquivo tem como intenção fazer a extração e tratamento de dados para que eles estejam organizados e prontos para serem 
utilizados em um dashboard de análise de dados sobre a Covid-19 no Brasil. Os dados são extraídos de fontes públicas e são tratados 
para que possam ser utilizados em um dashboard de análise de dados.

A intenção é conseguir extrarir informações relevantes sobre a situação da Covid-19 no Brasil, como número de casos, número de mortes, 
número de vacinados, entre outros. A partir dessas informações, é possível fazer análises e comparações sobre a situação da Covid-19 no 
Brasil, auxiliando na compreensão das estratégias adotadas pelo Brasil no período de pandemia.
Esse tipo de informação é essencial para que possamos traçar estratégias futuras no tratamento de novas doenças, bem como na criação de
políticas públicas na área da saúde. 
--------------------------------------
O projeto busca responder as seguintes perguntas:
- Qual era a situação da pandemia de Covid-19 no Brasil em 2021?
- Qual foi o impacto da vacinação na pandemia de Covid-19 no Brasil em 2021?
- Quais foram as tendências de casos e mortes por Covid-19 no Brasil em 2021?

--------------------------------------
O código inclui as seguintes etapas:
- Extração de dados;
- Limpeza e pré-processamento de dados;
- Dashboard para visualização.
--------------------------------------
Links:
- Fontes dos dados sobre os casos de Covid: https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports
- Fontes dos dados socbre a vacinação: https://covid.ourworldindata.org/data/owid-covid-data.csv
- Dashboard de visualização: https://lookerstudio.google.com/u/0/reporting/edc3d964-8f1b-4f66-87fe-4f478b2f358b/page/ZfhdE
"""

# Importação de bibliotecas

import math
from typing import Iterator
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Dados sobre os casos de Covid

## Extração

cases = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/01-12-2021.csv', sep=',')

### Visualização inicial e definição da data

cases.head()

def date_range(start_date: datetime, end_date: datetime) -> Iterator[datetime]:
  date_range_days: int = (end_date - start_date).days
  for lag in range(date_range_days):
    yield start_date + timedelta(lag)

start_date = datetime(2021,  1,  1) # Será analisado apenas o ano de 2021
end_date   = datetime(2021, 12, 31)

### Seleção das colunas sobre o Brasil

cases = None
cases_is_empty = True

for date in date_range(start_date=start_date, end_date=end_date):

  date_str = date.strftime('%m-%d-%Y')
  data_source_url = f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{date_str}.csv'

  case = pd.read_csv(data_source_url, sep=',')

  case = case.drop(['FIPS', 'Admin2', 'Last_Update', 'Lat', 'Long_', 'Recovered', 'Active', 'Combined_Key', 'Case_Fatality_Ratio'], axis=1)
  case = case.query('Country_Region == "Brazil"').reset_index(drop=True)
  case['Date'] = pd.to_datetime(date.strftime('%Y-%m-%d'))
  if cases_is_empty:
    cases = case
    cases_is_empty = False
  else:
    cases = pd.concat([cases, case], axis= 0, ignore_index=True)

cases.query('Province_State == "Sao Paulo"').head() # Visualização de São Paulo como exemplo

## Wrangling

cases.head()

cases.shape

cases.info()

cases = cases.rename( # Renomeando as colunas para o padrão de divisão geográfico brasleiro
  columns={
    'Province_State': 'state',
    'Country_Region': 'country'
  }
)

for col in cases.columns:
  cases = cases.rename(columns={col: col.lower()})

states_map = { # Acentuação correta dos estados
    'Amapa': 'Amapá',
    'Ceara': 'Ceará',
    'Espirito Santo': 'Espírito Santo',
    'Goias': 'Goiás',
    'Para': 'Pará',
    'Paraiba': 'Paraíba',
    'Parana': 'Paraná',
    'Piaui': 'Piauí',
    'Rondonia': 'Rondônia',
    'Sao Paulo': 'São Paulo'
}

cases['state'] = cases['state'].apply(lambda state: states_map.get(state) if state in states_map.keys() else state)

### Chaves temporais

cases['month'] = cases['date'].apply(lambda date: date.strftime('%Y-%m'))
cases['year']  = cases['date'].apply(lambda date: date.strftime('%Y'))

### População estimada do estado

cases['population'] = round(100000 * (cases['confirmed'] / cases['incident_rate'])) # Cálculo da população a partir da taxa de confirmados e incidência de covid
cases = cases.drop('incident_rate', axis=1)

### Dados diários e médias móveis

ases_ = None
cases_is_empty = True

def get_trend(rate: float) -> str: # Estabelecimento de padrões para definição de tendência

  if np.isnan(rate):
    return np.nan

  if rate < 0.85:    
    status = 'downward'
  elif rate > 1.15:
    status = 'upward'
  else:
    status = 'stable'

  return status


for state in cases['state'].drop_duplicates():

  cases_per_state = cases.query(f'state == "{state}"').reset_index(drop=True)
  cases_per_state = cases_per_state.sort_values(by=['date'])

  cases_per_state['confirmed_1d'] = cases_per_state['confirmed'].diff(periods=1)
  cases_per_state['confirmed_moving_avg_7d'] = np.ceil(cases_per_state['confirmed_1d'].rolling(window=7).mean())
  cases_per_state['confirmed_moving_avg_7d_rate_14d'] = cases_per_state['confirmed_moving_avg_7d']/cases_per_state['confirmed_moving_avg_7d'].shift(periods=14)
  cases_per_state['confirmed_trend'] = cases_per_state['confirmed_moving_avg_7d_rate_14d'].apply(get_trend)

  cases_per_state['deaths_1d'] = cases_per_state['deaths'].diff(periods=1)
  cases_per_state['deaths_moving_avg_7d'] = np.ceil(cases_per_state['deaths_1d'].rolling(window=7).mean())
  cases_per_state['deaths_moving_avg_7d_rate_14d'] = cases_per_state['deaths_moving_avg_7d']/cases_per_state['deaths_moving_avg_7d'].shift(periods=14)
  cases_per_state['deaths_trend'] = cases_per_state['deaths_moving_avg_7d_rate_14d'].apply(get_trend)

  if cases_is_empty:
    cases_ = cases_per_state
    cases_is_empty = False
  else:
    cases_ = pd.concat([cases_, cases_per_state],axis=0, ignore_index=True)

cases = cases_
cases_ = None

### Reorganização

cases['population'] = cases['population'].astype('Int64')
cases['confirmed_1d'] = cases['confirmed_1d'].astype('Int64')
cases['confirmed_moving_avg_7d'] = cases['confirmed_moving_avg_7d'].astype('Int64')
cases['deaths_1d'] = cases['deaths_1d'].astype('Int64')
cases['deaths_moving_avg_7d'] = cases['deaths_moving_avg_7d'].astype('Int64')

cases = cases[['date', 'country', 'state', 'population', 'confirmed', 'confirmed_1d', 'confirmed_moving_avg_7d', 'confirmed_moving_avg_7d_rate_14d', 'confirmed_trend', 'deaths', 'deaths_1d', 'deaths_moving_avg_7d', 'deaths_moving_avg_7d_rate_14d', 'deaths_trend', 'month', 'year']]

cases.head(n=25)

### Criação do csv

cases.to_csv('./covid-cases.csv', sep=',', index=False)

# Dados sobre vacinação

## Extração

vaccines = pd.read_csv('https://covid.ourworldindata.org/data/owid-covid-data.csv', sep=',', parse_dates=[3], infer_datetime_format=True)

vaccines.head()

vaccines = vaccines.query('location == "Brazil"').reset_index(drop=True)
vaccines = vaccines[['location', 'population', 'total_vaccinations', 'people_vaccinated', 'people_fully_vaccinated', 'total_boosters', 'date']]

vaccines.head()

## Wrangling

vaccines.head()

vaccines.shape

vaccines.info()

vaccines = vaccines.ffill()

vaccines = vaccines[(vaccines['date'] >= '2021-01-01') & (vaccines['date'] <= '2021-12-31')].reset_index(drop=True) # fitlragem da data para apenas 2021

vaccines = vaccines.rename( # Novamente renomeando as colunas para padrão de divisão geográfico brasileiro
  columns={
    'location': 'country',
    'total_vaccinations': 'total',
    'people_vaccinated': 'one_shot',
    'people_fully_vaccinated': 'two_shots',
    'total_boosters': 'three_shots',
  }
)

### Chaves temporais

vaccines['month'] = vaccines['date'].apply(lambda date: date.strftime('%Y-%m'))
vaccines['year']  = vaccines['date'].apply(lambda date: date.strftime('%Y'))

### Dados relativos

vaccines['one_shot_perc'] = round(vaccines['one_shot'] / vaccines['population'], 4) # Estabelecimento de porcentagens de vacinação (por dose)
vaccines['two_shots_perc'] = round(vaccines['two_shots'] / vaccines['population'], 4)
vaccines['three_shots_perc'] = round(vaccines['three_shots'] / vaccines['population'], 4)

## Reorganização

vaccines['population'] = vaccines['population'].astype('Int64')
vaccines['total'] = vaccines['total'].astype('Int64')
vaccines['one_shot'] = vaccines['one_shot'].astype('Int64')
vaccines['two_shots'] = vaccines['two_shots'].astype('Int64')
vaccines['three_shots'] = vaccines['three_shots'].astype('Int64')

vaccines = vaccines[['date', 'country', 'population', 'total', 'one_shot', 'one_shot_perc', 'two_shots', 'two_shots_perc', 'three_shots', 'three_shots_perc', 'month', 'year']]

vaccines.tail()

### Criação do csv

vaccines.to_csv('./covid-vaccines.csv', sep=',', index=False)

# Visualizações e insights

## Evolução dos casos no Brasil

brazil_data = cases.groupby('date').agg({
    'confirmed_1d': 'sum',
    'deaths_1d': 'sum'
}).reset_index()

plt.figure(figsize=(10, 6))
plt.plot(brazil_data['date'], brazil_data['confirmed_1d'], label='Casos Confirmados Diários')
plt.title('Evolução dos Casos Confirmados no Brasil')
plt.xlabel('Data')
plt.ylabel('Casos Confirmados Diários')
plt.legend()
plt.tight_layout()
plt.show()

## Evolução das mortes no Brasil

plt.figure(figsize=(10, 6))
plt.plot(brazil_data['date'], brazil_data['deaths_1d'], label='Óbiros Diários')
plt.title('Evolução dos Óbitos no Brasil')
plt.xlabel('Data')
plt.ylabel('Óbitos Diários')
plt.legend()
plt.tight_layout()
plt.show()

## Evolução da vacinação no Brasil

vaccination_data = vaccines.groupby('date').agg({
    'one_shot': 'sum'
}).reset_index()

plt.figure(figsize=(10, 6))
plt.plot(vaccination_data['date'], vaccination_data['one_shot'], label='Primeira Dose Aplicada')
plt.title('Evolução da Vacinação no Brasil')
plt.xlabel('Data')
plt.ylabel('Vacinação')
plt.legend()
plt.tight_layout()
plt.show()
