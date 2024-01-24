# Time Series Forecasting of Cryptocurrencies

## Overview
O objetivo desse projeto é fazer prevsões os top 20 criptoativos em captalização de mercado. Sendo eles ```ADA, AVAX, BCH, BNB, BTC, DAI, DOGE, DOT, ETH, ICP, LINK, LTC, MATIC, SHIB, SOL, TON, TRX, USDC, USDT, XRP```. Os dados utilizados foram coletados no ```Coinmarketcap```.

<img src="framework.png">

O projeto foi dividido em três etapas: ```master```, ```functions``` e ```config```. O ```config``` é responsável por determinar todos os parâmetros e variáveis que serão usadas no pipeline, ```functions``` é onde todas as funções que serão usadas no pipeline estão, como ingestão de dados, processamento de dados, armazenamento, modelagem e previsão. O ```master``` é responsável por executar todo o pipeline.

## Results
<descrição>

# Instruções de Uso
1. Clone este repositório em seu ambiente de desenvolvimento local:
   - Linux: Abra o terminal e use o comando `git clone https://github.com/k3ybladewielder/crypto_forecast.git`.
   - Windows: Utilize o Git Bash ou o GitHub Desktop para clonar o repositório.

2. Crie seu ambiente virtual:
   - Linux: No terminal, execute `python3 -m venv env`.
   - Windows: Utilize o prompt de comando e execute `python -m venv env`.

3. Inicialize seu ambiente virtual:
   - Linux: No terminal, use o comando `source env/bin/activate`.
   - Windows: No prompt de comando, execute `.\env\Scripts\activate`.

4. Instale as bibliotecas necessárias:
   - Execute `pip install -r requirements.txt`.

5. Atualize as tabelas com os históricos, salvos no path `raw_data`:
   - Linux/Windows: Certifique-se de ter os dados no diretório especificado e prossiga para o próximo passo.

6. Execute a aplicação para gerar as previsões:
   - Utilize o comando `python3 master.py` no Linux.
   - No Windows, execute `python master.py`.

7. Execute a demo e visualize a aplicação:
   - No Linux, use `python3 demo.py`.
   - No Windows, execute `python demo.py`.

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

