#!/bin/bash
set -e

source .env
git pull
docker compose -f docker-compose.prod_ssl.yml build
docker compose -f docker-compose.prod_ssl.yml up -d
git_revision=$(git rev-parse HEAD)
echo $ROLLBAR_ACCESS_TOKEN
curl --request POST \
     --url https://api.rollbar.com/api/1/deploy \
     --header 'X-Rollbar-Access-Token: '$ROLLBAR_ACCESS_TOKEN'' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '{"environment": "'$ROLLBAR_ENVIRONMENT'", "revision": "'$git_revision'"}'

echo success deploy!!!