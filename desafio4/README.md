
# Desafio 4 — Microsserviços Independentes

Objetivo
--------
Dois microsserviços independentes: `users` (expõe `/users`) e `consumer` (expõe `/combined` e consome `users`). O serviço `users` exige um header `X-API-Key`.

Funcionamento e decisões de implementação
----------------------------------------
O serviço `users` responde listas JSON e exige `X-API-Key` para demonstrar autenticação simples; `consumer` chama `users` e formata a resposta. A separação em dois serviços simula uma arquitetura real de microsserviços e facilita testar autenticação, chamadas inter-serviço e visualização do spec OpenAPI. Optei por comunicação HTTP simples e exposição do spec para facilitar a avaliação manual.

A checagem da API key é feita no header `X-API-Key` e resulta em 401/403 quando ausente ou inválida — isso demonstra comportamento de autenticação leve sem introduzir tokens complexos. O `consumer` adiciona o header nas requisições ao `users` para autenticação; ambos os serviços são intencionalmente pequenos para facilitar leitura do código e depuração. O spec OpenAPI está disponível em `openapi/users.yaml` e em runtime (`/openapi.yaml`) para permitir inspeção automática ou com ferramentas como Redoc/Swagger.

Requisitos
---------
- Docker e Docker Compose

Execução
-----------
Na pasta `desafio4`:

```
docker compose up --build
```

Testes básicos
-------------
- `users` (direto):
	- `curl -H "X-API-Key: changeme" http://localhost:5001/users`
- `consumer` (chama `users`):
	- `curl http://localhost:5002/combined`

O endpoint `/combined` não exige `X-API-Key` — o `consumer` age como cliente autorizado do serviço `users` e envia sua própria chave (definida pela variável de ambiente `API_KEY`) ao fazer a chamada interna.

Passar a API key
----------------
- Sem editar o compose: exporte a variável ao rodar `docker run` ou defina `-e API_KEY=changeme`.
- Ou edite `docker-compose.yml` adicionando `environment: - API_KEY=changeme` na seção `users`.

OpenAPI
-------
- Spec: `desafio4/openapi/users.yaml`
- O serviço `users` também expõe `/openapi.yaml` em runtime; use um viewer (Redoc/Swagger) apontando para o arquivo para visualizar.

Logs e verificação
------------------
- Siga logs: `docker logs -f <container_name>` para ver requisições e erros.

Notas
-----
- Dependências são instaladas durante o build das imagens; instale localmente apenas se for rodar sem Docker.

