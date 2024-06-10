from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from datetime import date, timedelta
from django.contrib.auth.models import User
import os
import sys
caminho_absoluto = os.path.abspath('.')
sys.path.insert(0,caminho_absoluto)
from avaliacao import models


class Command(BaseCommand):
    help = 'Avaliar data limite de avaliações'

    def handle(self, *args, **options):

        periodicidade = {
            'Mensal': timedelta(days=30),
            'Bimestral': timedelta(days=2*30),
            'Trimestral': timedelta(days=3*30),
            'Quadrimestral': timedelta(days=4*30),
            'Semestral': timedelta(days=6*30),
            'Anual': timedelta(days=365),
        }

        sistema, create_sistema = User.objects.get_or_create(username='sistema', defaults={'password': 'stn123456'})
        sistema.save()

        data_atual = date.today()
        avaliacoes = models.Db_Avaliacao.objects.all()
        for avaliacao in avaliacoes:
            prazo = avaliacao.data_limite - data_atual
            prazo = prazo.days

            if prazo == -1:
                if avaliacao.status == "Pendente":
                    log_avaliacao = models.Db_Avaliacao_log(avaliacao = avaliacao,anotacao = 'Prazo para envio das informações finalizado: a entrega não foi efetivada. Data para nova entrega será renovada conforme periodicidade do critério.', usuario=sistema)
                    log_avaliacao.save()
                elif avaliacao.status == "Em análise":
                    log_avaliacao = models.Db_Avaliacao_log(avaliacao = avaliacao,anotacao = 'Prazo para envio das informações finalizado: a entrega anterior está em análise. Data para nova entrega será renovada conforme periodicidade do critério.', usuario=sistema)
                    log_avaliacao.save()

                avaliacao.data_limite += periodicidade[avaliacao.criterio.periodicidade]

                log_avaliacao = models.Db_Avaliacao_log(avaliacao = avaliacao,anotacao = 'Novo ciclo de avaliação: data limite atualizada para {}'.format(avaliacao.data_limite.strftime('%d/%m/%Y')), usuario=sistema)
                log_avaliacao.save()
                avaliacao.status='Pendente'
                avaliacao.save()
                    
        self.stdout.write(self.style.SUCCESS('Datas, prazos e status das avaliações atualizados com sucesso!'))