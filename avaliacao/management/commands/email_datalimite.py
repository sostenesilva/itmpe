from django.core.management.base import BaseCommand, CommandError
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

class Command(BaseCommand):
    help = 'Enviar email de notificação para data de avaliações'

    def handle(self, *args, **options):
        html_content = render_to_string('emails/prazo_avaliacao.html', {'criterio':'1.1 - TESTE', 'data_limite':'11/10/2024'})
        text_content = strip_tags(html_content)

        email = EmailMultiAlternatives('NOTIFICAÇÃO: Avaliação Continuada - ITMPe',text_content, settings.EMAIL_HOST_USER,['sostenesilvaa@gmail.com'])
        email.attach_alternative(html_content,'text/html')
        email.send()

        self.stdout.write(self.style.SUCCESS('Email enviado com sucess!'))