import time
from fastapi import FastAPI, HTTPException, Response
from dados import buscar_cotacao, buscar_varias, maior_alta_e_queda, ler_carteira, buscar_carteira, buscar_historico
from graficos import gerar_grafico, TEMAS, SIMBOLOS_MOEDA

app = FastAPI()

CORES = {
    "dourado": "#c9a24d",
    "verde": "#22c55e",
    "vermelho": "#ef4444",
    "azul": "#3b82f6",
    "roxo": "#a855f7",
    "branco": "#e6e9ef",
}

TEMPO_CACHE = 60
cache = {"hora": 0, "dados": None}

PERIODOS = ["5d", "1mo", "3mo", "6mo", "1y", "5y"]

cache_indices = {}
cache_historico = {}

def obter_historico(ticker, periodo):
    chave = f"{ticker}|{periodo}"
    agora = time.time()

    if chave in cache_historico:
        guardado = cache_historico[chave]
        if agora - guardado["hora"] < TEMPO_CACHE:
            return guardado["dados"]

    dados = buscar_historico(ticker, periodo)
    cache_historico[chave] = {"hora": agora, "dados": dados}
    return dados


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


@app.get("/historico/{ticker}")
def historico(ticker: str, periodo: str = "1mo"):
    
    ticker = ticker.upper()

    if periodo not in PERIODOS:
        
        raise HTTPException(
            
            status_code=400,
            detail=f"Período inválido. Use um destes: {', '.join(PERIODOS)}",
        
        )

    try:
        return obter_historico(ticker, periodo)
    except ValueError:
        raise HTTPException(status_code=404, detail=f"Sem histórico para {ticker}")
    except Exception as erro:
        print(f"Erro no histórico de {ticker}: {erro!r}")
        raise HTTPException(status_code=502, detail="Não foi possível buscar o histórico")


@app.get("/grafico/{ticker}")
def grafico(
    ticker: str,
    periodo: str = "3mo",
    largura: int = 800,
    altura: int = 480,
    cor: str = "dourado",
    tema: str = "escuro",
    moeda: str = "BRL",
):
    ticker = ticker.upper()
    moeda = moeda.upper()

    if periodo not in PERIODOS:
        raise HTTPException(status_code=400, detail=f"Período inválido. Use: {', '.join(PERIODOS)}")
    if not 400 <= largura <= 1920 or not 250 <= altura <= 1080:
        raise HTTPException(status_code=400, detail="Tamanho inválido: largura de 400 a 1920 e altura de 250 a 1080")
    if cor not in CORES:
        raise HTTPException(status_code=400, detail=f"Cor inválida. Use: {', '.join(CORES)}")
    if tema not in TEMAS:
        raise HTTPException(status_code=400, detail=f"Tema inválido. Use: {', '.join(TEMAS)}")
    if moeda not in SIMBOLOS_MOEDA:
        raise HTTPException(status_code=400, detail=f"Moeda inválida. Use: {', '.join(SIMBOLOS_MOEDA)}")

    try:
        historico = obter_historico(ticker, periodo)
    except ValueError:
        raise HTTPException(status_code=404, detail=f"Sem histórico para {ticker}")
    except Exception as erro:
        print(f"Erro no gráfico de {ticker}: {erro!r}")
        raise HTTPException(status_code=502, detail="Não foi possível buscar o histórico")

    png = gerar_grafico(historico, ticker, largura, altura, CORES[cor], tema, moeda)
    return Response(content=png, media_type="image/png")