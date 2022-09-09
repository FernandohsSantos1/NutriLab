from django.contrib import admin
from .models import Ativacao

#Faz com que a tabela ativacao criada em models.py seja acessada pela area administrativa do django
admin.site.register(Ativacao)
