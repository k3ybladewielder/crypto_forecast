import pandas as pd
import gradio as gr
import plotly.express as px

df_plot = pd.read_parquet('./gold/df_forecast_results.parquet') #, parse_dates=['timestamp'])

import gradio as gr

# Função para plotar o gráfico com base nos parâmetros fornecidos
def plot_graph(ticker_options):
    filtered_df = df_plot[(df_plot['ticker'].isin(ticker_options))] # & (df_plot['month'].isin(months))]
    
    fig = px.line(filtered_df, x=filtered_df["month"], y=filtered_df['close_mean'], title=f'Close Mean Over Time')
    fig.update_layout(xaxis_title='Date', yaxis_title='Close Mean')
    
    return fig

# Definir as opções para a caixa de seleção
ticker_options = list(df_plot['ticker'].unique())
months = list(df_plot["month"].unique())

# Criar a interface Gradio
iface = gr.Interface(fn=plot_graph, inputs=[
                         gr.CheckboxGroup(ticker_options, label='Select Ticker', info="Ticker to predict the next 6 months"),
                         #gr.DatePicker(label='Select Start Date', default='2018-01-01')
                         #gr.Dropdown(months, value=months, multiselect=True, label="Datas")
                        ],
                     outputs=gr.Plot(plot_graph(ticker_options))
                     )

# Lançar a interface
iface.launch()