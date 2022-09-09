from django.db import models
from django.contrib.auth.models import User

#Criar tabela Ativação no banco de dados para salvar os tokens
class Ativacao(models.Model):
    token = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    ativo = models.BooleanField(default=False)

    #Função para exibir o nome do usuário quando sua instância é chamada
    def __str__(self):
        return self.user.username