#!/bin/bash
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

docker-compose -f "${PROJECT_DIR}/docker-compose.yml" down
docker-compose -f "${PROJECT_DIR}/docker-compose.yml" build
docker-compose -f "${PROJECT_DIR}/docker-compose.yml" up

echo -e "Сайт запущен"