from django.shortcuts import render,redirect, HttpResponse
from . import forms, models
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from rolepermissions.roles import assign_role
from rolepermissions.checkers import has_role
from ITMPE.roles import Controle
from rolepermissions.decorators import has_role_decorator
from django.core.paginator import Paginator
from datetime import date

#------------------- PÁGINAS DE DASHBOARD -------------------#
@login_required
def dashboard(request):
    avaliacoes = models.Db_Avaliacao.objects.all()
    avaliacoes_log = models.Db_Avaliacao_log.objects.all()
    secretarias = Group.objects.all()

    data_atual = date.today()
    estatistica = []
    for sec in secretarias:
        avaliacao_sec = avaliacoes.filter(responsavel = sec).order_by('-data_limite')
        avaliacao_pendente = avaliacao_sec.filter(status = "Pendente")
        print(bool (avaliacao_pendente))
        if avaliacao_pendente:
            prazo = avaliacao_pendente[0].data_limite - data_atual
            data_pendente =  '{} ({})'.format(avaliacao_pendente[0].data_limite.strftime('%d/%m/%Y'), prazo.days)
        else:
            data_pendente = 'Não há'
        estatistica.append({'secretaria': str(sec.name).replace('_',' ').capitalize(),
                            'avaliacoes_registradas': len(avaliacao_sec),
                            'avaliacoes_pendentes': len(avaliacao_pendente),
                            'avaliacoes_pendentes_datalimite': data_pendente,
                            'avaliacoes_analise': len(avaliacao_sec.filter(status="Em análise")),
                            'movimentacoes': len(avaliacoes_log.filter(avaliacao__responsavel = sec))
                            })
    
    context = {
        'estatistica': estatistica,
    }

    return render (request,'dashboard/dashboard.html',context)

#------------------- PÁGINAS DE CRITÉRIOS -------------------#
@login_required
def criterios (request):

    criterios = models.Db_Criterios.objects.all()

    criterios_paginator = Paginator(criterios,10)
    page_num_criterios = request.GET.get('page')
    page_criterios = criterios_paginator.get_page(page_num_criterios)
 
    context = {
        'criterios': page_criterios
    }
    
    return render(request, 'criterios/criterios.html',context)


#CRITÉRIO ADD
@has_role_decorator('controle')
def criterios_add (request):
    criterios_form = forms.Criterios_form(request.POST or None)

    if request.POST:
        if criterios_form.is_valid():
            criterios_form.save()
            return redirect ('criterios')

    context = {
        'criterios_form': criterios_form
    }
    return render(request, 'criterios/criterios_add.html',context)

#CRITÉRIO EDIT
@has_role_decorator('controle')
def criterios_edit(request, criterio_pk):
    criterios = models.Db_Criterios.objects.get(pk=criterio_pk)

    criterios_form = forms.Criterios_form(request.POST or None, instance = criterios)

    if request.POST:
        if criterios_form.is_valid():
            criterios_form.save()
            return redirect ('criterios')
    
    context = {
        'criterios_form': criterios_form
    }

    return render(request, 'criterios/criterios_edit.html',context)

#CRITÉRIO DELET
@has_role_decorator('controle')
def criterios_delet(request, criterio_pk):
    criterios = models.Db_Criterios.objects.get(pk=criterio_pk)
    criterios.delete()
    return redirect('criterios')


#------------------- PÁGINAS DE AVALIAÇÃO -------------------#
@login_required
def avaliacao (request):

    if has_role(request.user, Controle):
        avaliacao = models.Db_Avaliacao.objects.all()
    else:
        avaliacao = models.Db_Avaliacao.objects.filter(responsavel__in = request.user.groups.all())

    avaliacao_paginator = Paginator(avaliacao,10)
    page_num_avaliacao = request.GET.get('page')
    page_avaliacao = avaliacao_paginator.get_page(page_num_avaliacao)

    context = {
        'avaliacao': page_avaliacao
    }
    
    return render(request, 'avaliacao/avaliacao.html', context)

#AVALIAÇÃO ADD
@has_role_decorator('controle')
def avaliacao_add (request):
    avaliacao_form = forms.Avaliacao_form(request.POST or None)

    if request.POST:
        if avaliacao_form.is_valid():
            avaliacao_form.save()
            return redirect ('avaliacao')

    context = {
        'avaliacao_form': avaliacao_form
    }
    return render(request, 'avaliacao/avaliacao_add.html',context)

#AVALIAÇÃO EDIT
@has_role_decorator('controle')
def avaliacao_edit(request, avaliacao_pk):
    avaliacao = models.Db_Avaliacao.objects.get(pk=avaliacao_pk)

    avaliacao_form = forms.Avaliacao_form(request.POST or None, instance = avaliacao)

    if request.POST:
        if avaliacao_form.is_valid():
            avaliacao.arquivo = request.FILES.get('arquivo')
            avaliacao_form.save()
            return redirect ('avaliacao')
    
    context = {
        'avaliacao_form': avaliacao_form
    }

    return render(request, 'avaliacao/avaliacao_edit.html',context)

#AVALIAÇÃO DELET
@has_role_decorator('controle')
def avaliacao_delet(request, avaliacao_pk):
    avaliacao = models.Db_Avaliacao.objects.get(pk=avaliacao_pk)
    avaliacao.delete()
    return redirect('avaliacao')


#AVALIAÇÃO EDITAR
@login_required
def avaliacao_enviar(request, avaliacao_pk):
    avaliacao = models.Db_Avaliacao.objects.get(pk=avaliacao_pk)
    avaliacao_log = models.Db_Avaliacao_log(avaliacao=avaliacao)
    avaliacao_log_hist = models.Db_Avaliacao_log.objects.filter(avaliacao=avaliacao).order_by('-dataehora')
    
    avaliacao_form = forms.Avaliacao_form(request.POST or None, instance = avaliacao)

    for f in avaliacao_form.fields:
        avaliacao_form.fields[f].disabled = True
    
    if request.POST:
        if avaliacao_form.is_valid() and (request.FILES.get('arquivo') or request.POST.get('anotacao') or request.POST.get('status_controle')=='Publicado'):
            avaliacao_log.arquivo = request.FILES.get('arquivo')
            avaliacao_log.anotacao = request.POST.get('anotacao')
            avaliacao_log.usuario = request.user
            
            

            if not has_role(request.user,'controle'):
                avaliacao.status = 'Em análise'
                
            else:
                avaliacao.status = request.POST.get('status_controle')
                if avaliacao.status == 'Publicado':
                    avaliacao_log.anotacao = 'Item publicado no Portal da Transparência. Após a data limite, o prazo desta avaliação será devidamente atualizado, conforme periodicidade do critério.'


            avaliacao.save()
            avaliacao_log.save()
            
            return redirect (request.path_info)


    avaliacao_log_paginator = Paginator(avaliacao_log_hist,6)
    page_num_avaliacao_log = request.GET.get('page')
    page_avaliacao_log = avaliacao_log_paginator.get_page(page_num_avaliacao_log)

    context = {
        'avaliacao_log_hist': page_avaliacao_log,
        'avaliacao_form': avaliacao_form
    }

    return render(request, 'avaliacao/avaliacao_enviar.html',context)

#AVALIAÇÃO DELETE
@has_role_decorator('controle')
def avaliacao_log_delet(request, avaliacao_pk, avaliacao_log_pk):
    avaliacao_log = models.Db_Avaliacao_log.objects.get(pk=avaliacao_log_pk)
    avaliacao_log.delete()
    return redirect (request.META.get('HTTP_REFERER'))


# def controle(request):
#     assign_role(request.user, 'controle')
#     return HttpResponse('CONTROLE INTERNO ADICIONADO!')

# def secadm(request):
#     assign_role(request.user, 'sec_adm')
#     return HttpResponse('SECRETARIA DE ADMINISTRAÇÃO ADICIONADA!')
