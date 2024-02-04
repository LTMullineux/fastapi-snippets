pytest_args=$*
docker compose run --rm snippet-test $pytest_args
docker compose --profile test down --volumes
