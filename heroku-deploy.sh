#!/bin/bash 

mv /app/.netrc ~/.netrc

heroku container:login
docker tag "${DOCKER_USER}"/todo_app registry.heroku.com/"${HEROKU_APP}"/web
docker login --username=_ --password="${HEROKU_KEY}" registry.heroku.com
docker push registry.heroku.com/"${HEROKU_APP}"/web
heroku container:release web --app "${HEROKU_APP}"