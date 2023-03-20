#!/bin/bash

set -e -o pipefail  # exit on errors

echo "[INIT] Create project directory"

cd myproject

echo "[INIT] Create virtual environment"
virtualenv env --python=/usr/bin/python3
source env/bin/activate
python -V

echo "[INIT] Start new Django project based on template"
env/bin/pip install django
mkdir -p foo
django-admin startproject \
    --template=https://bitbucket.org/maykinmedia/default-project/get/master.zip  \
    --extension=py,rst,html,gitignore,json,ini,js,sh,cfg,yml,example \
    --name Dockerfile foobar foo

echo "[INIT] Create pinned requirements"
# https://github.com/jazzband/pip-tools/issues/1558 pip 22.0 breaks pip-tools
env/bin/pip install pip setuptools --upgrade
env/bin/pip install pip-tools

cd foo
git init
./bin/compile_dependencies.sh

echo "[INIT] Done."
deactivate

echo "[INSTALL] Typical first steps in the new project"
# python bootstrap.py jenkins
# Replaced bootstrap.py with classic commands:
source ../env/bin/activate
../env/bin/pip install -r requirements/dev.txt
export DJANGO_SETTINGS_MODULE=foobar.conf.jenkins
# End classic commands.
../env/bin/python src/manage.py collectstatic --link --noinput
# python src/manage.py migrate --noinput
../env/bin/python src/manage.py check
deactivate

echo "[JENKINS] Execute Jenkins script"
../env/bin/python src/manage.py jenkins \
  --project-apps-tests \
  --verbosity 2 \
  --noinput \
  --coverage-rcfile=.coveragerc \
  --enable-coverage
