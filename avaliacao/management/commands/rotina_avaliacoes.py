from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from datetime import date, timedelta
from django.contrib.auth.models import User
import os
import sys

caminho_absoluto = os.path.abspath('.')
sys.path.insert(0,caminho_absoluto)

from avaliacao import models


class Command(BaseCommand):
    help = 'Enviar email de notificação para data de avaliações e atualizar as datas limites'

    def handle(self, *args, **options):

        data_atual = date.today()
        avaliacoes_pendentes = models.Db_Avaliacao.objects.filter(status = 'Pendente')
        Bd_email = models.Email_group.objects.all()
        
        for email in Bd_email:
            avaliacoes_group = avaliacoes_pendentes.filter(responsavel = email.group).order_by('data_limite')
            if avaliacoes_group:
                prazo = avaliacoes_group[0].data_limite - data_atual
                prazo = prazo.days
                if prazo == 15 or prazo == 7 or prazo == 3 or prazo == 1:
                    lista_avaliacoes = []
                    for avaliacao in avaliacoes_group:
                        lista_avaliacoes += ['Data limite: {}/{}/{} - {}'.format(avaliacao.data_limite.day,avaliacao.data_limite.month,avaliacao.data_limite.year,avaliacao.criterio)]

                    context = {
                        'lista_avaliacoes': lista_avaliacoes,
                        'prazo':prazo,
                    }

                    #html_replace = get_template('emails/prazo_avaliacao.html').template
                    html_content = render_to_string('emails/prazo_avaliacao.html',context)
                    text_content = strip_tags(html_content)
                    
                    if prazo == 1:
                        dias = '1 dia'
                    else:
                        dias = '{} dias'.format(prazo)
                    
                    email = EmailMultiAlternatives('ITMPe - {} para envio de informações'.format(dias), text_content, settings.EMAIL_HOST_USER, [email.email_group])
                    email.attach_alternative(html_content,'text/html')
                    email.send()
            
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


        self.stdout.write(self.style.SUCCESS('Email enviado com sucesso! Datas, prazos e status das avaliações atualizados com sucesso!'))