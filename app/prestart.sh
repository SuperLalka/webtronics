#! /usr/bin/env bash

# Let the DB start
bash ./wait_for_postgres.sh

# Run migrations
alembic upgrade head;
