from fastapi import FastAPI, HTTPException
from dados import buscar_cotacao, buscar_varias, maior_alta_e_queda, ler_carteira

app = FastAPI()


@app.get("/cotacao/{ticker}")
def cotacao(ticker: str):

    ticker = ticker.upper()
    if not ticker.endswith(".SA") and not ticker.startswith("^"):
        ticker = ticker + ".SA"

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

    tickers = ler_carteira()
    acoes = buscar_varias(tickers)
    destaques = maior_alta_e_queda(acoes)
    return {"acoes":acoes, "destaques": destaques}