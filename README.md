# Time Series Forecasting of Cryptocurrencies

## Overview
O objetivo desse projeto é fazer prevsões os top 20 criptoativos em captalização de mercado. Sendo eles ```ADA, AVAX, BCH, BNB, BTC, DAI, DOGE, DOT, ETH, ICP, LINK, LTC, MATIC, SHIB, SOL, TON, TRX, USDC, USDT, XRP```. Os dados utilizados foram coletados no ```Coinmarketcap```.

<img src="framework.png">

O projeto foi dividido em três etapas: ```master```, ```functions``` e ```config```. O ```config``` é responsável por determinar todos os parâmetros e variáveis que serão usadas no pipeline, ```functions``` é onde todas as funções que serão usadas no pipeline estão, como ingestão de dados, processamento de dados, armazenamento, modelagem e previsão. O ```master``` é responsável por executar todo o pipeline.

## Results
<descrição>

# Instruções de Uso
1. Clone este repositório em seu ambiente de desenvolvimento local
2. Crie seu ambiente virtual com o comando ```python3 -m venv env```.
3. Inicialize seu ambiente virtual com o comand ```source env/bin/activate```.
4. Instale as bibliotecas necessárias do ```pip install -r requirements.txt```
5. Atualize as tabelas com os históricos, salvos no path ```raw_data```.
6. Execute a aplicação para gerar as previsoes. Exemplo: ```python3 master.py```.
7. Execute a demo e visualize a aplicação. Exemplo: ```python3 demo.py```.

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

