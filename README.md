# tickrelay

API de cotações de bolsas de valores, feita em Python com FastAPI.

> Os dados vêm do Yahoo Finance (via yfinance) e têm atraso. Este projeto é
> educacional e não é recomendação de investimento.

## Sobre

O tickrelay busca cotações e calcula a variação do dia. Também lê uma
carteira pessoal e mostra qual ação mais subiu e qual mais caiu.

## Status

- [x] Estrutura inicial do projeto
- [x] Busca de dados de cotações
- [x] Endpoints da API
- [x] Suporte a múltiplas bolsas (a pessoa informa o símbolo completo)
- [ ] Testes
- [ ] Documentação

## Instalação

```bash
git clone https://github.com/SEU_USUARIO/tickrelay.git
cd tickrelay
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configurar a carteira

Copie o arquivo de exemplo e edite com os seus símbolos:

```bash
cp carteira.example.json carteira.json
```

O `carteira.json` não vai para o Git (está no `.gitignore`).

## Rodar

```bash
uvicorn main:app --reload
```

A documentação interativa fica em `http://127.0.0.1:8000/docs`.

## Rotas

| Rota | O que faz |
|---|---|
| `GET /cotacao/{simbolo}` | Preço, fechamento anterior e variação de um ativo |
| `GET /indices` | Ibovespa (`^BVSP`) |
| `GET /carteira` | Cotação de cada ativo da carteira, com a maior alta e a maior queda |

A rota `/carteira` guarda a resposta em cache por 60 segundos.

## Símbolos

Informe o símbolo completo, como o Yahoo Finance usa:

| Ativo | Exemplo |
|---|---|
| Ação da B3 | `PETR4.SA` |
| Índice | `^BVSP` |

Sem o sufixo, o símbolo não é encontrado (`PETR4` não funciona, `PETR4.SA` sim).

## Limitações

- Os dados têm atraso em relação ao mercado.
- Fora do pregão, o preço é o do último fechamento.
- O Yahoo pode falhar de vez em quando; nesse caso o ativo volta marcado
  com `"erro": true` na carteira.