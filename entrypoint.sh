#!/bin/bash

if [ -z "$MODEL" ]; then
  echo "Error: MODEL environment variable is not set."
  exit 1
fi

exec poetry run python "mlops/models/$MODEL/train.py" "$@"
