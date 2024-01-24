# Time Series Forecasting of Cryptocurrencies

## Overview
O objetivo desse projeto é fazer prevsões os top 20 criptoativos em captalização de mercado. Sendo eles ```ADA, AVAX, BCH, BNB, BTC, DAI, DOGE, DOT, ETH, ICP, LINK, LTC, MATIC, SHIB, SOL, TON, TRX, USDC, USDT, XRP```. Os dados utilizados foram coletados no ```Coinmarketcap```.

<img src="framework.png">

O projeto foi dividido em três etapas: ```master```, ```functions``` e ```config```. O ```config``` é responsável por determinar todos os parâmetros e variáveis que serão usadas no pipeline, ```functions``` é onde todas as funções que serão usadas no pipeline estão, como ingestão de dados, processamento de dados, armazenamento, modelagem e previsão. O ```master``` é responsável por executar todo o pipeline.

Para acessar a aplicação, basta executar a ```demo.py```, e selecionar quais ativos e suas previsões quer visualizar.

<img src="demo.gif"> 

## Results
<descrição>

# Instruções de Uso
1. Clone este repositório em seu ambiente de desenvolvimento local. No Linux, abra o terminal e use o comando `git clone https://github.com/k3ybladewielder/crypto_forecast.git`. Windows, utilize o Git Bash ou o GitHub Desktop para clonar o repositório.
2. Crie seu ambiente virtual com o comando ```python3 -m venv env``` no Linux ou `python -m venv env` no Windows.
3. Inicialize seu ambiente virtual com o comand ```source env/bin/activate```. No Windows execute `.\env\Scripts\activate`.
4. Instale as bibliotecas necessárias do ```pip install -r requirements.txt```
5. Atualize as tabelas com os históricos, salvos no path `raw_data`. Certifique-se de ter os dados no diretório especificado e prossiga para o próximo passo.
6. Execute a aplicação para gerar as previsoes. No linux execute ```python3 master.py```, no Windows `python master.py`.
7. Execute a demo e visualize a aplicação. Exemplo: ```python3 demo.py```. No Windows execute `python demo.py`. Abra o link retornado pelo comando para acessar a aplicação no navegador.

## Roadmap
- [ ] Coleta de dados via API
- [X] Previsão Univariada
- [ ] Previsão Multivariada
- [ ] Previsão com modelos de Bagging e Boosting
- [X] Estruturação de previsões
- [X] Estruturação do código
- [X] Modularização
- [ ] Demo
- [ ] Deploy

# Contribuições
Se você desenha contribuir com esse projeto com melhorias ou sugestões, sinta-se a vontade para abrir um pull request.

