# -*- coding: utf-8 -*-

# carregando infos, params, e funcoes
#%run "config.py"
#%run "functions.py"
from functions import processar_arquivos_csv, concatenar_dataframes, formatar_data, calcular_medias_por_mes, pivotar_dataframe, processar_e_salvar_params, gerar_previsoes_sarimax, carregar_dicionario_params
from config import build_best_params, file_names, diretorio, silver_path, gold_path

# Data Engineering
## dicionario de dataframes com bases históricas
data_frames = processar_arquivos_csv(diretorio)
data_frames.keys()

## base dicionario concatenada e anotada
df = concatenar_dataframes(data_frames)

## ajustando data
df_month = formatar_data(df)

## agrupando por mês, com média mensal
df_month_mean = calcular_medias_por_mes(df_month)

## criando df com histórico em cada coluna
df_month_mean_pivot = pivotar_dataframe(df_month_mean)

# métricas de avaliacao
## avaliando melhores parametros com auto_arima
dict_save_path = gold_path + "best_params_dict.json"
processar_e_salvar_params(dict_save_path, "best_params_dict.json", df_month_mean_pivot, build_best_params=build_best_params)

## carregando dicionario com melhores parametros
best_params_dict = carregar_dicionario_params(dict_save_path)

## Mape (to-do)

# previsao
df_forecast = df_month_mean.copy()
df_forecast.set_index("month", inplace=True)
df_forecast["type"] = "HIST"
df_forecast["model"] = "HIST"
df_forecast = df_forecast[["ticker", "close_mean", "type", "model"]].copy()

fs_df = gerar_previsoes_sarimax(df_month_mean_pivot, best_params_dict, n_periods_out_of_sample=6)
#df_forecast_results = df_forecast.append(fs_df)
#df_forecast_results = df_forecast.copy().append(fs_df)

import pandas as pd
df_forecast_results = pd.DataFrame()
df_forecast_results = pd.concat([df_month_mean, fs_df], ignore_index=True)

# salvando tabelas
# salvar_dados(df, df_month_mean, df_month_mean_pivot, silver_path, gold_path)
df.to_parquet(silver_path + "df_silver.parquet")
df_month_mean.to_parquet(silver_path + "df_month_mean.parquet")
df_month_mean_pivot.to_parquet(gold_path + "df_gold.parquet")
df_forecast_results.to_parquet(gold_path + "df_forecast_results.parquet")
