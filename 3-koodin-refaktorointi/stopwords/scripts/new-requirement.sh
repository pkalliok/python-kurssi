#!/bin/sh

. myenv/bin/activate
pip install "$@"
git stash
pip freeze > requirements.txt
git commit -am "New requirement: $*"
git stash pop

