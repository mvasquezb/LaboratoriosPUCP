#!/usr/bin/env sh

python3 laboratorios/manage.py shell	"import django\
										django.setup()\
										from internal.models import *\
										essayt1=EssayTemplate(code=1,test_number=2,description='essayt1')\
										essayt1.save()\
										"