# export $(grep -v '^#' .env | xargs -d '\n')
# rq worker --with-scheduler --url redis://redis:6379


#!/bin/bash

cd "/workspaces/PROMPT ENGINEERING"

set -a
source .env
set +a

export PYTHONPATH=$PWD

rq worker --with-scheduler --url redis://redis:6379