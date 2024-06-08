from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

html_content = render_to_string('emails/prazo_avaliacao.html', {'criterio':'1.1 - TESTE', 'data_limite':'11/10/2024'})
text_content = strip_tags(html_content)

email = EmailMultiAlternatives('NOTIFICAÇÃO: Avaliação Continuada - ITMPe',text_content, settings.EMAIL_HOST_USER,['sostenesilvaa@gmail.com'])
email.attach_alternative(html_content,'text/html')
email.send()