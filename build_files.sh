#!/bin/bash

python3.9 -m pip install -r requirements.txt
python3.9 manage.py collectstatic
python3.9 manage.py makemigrations mini_fb
python3.9 manage.py migrate