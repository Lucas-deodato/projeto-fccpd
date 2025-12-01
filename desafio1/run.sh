#!/usr/bin/env bash
set -euo pipefail

NET_NAME=desafio1_net
SERVER_IMG=desafio1_server_img
CLIENT_IMG=desafio1_client_img

usage(){
  echo "Usage: $0 {up|down}"
}

if [ "$#" -ne 1 ]; then
  usage; exit 1
fi

cmd=$1

if [ "$cmd" = "up" ]; then
  echo "Creating network (if not exists): $NET_NAME"
  docker network ls --format '{{.Name}}' | grep -q "^${NET_NAME}$" || docker network create ${NET_NAME}

  echo "Building server image"
  docker build -t ${SERVER_IMG} ./server/

  echo "Building client image"
  docker build -t ${CLIENT_IMG} ./client

  echo "Running server container"
  docker run -d --name desafio1_server --network ${NET_NAME} -p 8080:8080 ${SERVER_IMG}

  echo "Running client container (logs will stream)"
  docker run -d --name desafio1_client --network ${NET_NAME} ${CLIENT_IMG}

  echo "Done. Server on localhost:8080. Use 'docker logs -f desafio1_client' to follow client logs."

elif [ "$cmd" = "down" ]; then
  docker rm -f desafio1_client || true
  docker rm -f desafio1_server || true
  docker network rm ${NET_NAME} || true
  docker image rm -f ${SERVER_IMG} ${CLIENT_IMG} || true
  echo "Cleaned up"
else
  usage; exit 1
fi
