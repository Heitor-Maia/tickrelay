import warnings
import yfinance as yf


warnings.filterwarnings("ignore")


def buscar_cotacao(ticker):

    acao = yf.Ticker(ticker)
    info = acao.fast_info

    preco = info["lastPrice"]
    fechamento_anterior = info["previousClose"]

    variacao = (preco - fechamento_anterior) / fechamento_anterior * 100

    return {

        "ticker": ticker,
        "preco": round(preco, 2),
        "fechamento_anterior": round(fechamento_anterior, 2),
        "variacao": round(variacao, 2),
    
    }

def buscar_varias(tickers):

    resultados = []

    for ticker in tickers:
        resultado_cotacao = buscar_cotacao(ticker)
        resultados.append(resultado_cotacao)

    return resultados


if __name__ == "__main__":
    print(buscar_varias(["PETR4.SA", "VALE3.SA", "ITUB4.SA"]))
