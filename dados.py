import json
import warnings
from concurrent.futures import ThreadPoolExecutor

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
        "moeda": info["currency"],
    }


def buscar_cotacao_segura(ticker):
    try:
        return buscar_cotacao(ticker)
    except Exception:
        print(f"Erro ao buscar {ticker}")
        return {"ticker": ticker, "erro": True}


def buscar_varias(tickers):
    with ThreadPoolExecutor(max_workers=8) as executor:
        return list(executor.map(buscar_cotacao_segura, tickers))


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

    return {"maior_alta": alta, "maior_queda": queda}


def ler_carteira():

    with open("carteira.json") as arquivo:
        carteira = json.load(arquivo)

    return carteira


def buscar_carteira(carteira):

    todos = [simbolo for simbolos in carteira.values() for simbolo in simbolos]
    cotacoes = buscar_varias(todos)
    por_ticker = {c["ticker"]: c for c in cotacoes}

    resultado = {}

    for nome, simbolos in carteira.items():
        itens = [por_ticker[s] for s in simbolos]
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


def buscar_variacoes(ticker):

    tabela = yf.Ticker(ticker).history(period="1y")

    if tabela.empty:
        raise ValueError(f"Sem histórico para {ticker}")

    fechamentos = tabela["Close"]
    atual = float(fechamentos.iloc[-1])

    def variacao_desde(pregoes_atras):
        if len(fechamentos) <= pregoes_atras:
            return None
        base = float(fechamentos.iloc[-1 - pregoes_atras])
        return round((atual - base) / base * 100, 2)

    ano = fechamentos.index[-1].year
    antes_do_ano = fechamentos[fechamentos.index.year < ano]
    if antes_do_ano.empty:
        base_ano = float(fechamentos.iloc[0])
    else:
        base_ano = float(antes_do_ano.iloc[-1])

    maxima = float(tabela["High"].max())
    minima = float(tabela["Low"].min())

    return {
        "ticker": ticker,
        "preco": round(atual, 2),
        "variacoes": {
            "5d": variacao_desde(5),
            "1mo": variacao_desde(21),
            "3mo": variacao_desde(63),
            "6mo": variacao_desde(126),
            "12m": variacao_desde(len(fechamentos) - 1),
            "ano": round((atual - base_ano) / base_ano * 100, 2),
        },
        "maxima_52s": round(maxima, 2),
        "minima_52s": round(minima, 2),
        "dist_maxima": round((atual - maxima) / maxima * 100, 2),
        "dist_minima": round((atual - minima) / minima * 100, 2),
    }


if __name__ == "__main__":
    import time

    inicio = time.time()
    print(buscar_carteira(ler_carteira()))
    print(f"Levou {time.time() - inicio:.1f} segundos")