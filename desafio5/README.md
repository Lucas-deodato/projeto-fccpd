
# Desafio 5 — Microsserviços com API Gateway

Objetivo
--------
Gateway que roteia (proxy) chamadas para dois microsserviços (`users`, `orders`) e demonstra retry + circuit-breaker.

Funcionamento e decisões de implementação
----------------------------------------
O gateway aceita chamadas externas e repassa para os serviços `users` e `orders`, implementando retry com backoff e um circuito simples que abre após falhas consecutivas. Essa peça demonstra padrões de resiliência (retry, circuit-breaker) sem depender de infra externa. Optei por lógica embarcada no gateway para manter o exemplo autocontido e fácil de inspecionar via logs.

O gateway mantém estado simples por upstream: contador de falhas consecutivas e timestamp de abertura do circuito. Em falhas transitórias ele tenta até 3 vezes com backoff incremental antes de responder com erro ao cliente; após 3 falhas consecutivas o circuito abre por ~10 segundos e as chamadas seguintes retornam 503 imediatamente, sem atingir o downstream. Essa implementação em-processo foi escolhida por simplicidade e para permitir fácil observação em logs.

Requisitos
---------
- Docker e Docker Compose

Execução
-----------
Na pasta `desafio5`:

```
docker compose up --build
```

Verificação
-----------
- Teste as rotas expostas pelo gateway:
	- `curl http://localhost:8082/users`
	- `curl http://localhost:8082/orders`

Retry e circuit-breaker
-----------------------
- Comportamento:
	- Até 3 tentativas em falhas temporárias (com backoff).
	- Após 3 falhas consecutivas o gateway abre o circuito por ~10s e responde 503 sem chamar o upstream.

Testando falhas
--------------
- Pare o serviço downstream (ex.: `orders`) e gere tráfego para observar retries e 503s:

```
for i in {1..10}; do curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8082/orders; sleep 1; done
```

- Acompanhe logs do gateway para eventos de retry/abrir-circuito:
```
docker logs -f <gateway_container_name>
```