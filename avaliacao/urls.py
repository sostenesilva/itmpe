from django.urls import path
from . import views
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('avaliacao', views.avaliacao, name='avaliacao'),
    path('adicionar/', views.avaliacao_add, name='avaliacao_add'),
    path('avaliacao/editar/<int:avaliacao_pk>', views.avaliacao_edit, name='avaliacao_edit'),
    path('avaliacao/deletar/<int:avaliacao_pk>', views.avaliacao_delet, name='avaliacao_delet'),
    path('avaliacao/anexar/<int:avaliacao_pk>/', views.avaliacao_enviar, name='avaliacao_enviar'),
    path('avaliacao/anexar/<int:avaliacao_pk>/deletar/<int:avaliacao_log_pk>', views.avaliacao_log_delet, name='avaliacao_log_delet'),

    path('criterios/', views.criterios, name='criterios'),
    path('criterios/adicionar/', views.criterios_add, name='criterios_add'),
    path('criterios/editar/<int:criterio_pk>', views.criterios_edit, name='criterios_edit'),
    path('criterios/deletar/<int:criterio_pk>', views.criterios_delet, name='criterios_delet'),

    # path('controle/', views.controle, name='controle'),
    # path('secadm/', views.secadm, name='secadm'),
]