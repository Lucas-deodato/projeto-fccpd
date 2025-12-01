# Desafio 3 — Docker Compose (web, db, cache)

Objetivo
--------
Demonstrar orquestração com Docker Compose usando três serviços: `web` (Flask), `db` (Postgres) e `cache` (Redis).

Funcionamento e decisões de implementação
----------------------------------------
O `docker-compose.yml` orquestra web, banco e cache em uma rede comum; o serviço web consulta o banco e o Redis para demonstrar integração entre serviços. Adicionei healthchecks no Compose para demonstrar readiness; usar Compose permite avaliar dependências, resolução DNS por serviço e inspeção fácil via `docker ps` e `docker inspect`.

Requisitos
---------
- Docker e Docker Compose

Execução
-----------
Na pasta `desafio3`:

```
docker compose up --build
```

Verificação
-----------
- Endpoint: `curl http://localhost:8081/info` — deve retornar JSON com referências a `db` e `cache`.
- Healthchecks:
	- Rodar em background: `docker compose up --build -d`
	- Listar containers: `docker ps --format 'table {{.Names}}\t{{.Status}}'`
	- Inspecionar health: `docker inspect --format '{{json .State.Health}}' <container_name>`

Notas
-----
- `depends_on` controla ordem de start, mas não readiness — use healthchecks para verificar se um serviço está pronto.
- Se quiser rodar localmente sem Docker, instale `web/requirements.txt` e execute `web/app.py`.

