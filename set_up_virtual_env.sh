#!/bin/bash

if ! [[ -z "${VIRTUAL_ENV}" ]]; then
  echo "already in virtual env"
  exit
fi

ENV_FILE=venv/bin/activate
if test -f "$ENV_FILE"; then
	echo "$ENV_FILE exists."
else
	python3 -m venv venv
fi

source "$ENV_FILE"
pip3 install -r requirements.txt

export MPLBACKEND=Agg

