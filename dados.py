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


if __name__ == "__main__":
    print(buscar_cotacao("PETR4.SA"))
