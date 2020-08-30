#!/bin/bash

#ローカルでのpsycopg2のインストールエラーを防ぐためrequirements.txtには記載していない
pip install django-heroku==0.3.1 --no-deps
python manage.py migrate