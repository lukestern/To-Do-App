#!/bin/bash 
heroku container:login
docker tag "${DOCKER_USER}"/todo_app registry.heroku.com/"${HEROKU_APP}"/web
echo $DOCKER_PASSWD | docker login --username $DOCKER_USER --password-stdin
docker push registry.heroku.com/"${HEROKU_APP}"/web
heroku container:release web --app "${HEROKU_APP}"