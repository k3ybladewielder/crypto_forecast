import pandas as pd
import gradio as gr
import plotly.express as px

df_plot = pd.read_parquet('./gold/df_forecast_results.parquet') #, parse_dates=['timestamp'])

# Função para plotar o gráfico com base nos parâmetros fornecidos
def plot_graph(ticker_options):
    df_ticker = df_plot[df_plot["ticker"].isin(ticker_options)]

    fig = px.line()
    for ticker in df_ticker["ticker"].unique():
        # Adicionar linha para HIST e PRED
        fig.add_scatter(x=df_ticker.index, 
                        y=df_ticker["close_mean"],
                        mode='lines', name=f'{ticker}',
                        line=dict(dash='solid'),  # Linha HIST
                        legendgroup=f'{ticker}')

        fig.add_scatter(x=df_ticker[df_ticker["type"] == "PRED"].index,
                        y=df_ticker[df_ticker["type"] == "PRED"]["close_mean"],
                        mode='lines',
                        name=f'{ticker}',
                        line=dict(dash='dot'),  # Linha PRED
                        legendgroup=f'{ticker}')

    # Adicionar rótulos e título
    fig.update_layout(
        title="Histórico e Previsão para os Tickers",
        xaxis_title="Data",
        yaxis_title="Valor",
        )        
    return fig

# Definir as opções para a caixa de seleção
ticker_options = list(df_plot['ticker'].unique())
months = list(df_plot.index)

# Criar a interface Gradio com blocos
#intro_block = gr.Markdown("Time Series Forecasting of Cryptocurrencies.")
ticker_block = gr.CheckboxGroup(ticker_options, label='Selecione o Ticker', every=True)
graph_block = gr.Plot(plot_graph(ticker_options))

# Criar a interface Gradio
iface = gr.Interface(fn=plot_graph,
                    title="Time Series Forecasting of Cryptocurrencies",
                    description="Forecast dos top 20 criptoativos em captalização de mercado. \
                                 Sendo eles ```ADA, AVAX, BCH, BNB, BTC, DAI, DOGE, DOT, ETH, ICP, LINK, LTC, MATIC, SHIB, SOL, TON, TRX, USDC, USDT, XRP```. \
                                 Os dados utilizados foram coletados no ```Coinmarketcap```.",
                                 inputs=[ticker_block],
                                 outputs=graph_block
                            )

# Lançar a interface
iface.launch()