# -*- coding: utf-8 -*-
# analysis
import pandas as pd
import numpy as np
import glob
import json
import os
import sys

# # define random seed of numpy
seed_value = 42
np.random.seed(seed_value)

# plot
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as plx
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = [16, 4]

# # progress
import traceback
from tqdm import tqdm
tqdm.pandas(desc="Processing Rows")

# # output
import warnings
warnings.filterwarnings('ignore')

# # forecast
from sklearn.model_selection import TimeSeriesSplit
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from pmdarima import auto_arima
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import adfuller

# # expand display output
pd.set_option('display.max_columns', None)

"""# Data Process"""
file_names = glob.glob("./raw_data/*")

def processar_arquivos_csv(diretorio):
    """
    Processa arquivos CSV em um diretório específico.

    Parameters:
    - diretorio (str): O caminho do diretório que contém os arquivos CSV.

    Returns:
    - data_frames (dict): Um dicionário contendo DataFrames tratados, onde as chaves são os nomes dos arquivos.

    Example:
    >>> diretorio = "../path/para/raw_data/"
    >>> data_frames = processar_arquivos_csv(diretorio)
    >>> print(data_frames.keys())
    dict_keys(['nome_arquivo1', 'nome_arquivo2', ...])
    """
    # Obtendo a lista de nomes de arquivo no diretório
    file_names = glob.glob(f"{diretorio}/*")

    # Dicionário para armazenar os DataFrames tratados
    data_frames = {}

    for file_name in file_names:
        # Obtendo o nome do arquivo sem a extensão
        name = file_name.split('/')[-1].split('.')[0]

        # Lendo o arquivo CSV e aplicando os tratamentos
        df = pd.read_csv(file_name, sep=';')
        cols_to_keep = ['close', 'volume', 'marketCap', 'timestamp']
        cols_to_rename = {'timestamp': 'date', 'marketCap': 'market_cap'}
        df = df[cols_to_keep].rename(columns=cols_to_rename)
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)

        # Extrair o ticker da parte inicial do nome da chave
        ticker = name.split('_')[0]

        # Adicionar a coluna 'ticker' ao DataFrame com o valor do ticker
        df['ticker'] = ticker

        # Armazenando o DataFrame tratado no dicionário
        data_frames[name] = df

    return data_frames

def concatenar_dataframes(data_frames):
    """
    Concatena DataFrames de um dicionário e remove possíveis duplicatas.

    Parameters:
    - data_frames (dict): Um dicionário contendo DataFrames a serem concatenados.

    Returns:
    - df_concatenado (pd.DataFrame): O DataFrame resultante após a concatenação e remoção de duplicatas.

    Example:
    >>> data_frames = {'nome_arquivo1': df1, 'nome_arquivo2': df2, ...}
    >>> df_concatenado = concatenar_dataframes(data_frames)
    >>> print(df_concatenado.head())
       close  volume  market_cap  ticker
    date
    ...
    """
    # Criar um DataFrame vazio para a concatenação
    df = pd.DataFrame()

    # Concatenar todos os DataFrames no dicionário
    for value in data_frames.values():
        df = pd.concat([df, value])

    # Remover possíveis duplicatas do DataFrame resultante
    df_concatenado = df.drop_duplicates()

    return df_concatenado

def formatar_data(df):
    """
    Formata a coluna de data e adiciona uma coluna de mês ao DataFrame.

    Parameters:
    - df (pd.DataFrame): O DataFrame a ser formatado.

    Returns:
    - df_formatado (pd.DataFrame): O DataFrame resultante após a formatação da data.

    Example:
    >>> df = pd.DataFrame({'date': ['2022-01-01', '2022-02-01', '2022-03-01'],
    ...                    'close': [100, 105, 98],
    ...                    'volume': [1000, 1200, 900],
    ...                    'market_cap': [5000, 5500, 4800],
    ...                    'ticker': ['AAPL', 'AAPL', 'AAPL']})
    >>> df_formatado = formatar_data(df)
    >>> print(df_formatado.head())
         date  close  volume  market_cap ticker      month
    0 2022-01-01    100    1000        5000   AAPL 2022-01-01
    1 2022-02-01    105    1200        5500   AAPL 2022-02-01
    2 2022-03-01     98     900        4800   AAPL 2022-03-01
    """
    # Criar uma cópia do DataFrame para evitar modificações indesejadas
    df_copy = df.reset_index().copy()

    # Adicionar uma coluna de mês ao DataFrame
    df_copy['month'] = df_copy['date'].dt.to_period('M').dt.to_timestamp()

    return df_copy

def calcular_medias_por_mes(df):
    """
    Calcula médias por mês e ticker a partir de um DataFrame.

    Parameters:
    - df (pd.DataFrame): O DataFrame contendo os dados a serem agregados.

    Returns:
    - df_agregado (pd.DataFrame): O DataFrame resultante após a agregação por mês e ticker.

    Example:
    >>> df = pd.DataFrame({'date': ['2022-01-01', '2022-01-01', '2022-02-01', '2022-02-01'],
    ...                    'close': [100, 110, 105, 108],
    ...                    'volume': [1000, 1200, 900, 950],
    ...                    'market_cap': [5000, 5500, 4800, 5200],
    ...                    'ticker': ['AAPL', 'AAPL', 'AAPL', 'AAPL']})
    >>> df_agregado = calcular_medias_por_mes(df)
    >>> print(df_agregado.head())
         month ticker  close_mean  volume_mean  market_cap_mean
    0 2022-01-01   AAPL       105.0       1100.0           5250.0
    1 2022-02-01   AAPL       106.5        925.0           5000.0
    """
    # Agrupar por mês e ticker, calculando as médias
    df_agregado = df.groupby(["month", "ticker"]).agg(
        close_mean=("close", "mean"),
        volume_mean=("volume", "mean"),
        market_cap_mean=("market_cap", "mean")
    ).reset_index()

    return df_agregado

def pivotar_dataframe(df):
    """
    Realiza a pivotagem de um DataFrame.

    Parameters:
    - df (pd.DataFrame): O DataFrame a ser pivotado.

    Returns:
    - df_pivotado (pd.DataFrame): O DataFrame resultante após a pivotagem.

    Example:
    >>> df = pd.DataFrame({'month': ['2022-01-01', '2022-02-01'],
    ...                    'ticker': ['AAPL', 'AAPL'],
    ...                    'close_mean': [105.0, 106.5]})
    >>> df_pivotado = pivotar_dataframe(df)
    >>> print(df_pivotado.head())
           month   AAPL
    0 2022-01-01  105.0
    1 2022-02-01  106.5
    """
    # Pivotar o DataFrame
    df_pivotado = df.pivot_table(index='month', columns='ticker', values='close_mean')

    # Tornar todos os nomes de coluna como string
    df_pivotado.columns = df_pivotado.columns.astype(str)

    # Preencher valores ausentes com 0
    df_pivotado = df_pivotado.fillna(0)

    # Resetar o índice e remover o nome da coluna
    df_pivotado = df_pivotado.reset_index()
    df_pivotado.columns.name = None

    return df_pivotado

"""# Metrics"""

def processar_e_salvar_params(gold_save_path, filename, df, build_best_params=False):
    """
    Processa os parâmetros para cada ticker no DataFrame df usando auto_arima e salva os resultados em um arquivo JSON.

    Parameters:
    - gold_save_path (str): Caminho onde o arquivo será salvo.
    - filename (str): Nome do arquivo a ser salvo.
    - df (pandas.DataFrame): DataFrame contendo os dados para os quais os parâmetros serão calculados.
    - build_best_params (bool, optional): Indica se deve criar um novo arquivo de parâmetros ou apenas verificar se o arquivo já existe.
                                          Se True, cria um novo arquivo; se False (padrão), verifica a existência do arquivo.

    Returns:
    None

    Example:
    processar_e_salvar_params(gold_save_path, "best_params_dict.json", df, build_best_params=False)
    """

    # Verificando se o arquivo já existe
    if os.path.exists(gold_save_path) and not build_best_params:
#        print(f'O conjunto de parâmetros para cada ticker {filename} já existe. Não foi criado um novo arquivo.')
        print(f'\n {filename} OK. \n')
    else:
        best_params_dict = {}
        for tk in tqdm(df.columns, desc=f"Processando parâmetros para {tk}"):
            model = auto_arima(df[tk].values, seasonal=True, m=12, D=1, start_P=1, start_Q=1, max_P=3, max_Q=3, information_criterion='aic', trace=False, error_action='ignore', stepwise=True)
            best_order = model.order
            best_seasonal_order = model.seasonal_order
            best_params_dict[tk] = {"best_order": model.order, "best_seasonal_order": model.seasonal_order}

        # Salvando o dicionário usando json
        with open(gold_save_path, 'w') as arquivo:
            json.dump(best_params_dict, arquivo)
        print(f'Dicionário salvo em {gold_save_path}')

def carregar_dicionario_params(caminho_arquivo):
    """
    Carrega um dicionário a partir de um arquivo JSON.

    Parameters:
    - caminho_arquivo (str): O caminho para o arquivo JSON a ser carregado.

    Returns:
    - dict: O dicionário carregado a partir do arquivo JSON.

    Example:
    >>> best_params_dict = carregar_dicionario("../content/drive/MyDrive/01 - Projetos/crypto_forecast/gold/df_gold.parquet")
    >>> print(best_params_dict)
    {'BTC': {'best_order': (1, 1, 1), 'best_seasonal_order': (0, 1, 1, 12)}, ...}
    """
    with open(caminho_arquivo, 'r') as arquivo:
        dicionario_carregado = json.load(arquivo)

    return dicionario_carregado

# to-do: MAPE dos modelos

"""# Forecast"""
# Desativar os avisos de convergência
from statsmodels.tools.sm_exceptions import ConvergenceWarning
warnings.filterwarnings("ignore", category=ConvergenceWarning)

def gerar_previsoes_sarimax(df, best_params_dict, n_periods_out_of_sample=6):
    """
    Gera previsões utilizando o modelo SARIMAX para várias séries temporais.

    Parameters:
    - df (pd.DataFrame): O DataFrame contendo as séries temporais.
    - best_params_dict (dict): Um dicionário contendo os melhores parâmetros para cada série.
    - n_periods_out_of_sample (int): O número de períodos para prever out-of-sample.

    Returns:
    - fs_df (pd.DataFrame): Um DataFrame contendo as previsões, intervalos de confiança e informações adicionais.

    Example:
    >>> df = ...  # Seu DataFrame com séries temporais
    >>> best_params_dict = {'BTC': {'best_order': (1, 1, 1), 'best_seasonal_order': (0, 1, 1, 12)}}
    >>> fs_df = gerar_previsoes_sarimax(df, best_params_dict, n_periods_out_of_sample=6)
    >>> print(fs_df.head())
             close_mean  lower_bound  upper_bound ticker  type
    2023-01-01    ...         ...         ...       BTC  PRED
    ...           ...         ...         ...       ...  ...
    """
    #fs_df = pd.DataFrame()
    fs_list = []

    print("Gerando Previsões SARIMAX")
    for tk, params in tqdm(best_params_dict.items(), file=sys.stdout):
        
        #print(f" Prevendo valores para {tk}")
        BEST_ORDER = params["best_order"]
        BEST_SEASONAL_ORDER = params["best_seasonal_order"]

        model = SARIMAX(df[f'{tk}'], order=BEST_ORDER, seasonal_order=BEST_SEASONAL_ORDER)
        res = model.fit(disp=False)

        fs = res.get_forecast(steps=n_periods_out_of_sample)
        fs_values = fs.predicted_mean
        fs_lower_bound = fs.conf_int().iloc[:, 0]
        fs_upper_bound = fs.conf_int().iloc[:, 1]

        #  fs_values_df = pd.DataFrame(fs_values.values, columns=[f'close_mean'], index=fs_values.index)
        fs_values_df = fs_values.reset_index()
        fs_values_df["lower_bound"] = np.where(fs_lower_bound.values < 0, fs_lower_bound.values, 0)
        fs_values_df["upper_bound"] = fs_upper_bound.values
        fs_values_df["ticker"] = tk
        fs_values_df["type"] = "PRED"
        fs_values_df["model"] = "SARIMA"

        #fs_df = fs_df.append(fs_values_df)
        fs_list.append(fs_values_df)
        
    fs_df = pd.concat(fs_list, ignore_index=True)		
    fs_df.rename(columns={"predicted_mean": "close_mean"}, inplace=True)
    fs_df.set_index("index", inplace=True)
    return fs_df