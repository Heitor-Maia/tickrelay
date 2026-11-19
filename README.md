<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://github.com/user-attachments/assets/382934bc-0729-4823-a35d-ca6dd10b7534">
    <img src="https://github.com/user-attachments/assets/1a3051d9-b3bc-482d-8210-0466b0f9741c" alt="Logo do cachalot" width="200">
  </picture>
</p>

<h1 align="center">CACHALOT</h1>

<p align="center"><b>PROFUNDO · RESISTENTE · IMPONENTE</b></p>

<p align="center">
  <b>O mercado agita a superfície. Quem tem fôlego, vai fundo.</b><br>
  API de cotações de bolsas de valores, feita em Python com FastAPI.
</p>

> **Aviso:** os dados vêm do Yahoo Finance (via [yfinance](https://github.com/ranaroussi/yfinance)),
> têm atraso e podem falhar de vez em quando. Projeto educacional e de uso pessoal.
> Nada aqui é recomendação de investimento.

<p align="center">
  <img width="800" height="480" alt="Exemplo de gráfico" src="https://github.com/user-attachments/assets/a6f2932a-d7fb-402c-a7a8-fbc895cc48f9" />
</p>

## Sobre

O cachalot busca cotações e calcula a variação do dia. Também lê uma carteira
pessoal, dividida em grupos escolhidos por você (ações, FIIs, índices, cripto...),
e mostra a maior alta e a maior queda de cada grupo. A busca dos ativos é feita em
paralelo, e além dos números, a API gera gráficos em PNG que podem ser personalizados
pela URL.

## Sobre o nome

O cachalote é um dos maiores mergulhadores do planeta: desce a mais de mil metros,
onde a pressão esmagaria quase tudo, e volta. É esse o espírito do projeto: aguentar
a pressão do mercado, mergulhar fundo nos números e trazer de volta só o que importa.

## Status

- [x] Estrutura inicial do projeto
- [x] Busca de dados de cotações
- [x] Endpoints da API
- [x] Suporte a múltiplas bolsas (você informa o símbolo completo)
- [x] Histórico de preços
- [x] Gráficos em PNG
- [x] Busca de ativos em paralelo
- [x] Variações por período e posição em relação às máximas e mínimas de 52 semanas
- [x] Documentação


## Instalação

```bash
git clone https://github.com/Heitor-Maia/Cachalot-API.git
cd Cachalot-API
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configurar a carteira

Copie o arquivo de exemplo e edite com os seus símbolos:

```bash
cp carteira.example.json carteira.json
```

A carteira é dividida em grupos, e os nomes dos grupos são livres:

```json
{
    "acoes": ["PETR4.SA", "VALE3.SA", "ITUB4.SA"],
    "fiis": ["HGLG11.SA", "MXRF11.SA"],
    "etfs": ["BOVA11.SA"],
    "acoes_estrangeiras": ["AAPL", "MSFT"],
    "cripto": ["BTC-USD", "ETH-USD"],
    "indices": ["^BVSP", "^GSPC", "^IXIC"]
}
```

O `carteira.json` é ignorado pelo Git (está no `.gitignore`), então cada pessoa mantém a própria carteira localmente e ela nunca é enviada ao repositório.

## Rodar

```bash
uvicorn main:app --reload
```

A documentação interativa fica em `http://127.0.0.1:8000/docs`.

## Rotas

| Rota | O que faz |
|---|---|
| `GET /cotacao/{simbolo}` | Preço, fechamento anterior, variação e moeda de um ativo |
| `GET /indices?simbolos=^BVSP,^IXIC` | Cotação de vários símbolos de uma vez (padrão: Ibovespa, S&P 500, Nasdaq e Dow Jones) |
| `GET /carteira` | Cotação dos ativos da carteira, dividida em grupos, com a maior alta e a maior queda de cada grupo |
| `GET /historico/{simbolo}?periodo=1mo` | Histórico diário: abertura, máxima, mínima, fechamento e volume |
| `GET /variacoes/{simbolo}` | Variação por período e distância das máximas e mínimas de 52 semanas |
| `GET /grafico/{simbolo}` | Gráfico de linha em PNG |

As respostas de `/indices`, `/carteira`, `/historico` e `/variacoes` ficam em cache por 60 segundos.

### Exemplo de resposta de `/cotacao/PETR4.SA`

```json
{
    "ticker": "PETR4.SA",
    "preco": 52.51,
    "fechamento_anterior": 52.92,
    "variacao": -0.77,
    "moeda": "BRL"
}
```

Em `/carteira`, um ativo que falhou na busca volta como `{"ticker": "...", "erro": true}`
e os outros continuam normalmente. Em cada grupo, `maior_alta` só existe se algum
ativo subiu, e `maior_queda` só existe se algum caiu. Do contrário, o valor é `null`.

## Símbolos

Informe o símbolo completo, como o Yahoo Finance usa. A API **não** acrescenta
sufixos: `PETR4` não funciona, `PETR4.SA` sim.

| Ativo | Exemplo |
|---|---|
| Ação da B3 | `PETR4.SA` |
| FII | `HGLG11.SA` |
| ETF da B3 | `BOVA11.SA` |
| ETF estrangeiro | `VOO` |
| Ação estrangeira | `AAPL` |
| Criptomoeda | `BTC-USD` |
| Índice | `^BVSP`, `^GSPC`, `^IXIC` |

Cada ativo informa a moeda em que o preço é cotado (`BRL`, `USD`...).
Os valores **não são convertidos**.

## Histórico

`GET /historico/{simbolo}?periodo=1mo`

Períodos aceitos: `5d`, `1mo`, `3mo`, `6mo`, `1y` e `5y`. O padrão é `1mo`.

```json
[
    {
        "data": "2026-10-30",
        "abertura": 59.44,
        "maxima": 62.98,
        "minima": 59.42,
        "fechamento": 62.02,
        "volume": 34856400
    }
]
```

## Variações

`GET /variacoes/{simbolo}`

Devolve a variação do preço em cada período, as máximas e mínimas dos últimos 12 meses
e quanto o preço atual está distante delas.

```json
{
    "ticker": "VALE3.SA",
    "preco": 59.0,
    "variacoes": {
        "5d": -8.43,
        "1mo": -11.09,
        "3mo": -17.54,
        "6mo": -26.03,
        "12m": -1.83,
        "ano": -15.71
    },
    "maxima_52s": 89.12,
    "minima_52s": 58.79,
    "dist_maxima": -33.8,
    "dist_minima": 0.36
}
```

| Campo | O que é |
|---|---|
| `ticker` | Símbolo consultado |
| `preco` | Preço atual (durante o pregão) ou último fechamento |
| `variacoes.5d` | Variação em %, comparada a 5 pregões atrás (cerca de 1 semana) |
| `variacoes.1mo` | Variação em %, comparada a 21 pregões atrás (cerca de 1 mês) |
| `variacoes.3mo` | Variação em %, comparada a 63 pregões atrás (cerca de 3 meses) |
| `variacoes.6mo` | Variação em %, comparada a 126 pregões atrás (cerca de 6 meses) |
| `variacoes.12m` | Variação em %, desde o primeiro pregão dos últimos 12 meses |
| `variacoes.ano` | Variação em %, desde o último fechamento do ano anterior |
| `maxima_52s` | Maior preço dos últimos 12 meses |
| `minima_52s` | Menor preço dos últimos 12 meses |
| `dist_maxima` | Distância do preço atual até a máxima, em % (zero ou negativo) |
| `dist_minima` | Distância do preço atual até a mínima, em % (zero ou positivo) |

Um período fica `null` quando o ativo não tem histórico suficiente para calculá-lo.
Preço, máxima e mínima vêm na moeda do ativo, e os demais campos são percentuais.
O exemplo acima é uma resposta real, mas os valores mudam a cada dia.

## Gráfico

`GET /grafico/{simbolo}`

Todos os parâmetros são opcionais:

| Parâmetro | Opções | Padrão |
|---|---|---|
| `periodo` | os mesmos do histórico | `3mo` |
| `largura` | 400 a 1920 (pixels) | `800` |
| `altura` | 250 a 1080 (pixels) | `480` |
| `cor` | `dourado`, `verde`, `vermelho`, `azul`, `roxo`, `branco` | `dourado` |
| `tema` | `escuro`, `claro` | `escuro` |
| `moeda` | `BRL`, `USD`, `EUR`, `GBP` | `BRL` |

Exemplo:

```
/grafico/VALE3.SA?periodo=1y&tema=claro&cor=verde
```

O gráfico mostra a linha de fechamento, uma linha tracejada no valor do início do
período, e marca a maior alta e a maior baixa. A moeda é informada por quem chama
(`?moeda=USD` para ativos em dólar), porque a API não a detecta sozinha.

## Erros

| Código | Quando |
|---|---|
| `400` | Parâmetro inválido (período, tamanho, cor, tema ou moeda) |
| `404` | Símbolo não encontrado ou sem dados |
| `502` | Falha ao buscar os dados no Yahoo Finance |

## Limitações

- Os dados têm atraso em relação ao mercado.
- Fora do pregão, o preço é o do último fechamento.
- As variações por período contam pregões (5, 21, 63 e 126), então são aproximadas.
- O Yahoo Finance pode falhar de forma passageira. Em geral, repetir a chamada
  depois de alguns minutos resolve.
- O yfinance não é uma API oficial e pode mudar sem aviso.
- O cache fica na memória e é zerado quando o servidor reinicia.

## Estrutura

```
├── main.py                  # rotas da API (FastAPI)
├── dados.py                 # busca de cotações, histórico e variações
├── graficos.py              # geração dos gráficos
├── carteira.example.json    # modelo da carteira
└── requirements.txt
```

## Créditos

- Dados de mercado: [Yahoo Finance](https://finance.yahoo.com), acessados pela biblioteca [yfinance](https://github.com/ranaroussi/yfinance).
- API: [FastAPI](https://fastapi.tiangolo.com).
- Gráficos: [Matplotlib](https://matplotlib.org).

## Licença

Distribuído sob a licença MIT. Veja o arquivo [LICENSE](LICENSE).