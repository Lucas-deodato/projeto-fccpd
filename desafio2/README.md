# Desafio 2 — Volumes e Persistência

Objetivo
--------
Demonstrar persistência usando volumes Docker com um container Postgres e uma pequena UI para visualizar notas.

Funcionamento e decisões de implementação
----------------------------------------
O projeto usa um container Postgres com um volume nomeado para persistir dados entre reinícios. Um script `run.sh` automatiza criação do volume e inicialização de dados de exemplo. A UI é uma aplicação Flask simples que conecta ao banco (via host ou rede) para demonstrar leitura/inserção; a decisão por Postgres e volumes foi para demonstrar persistência real e fácil verificação com `psql` e logs.

O volume é um recurso Docker nomeado montado no diretório de dados do Postgres (pgdata), garantindo que arquivos do banco sobrevivam à remoção do container. O `run.sh` cria o volume e injeta dados de exemplo via comando `psql` para permitir validação imediata. A UI pode rodar em host networking (Linux) para se conectar ao Postgres do host ou ser colocada na mesma rede do container — isso demonstra dois modos reais de integração. Para depurar, use `docker exec -it desafio2_db psql -U postgres` para inspecionar tabelas e `docker volume inspect` para localizar os dados no host.

Requisitos
---------
- Docker instalado

Execução
-----------
Na pasta `desafio2`, execute:

```
chmod +x run.sh
./run.sh up
```

Verificação
-----------
- Opção 1: Abrir psql dentro do container:
  - `./run.sh psql`
  - No prompt psql: `SELECT id, text FROM notes;`

- Opção 2: Consulta direta sem shell:
  - `docker exec -i desafio2_db psql -U postgres -c "SELECT id, text FROM notes;"`
  
- Visualizar os logs do Postgres: `docker logs -f desafio2_db`

UI para notas
-------------
Uma UI simples está em `ui/` para visualizar/inserir notas.

Rodar localmente (conectar ao Postgres do host):

```
python -m venv .venv
source .venv/bin/activate
pip install -r ui/requirements.txt
python ui/app.py
# abra http://localhost:8080
```

Rodar a UI em Docker (Linux, usando host networking):

```
docker build -t desafio2_ui ./ui
docker run --rm --network host --name desafio2_ui desafio2_ui
```

Persistência
-----------
Parar o container (`./run.sh stop`) e recriá-lo (`./run.sh start`) deve preservar os dados — o volume guarda o banco fora do container.

Notas
------------
- Se o seu editor mostrar erros de import (ex.: `psycopg2`), instale as dependências localmente ou use os containers (as libs são instaladas durante o build).