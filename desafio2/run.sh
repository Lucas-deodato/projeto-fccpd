#!/usr/bin/env bash
set -euo pipefail

VOLUME_NAME=desafio2_pgdata
CONTAINER_NAME=desafio2_db
POSTGRES_PASSWORD=examplepass

usage(){
  echo "Usage: $0 {up|stop|start|down|psql}"
}

if [ "$#" -ne 1 ]; then
  usage; exit 1
fi

case "$1" in
  up)
    docker volume create ${VOLUME_NAME} || true
    docker run -d --name ${CONTAINER_NAME} -e POSTGRES_PASSWORD=${POSTGRES_PASSWORD} -v ${VOLUME_NAME}:/var/lib/postgresql/data -p 5432:5432 postgres:15
    echo "Waiting for DB to be ready..."
    sleep 5
    docker exec -i ${CONTAINER_NAME} psql -U postgres <<'SQL'
CREATE TABLE IF NOT EXISTS notes(id SERIAL PRIMARY KEY, text TEXT);
INSERT INTO notes(text) VALUES('Primeira nota persistida');
SQL
    echo "DB initialized and sample data inserted."
    ;;
  stop)
    docker stop ${CONTAINER_NAME} || true
    docker rm ${CONTAINER_NAME} || true
    echo "Container removed, volume remains: ${VOLUME_NAME}"
    ;;
  start)
    docker run -d --name ${CONTAINER_NAME} -e POSTGRES_PASSWORD=${POSTGRES_PASSWORD} -v ${VOLUME_NAME}:/var/lib/postgresql/data -p 5432:5432 postgres:15
    echo "Started container using existing volume"
    ;;
  down)
    docker rm -f ${CONTAINER_NAME} || true
    docker volume rm ${VOLUME_NAME} || true
    echo "Removed container and volume"
    ;;
  psql)
    docker exec -it ${CONTAINER_NAME} psql -U postgres
    ;;
  *) usage; exit 1 ;;
esac
