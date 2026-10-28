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

        try:
            resultado_cotacao = buscar_cotacao(ticker)
            resultados.append(resultado_cotacao)

        except:
            print(f"Erro ao buscar {ticker}")
            resultados.append({"ticker": ticker, "erro": True})


    return resultados

def maior_alta_e_queda(resultados):

    validos = [r for r in resultados if "erro" not in r]

    if not validos:
        return None

    alta = max(validos, key=lambda r: r["variacao"])
    queda = min(validos, key=lambda r: r["variacao"])

    if alta["variacao"] <= 0:
        alta = None

    if queda["variacao"] >= 0:
        queda = None     


    return{"maior_alta": alta, "maior_queda": queda}

if __name__ == "__main__":
    cotacoes = buscar_varias(["XXXX9.SA", "YYYY9.SA"])
    print(maior_alta_e_queda(cotacoes))