# Desafio 1 — Containers em Rede

Objetivo
--------
Dois containers comunicando-se via rede Docker nomeada: um servidor Flask (porta 8080) e um cliente que faz requisições periódicas.

Funcionamento e decisões de implementação
----------------------------------------
O servidor Flask expõe endpoints simples (root e `/messages`) e mantém mensagens em memória; o cliente faz POSTs periódicos e lista mensagens via GET. Usei Flask e HTTP para tornar o fluxo fácil de inspecionar nos logs do Docker. O `run.sh` cria uma rede nomeada e usa nomes de serviço previsíveis para facilitar a avaliação e a comunicação entre containers.

Requisitos
---------
- Docker instalado

Execução
------------
No diretório `desafio1`:

```
chmod +x run.sh
./run.sh up
```

Verificação
------------
- Server: Execute `curl http://localhost:8080/` (A resposta esperada é: `{"message":"Hello from Desafio1 Server"}`)

- Messages endpoint:
  - POST: `curl -X POST -H "Content-Type: application/json" -d '{"from":"tester","text":"oi","id":123}' http://localhost:8080/messages`
  - GET:  `curl http://localhost:8080/messages`

- Client logs (executa requisições POST periodicamente): `docker logs -f desafio1_client`

- Server logs: `docker logs -f desafio1_server`

Rede
----
`run.sh` cria a rede `desafio1_net` e conecta ambos os containers; o client alcança o server por `desafio1_server`.

Parar e remover
--------------
```
./run.sh down
```

Notas
------------
- Dependências são instaladas nas imagens durante o build. Se quiser rodar localmente, crie um virtualenv e instale `server/requirements.txt` ou `client/requirements.txt`.

