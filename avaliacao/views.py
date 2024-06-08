from django.shortcuts import render,redirect, HttpResponse
from . import forms, models
from django.contrib.auth.decorators import login_required
from rolepermissions.roles import assign_role
from rolepermissions.checkers import has_role
from ITMPE.roles import Controle
from rolepermissions.decorators import has_role_decorator


#PÁGINAS DE DASHBOARD#
@login_required
def dashboard(request):
    criterios = models.Db_Criterios.objects.all()
    avaliacoes = models.Db_Avaliacao.objects.all()
    avaliacoes_log = models.Db_Avaliacao_log.objects.all()

    context = {
        'criterios_len': len(criterios),
        'avaliacoes_len': len(avaliacoes),
        'avaliacoeslog_len': len(avaliacoes_log),
    }

    for grupo in request.user.groups.all():
        context['criterio_sec'] = len(criterios)
        context['avaliacao_sec'] = len(avaliacoes.filter(responsavel = grupo.id))
        context['avaliacao_log_sec'] = len(avaliacoes_log.filter(avaliacao__responsavel = grupo.id))
        context['sec'] = str(grupo).replace('_',' ').capitalize()

    return render (request,'dashboard/dashboard.html',context)

#PÁGINAS DE CRITÉRIOS#
@login_required
def criterios (request):

    criterios = models.Db_Criterios.objects.all()
    #if has_role(request.user, Controle):
    #    criterios = models.Db_Criterios.objects.all()
    #else:
    #    criterios = models.Db_Criterios.objects.filter(responsavel__in = request.user.groups.all())
 
    context = {
        'criterios': criterios
    }
    
    return render(request, 'criterios/criterios.html',context)


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

@has_role_decorator('controle')
def criterios_delet(request, criterio_pk):
    criterios = models.Db_Criterios.objects.get(pk=criterio_pk)
    criterios.delete()
    return redirect('criterios')

#PÁGINAS DE AVALIAÇÃO#
@login_required
def avaliacao (request):

    if has_role(request.user, Controle):
        avaliacao = models.Db_Avaliacao.objects.all()
    else:
        avaliacao = models.Db_Avaliacao.objects.filter(responsavel__in = request.user.groups.all())

    context = {
        'avaliacao': avaliacao
    }
    
    return render(request, 'avaliacao/avaliacao.html', context)


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

@has_role_decorator('controle')
def avaliacao_delet(request, avaliacao_pk):
    avaliacao = models.Db_Avaliacao.objects.get(pk=avaliacao_pk)
    avaliacao.delete()
    return redirect('avaliacao')

def avaliacao_enviar(request, avaliacao_pk):
    avaliacao = models.Db_Avaliacao.objects.get(pk=avaliacao_pk)
    avaliacao_log = models.Db_Avaliacao_log(avaliacao=avaliacao)
    avaliacao_log_hist = models.Db_Avaliacao_log.objects.filter(avaliacao=avaliacao).order_by('-dataehora')
    
    avaliacao_form = forms.Avaliacao_form(request.POST or None, instance = avaliacao)

    for f in avaliacao_form.fields:
        avaliacao_form.fields[f].disabled = True
        avaliacao_form.fields[f].required = False
    
    if request.POST:
        if avaliacao_form.is_valid() and (request.FILES.get('arquivo') or request.POST.get('anotacao')):
            avaliacao_log.arquivo = request.FILES.get('arquivo')
            avaliacao_log.anotacao = request.POST.get('anotacao')
            avaliacao_log.usuario = request.user
            avaliacao_log.save()
            

            if not has_role(request.user,'controle'):
                print('status deve ser alterado')
                avaliacao.status = 'Em análise'
                avaliacao.save()
            else:
                print('status deve ser alterado')
                avaliacao.status = request.POST.get('status_controle')
                avaliacao.save()

            print(avaliacao.status)
            
            return redirect (request.path_info)


    context = {
        'avaliacao_log_hist': avaliacao_log_hist,
        'avaliacao_form': avaliacao_form
    }

    return render(request, 'avaliacao/avaliacao_enviar.html',context)

@has_role_decorator('controle')
def avaliacao_log_delet(request, avaliacao_pk, avaliacao_log_pk):
    avaliacao_log = models.Db_Avaliacao_log.objects.get(pk=avaliacao_log_pk)
    avaliacao_log.delete()
    return redirect (request.META.get('HTTP_REFERER'))


def controle(request):
    assign_role(request.user, 'controle')
    return HttpResponse('CONTROLE INTERNO ADICIONADO!')

def secadm(request):
    assign_role(request.user, 'sec_adm')
    return HttpResponse('SECRETARIA DE ADMINISTRAÇÃO ADICIONADA!')
