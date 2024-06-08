from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group

class Db_dimensao (models.Model):
    dimensao = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.dimensao

class Db_Criterios(models.Model):
    item = models.CharField(null=True,max_length=6)
    criterio = models.TextField(null=True)
    dimensao = models.ForeignKey(Db_dimensao, on_delete=models.PROTECT, blank=True, null=True)
    periodicidade = models.CharField(max_length=20, null=True, choices=[('Mensal','Mensal'),('Bimestral','Bimestral'),('Trimestral','Trimestral'),('Quadrimestral','Quadrimestral'),('Semestral','Semestral'),('Anual','Anual'),('Tempestivo','Tempestivo')])

    def __str__(self):
        return 'Item {} - {}'.format(self.item,self.criterio)

def diretorioItemAvaliacao(instance, filename): 
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename> 
    return 'criterios/{} - {}/{}/{}/{}'.format(instance.avaliacao.criterio.item,instance.avaliacao.criterio.criterio.replace('?','')[:30],instance.avaliacao.responsavel,instance.avaliacao.data_limite,filename)

class Db_Avaliacao (models.Model):
    criterio = models.ForeignKey(Db_Criterios,on_delete=models.PROTECT)
    data_limite = models.DateField(null=True, blank=True)
    responsavel = models.ForeignKey(Group, null=True,on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=[('Pendente','Pendente'),('Em análise','Em análise'),('Publicado','Publicado')], default=('Pendente','Pendente'))

    def __str__(self):
        return 'Item {} - {} ({})'.format(self.criterio.item,self.data_limite,self.responsavel)

class Db_Avaliacao_log (models.Model):
    avaliacao = models.ForeignKey(Db_Avaliacao,on_delete=models.CASCADE)
    arquivo = models.FileField(null=True, blank=True, upload_to= diretorioItemAvaliacao)
    anotacao = models.TextField(null=True,blank=True)
    dataehora = models.DateTimeField(auto_now=True,blank=True,null=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.PROTECT)


    

