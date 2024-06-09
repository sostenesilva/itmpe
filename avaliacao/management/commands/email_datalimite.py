from django.core.management.base import BaseCommand, CommandError
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.template.loader import get_template
from django.utils.html import strip_tags
from django.conf import settings
from datetime import date
import os
import sys

caminho_absoluto = os.path.abspath('.')
sys.path.insert(0,caminho_absoluto)

from avaliacao import models


class Command(BaseCommand):
    help = 'Enviar email de notificação para data de avaliações'

    def handle(self, *args, **options):

        data_atual = date.today()
        avaliacoes_pendentes = models.Db_Avaliacao.objects.filter(status = 'Pendente')
        Bd_email = models.Email_group.objects.all()
        
        for email in Bd_email:
            avaliacoes_group = avaliacoes_pendentes.filter(responsavel = email.group).order_by('data_limite')
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

        self.stdout.write(self.style.SUCCESS('Email enviado com sucess!'))