#!/usr/bin/env bash

set -e

USAGE="Usage: python3 build_isolated.py"

if [ -d venv ]; then
  echo "$USAGE"
  exit 1
fi

if [ -d .git ]; then
  echo "$USAGE"
  exit 1
fi

git init
git add .
git commit -m "foreign build dummy commit"

python3 -m venv venv
source venv/bin/activate
make install
make test