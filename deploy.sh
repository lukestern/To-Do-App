docker tag $DOCKER_USER/todo_app registry.heroku.com/$HEROKU_APP/web
heroku container:login
docker push registry.heroku.com/$HEROKU_APP/web
heroku container:release web -a $HEROKU_APP