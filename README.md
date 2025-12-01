
# Projeto FCCPD - Fundamentos de Computação Concorrente, Paralela e Distribuída

Este repositório contém implementações didáticas dos 5 desafios solicitados na disciplina. Cada desafio está em uma pasta separada com o código, Dockerfile(s) e um README local com instruções específicas.

### Estrutura
- `desafio1/` — Containers em rede (server + client)
- `desafio2/` — Volumes e persistência (Postgres + UI)
- `desafio3/` — Docker Compose (web, db, cache)
- `desafio4/` — Microsserviços independentes (users + consumer)
- `desafio5/` — Microsserviços com API Gateway (users, orders, gateway)

### Requisitos mínimos
- Docker e Docker Compose (ou Docker Engine com `docker compose`)
- **Opcional**: Python 3.11+ para executar serviços fora de containers

Uso rápido
-----------
Navegue até a pasta do desafio desejado e siga o README local. Exemplos rápidos:

```
cd desafio1 && chmod +x run.sh && ./run.sh up
cd desafio2 && chmod +x run.sh && ./run.sh up
cd desafio3 && docker compose up --build
cd desafio4 && docker compose up --build
cd desafio5 && docker compose up --build
```

Verificação e evidências
-------------------------
Prefira inspecionar respostas e logs ao vivo em vez de salvar arquivos. Exemplos úteis:

```
docker logs -f <container_name>
curl http://localhost:<port>/health
docker exec -it <db_container> psql -U postgres -c "SELECT * FROM ..."
```

Executar localmente (opcional)
-----------------------------
Se quiser rodar serviços sem Docker, crie um virtualenv e instale os requirements do serviço apropriado:

```
python -m venv .venv
source .venv/bin/activate
pip install -r desafio1/server/requirements.txt
python desafio1/server/app.py
```