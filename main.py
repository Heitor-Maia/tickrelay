import time
from fastapi import FastAPI, HTTPException
from dados import buscar_cotacao, buscar_varias, maior_alta_e_queda, ler_carteira, buscar_carteira

app = FastAPI()

TEMPO_CACHE = 60
cache = {"hora": 0, "dados": None}

cache_indices = {}

@app.get("/cotacao/{ticker}")
def cotacao(ticker: str):

    ticker = ticker.upper()

    try:
        return buscar_cotacao(ticker)

    except Exception:
        raise HTTPException(status_code=404, detail=f"Não foi possivel buscar {ticker}")


@app.get("/indices")
def indices(simbolos: str = "^BVSP,^GSPC,^IXIC,^DJI"):
    agora = time.time()

    if simbolos in cache_indices:
        guardado = cache_indices[simbolos]
        if agora - guardado["hora"] < TEMPO_CACHE:
            return guardado["dados"]

    lista = [s.strip().upper() for s in simbolos.split(",") if s.strip()]
    resposta = buscar_varias(lista)

    cache_indices[simbolos] = {"hora": agora, "dados": resposta}

    return resposta

@app.get("/carteira")
def carteira():
    agora = time.time()

    if cache["dados"] is not None and agora - cache["hora"] < TEMPO_CACHE:
            return cache["dados"]

    carteira = ler_carteira()
    resposta = buscar_carteira(carteira)

    cache["dados"] = resposta
    cache["hora"] = agora


    return resposta