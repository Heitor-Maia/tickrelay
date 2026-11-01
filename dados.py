import warnings
import yfinance as yf
import json

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
        "moeda":info["currency"],

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

def ler_carteira():

    with open("carteira.json") as arquivo:

        tickers = json.load(arquivo)

        return tickers


def buscar_carteira(carteira):

    resultado = {}

    for nome, simbolos in carteira.items():
        itens = buscar_varias(simbolos)
        destaques = maior_alta_e_queda(itens)
        resultado[nome] = {"itens": itens, "destaques": destaques}

    return resultado

def buscar_historico(ticker, periodo="1mo"):

    tabela = yf.Ticker(ticker).history(period=periodo)

    if tabela.empty:
        raise ValueError(f"Sem histórico para {ticker}")

    resultado = []

    for data, linha in tabela.iterrows():
        resultado.append({

            "data": data.strftime("%Y-%m-%d"),
            "abertura": round(float(linha["Open"]), 2),
            "maxima": round(float(linha["High"]), 2),
            "minima": round(float(linha["Low"]), 2),
            "fechamento": round(float(linha["Close"]), 2),
            "volume": int(linha["Volume"]),
            
        })

    return resultado


if __name__ == "__main__":
    print(buscar_historico("VALE3.SA", "5d"))