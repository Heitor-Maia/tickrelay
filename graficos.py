import io
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter

TEMAS = {
    "escuro": {
        "fundo": "#141821", "texto": "#9aa4b2", "grade": "#2a3140",
        "titulo": "#e6e9ef", "caixa": "#1d2331", "referencia": "#6ea8fe", "sombra": 0.35,
    },
    "claro": {
        "fundo": "#ffffff", "texto": "#4a5568", "grade": "#e5e7eb",
        "titulo": "#1a202c", "caixa": "#f3f4f6", "referencia": "#2b6cb0", "sombra": 0.30,
    },
}

SIMBOLOS_MOEDA = {"BRL": "R$", "USD": "US$", "EUR": "€", "GBP": "£"}

VERDE = "#22c55e"
VERMELHO = "#ef4444"


def formatar_data(texto):
    ano, mes, dia = texto.split("-")
    return f"{dia}/{mes}/{ano[2:]}"


def formatar_preco(valor, simbolo):
    if valor == int(valor):
        texto = f"{valor:,.0f}"
    else:
        texto = f"{valor:,.2f}"
    texto = texto.replace(",", "#").replace(".", ",").replace("#", ".")
    return f"{simbolo} {texto}"


def texto_em_caixa(fig, x, y, texto, cores, cor_destaque, tamanho, negrito=False, cor_texto=None, recuo=0):
    peso = "bold" if negrito else "normal"
    estilo_caixa = "round,pad=0.5"
    texto = " " * recuo + texto

    # sombra: o mesmo texto, deslocado, com o texto invisível e só a caixa colorida aparecendo
    fig.text(
        x + 0.004, y - 0.008, texto,
        color=(0, 0, 0, 0), fontsize=tamanho, fontweight=peso, ha="left", va="center",
        bbox=dict(boxstyle=estilo_caixa, facecolor=cor_destaque, edgecolor="none", alpha=cores["sombra"]),
    )

    # caixa de verdade, com borda na cor de destaque
    fig.text(
        x, y, texto,
        color=cor_texto or cores["titulo"], fontsize=tamanho, fontweight=peso, ha="left", va="center",
        bbox=dict(boxstyle=estilo_caixa, facecolor=cores["caixa"], edgecolor=cor_destaque),
    )


def gerar_grafico(historico, titulo, largura=800, altura=480, cor="#c9a24d", tema="escuro", moeda="BRL"):

    cores = TEMAS[tema]
    simbolo = SIMBOLOS_MOEDA.get(moeda, moeda)

    datas = [d["data"] for d in historico]
    fechamentos = [d["fechamento"] for d in historico]

    fig = Figure(figsize=(largura / 100, altura / 100), dpi=100, facecolor=cores["fundo"])
    ax = fig.subplots()
    ax.set_facecolor(cores["fundo"])

    posicoes = range(len(datas))

    minimo = min(fechamentos)
    maximo = max(fechamentos)
    indice_max = fechamentos.index(maximo)
    indice_min = fechamentos.index(minimo)

    margem = (maximo - minimo) * 0.08 or 1
    base = minimo - margem

    # linha e área preenchida
    ax.plot(posicoes, fechamentos, color=cor, linewidth=2)
    ax.fill_between(posicoes, fechamentos, base, color=cor, alpha=0.12)

    # linha de referência no valor inicial, com etiqueta na direita
    ax.axhline(fechamentos[0], color=cores["referencia"], linestyle="--", linewidth=1, alpha=0.8)
    ax.annotate(
        formatar_preco(fechamentos[0], simbolo),
        xy=(1, fechamentos[0]),
        xycoords=ax.get_yaxis_transform(),
        xytext=(6, 0),
        textcoords="offset points",
        ha="left",
        va="center",
        fontsize=9,
        fontweight="bold",
        color=cores["fundo"],
        bbox=dict(boxstyle="round,pad=0.3", facecolor=cores["referencia"], edgecolor="none"),
        annotation_clip=False,
    )

    # pontos de maior alta e maior baixa
    ax.scatter(indice_max, maximo, color=VERDE, s=45, zorder=5,
               edgecolors=cores["fundo"], linewidths=1.5, clip_on=False)
    ax.scatter(indice_min, minimo, color=VERMELHO, s=45, zorder=5,
               edgecolors=cores["fundo"], linewidths=1.5, clip_on=False)

    ax.set_ylim(base, maximo + margem)
    ax.set_xlim(0, max(1, len(datas) - 1))

    # rótulos de data espalhados, incluindo o primeiro e o último dia
    total = len(datas)
    quantidade = min(total, 6)
    if quantidade > 1:
        indices = sorted({round(i * (total - 1) / (quantidade - 1)) for i in range(quantidade)})
    else:
        indices = [0]

    ax.set_xticks(indices)
    rotulos = ax.set_xticklabels([formatar_data(datas[i]) for i in indices])
    rotulos[0].set_ha("left")
    rotulos[-1].set_ha("right")

    ax.yaxis.set_major_formatter(FuncFormatter(lambda valor, pos: formatar_preco(valor, simbolo)))

    ax.tick_params(colors=cores["texto"], length=0)
    ax.grid(axis="y", color=cores["grade"], linewidth=0.8)
    ax.set_axisbelow(True)

    for lado in ["top", "right", "left", "bottom"]:
        ax.spines[lado].set_visible(False)

    y_topo = 0.93

    # nome da ação: borda e sombra na mesma cor da linha do gráfico
    texto_em_caixa(fig, 0.06, y_topo, titulo, cores, cor, tamanho=15, negrito=True)

    # legenda: caixa com borda e sombra na cor do ponto, e o ponto dentro dela
    for x_texto, rotulo, valor, cor_ponto in [
        (0.44, "Maior alta", maximo, VERDE),
        (0.69, "Maior baixa", minimo, VERMELHO),
    ]:
        texto_em_caixa(
            fig, x_texto, y_topo, f"{rotulo}  {formatar_preco(valor, simbolo)}",
            cores, cor_ponto, tamanho=9, cor_texto=cores["texto"], recuo=4,
        )
        fig.add_artist(Line2D(
            [x_texto + 0.010], [y_topo], marker="o", color="none",
            markerfacecolor=cor_ponto, markeredgecolor="none", markersize=7,
            transform=fig.transFigure, zorder=10,
        ))

    fig.tight_layout(rect=(0.01, 0, 0.985, 0.86))

    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", facecolor=fig.get_facecolor())

    return buffer.getvalue()


if __name__ == "__main__":
    from dados import buscar_historico

    dados = buscar_historico("VALE3.SA", "3mo")

    for tema in ["escuro", "claro"]:
        png = gerar_grafico(dados, "VALE3.SA", tema=tema)
        with open(f"teste_{tema}.png", "wb") as arquivo:
            arquivo.write(png)


if __name__ == "__main__":
    from dados import buscar_historico

    dados = buscar_historico("VALE3.SA", "3mo")
    png = gerar_grafico(dados, "VALE3.SA")

    with open("teste.png", "wb") as arquivo:
        arquivo.write(png)