import time
from fastapi import FastAPI, HTTPException
from dados import buscar_cotacao, buscar_varias, maior_alta_e_queda, ler_carteira

app = FastAPI()

TEMPO_CACHE = 60
cache = {"hora": 0, "dados": None}


@app.get("/cotacao/{ticker}")
def cotacao(ticker: str):

    ticker = ticker.upper()

    try:
        return buscar_cotacao(ticker)

    except Exception:
        raise HTTPException(status_code=404, detail=f"Não foi possivel buscar {ticker}")


@app.get("/indices")
def indices():
    try:
        return buscar_cotacao("^BVSP")

    except Exception:
        raise HTTPException(status_code=502, detail="Não foi possivel buscar o ibovespa")


@app.get("/carteira")
def carteira():
    agora = time.time()

    if cache["dados"] is not None and agora - cache["hora"] < TEMPO_CACHE:
            return cache["dados"]

    tickers = ler_carteira()
    acoes = buscar_varias(tickers)
    destaques = maior_alta_e_queda(acoes)
    resposta = {"acoes": acoes, "destaques": destaques}

    cache["dados"] = resposta
    cache["hora"] = agora


    return resposta