from django.urls import path, include
from rest_framework import routers
from tarefa import views

# Criação de um roteador para as rotas automáticas
router = routers.DefaultRouter()
router.register(r'tarefas', views.TarefaViewSet)

# Definição das rotas
urlpatterns = [
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("", include(router.urls)),  # Inclui as rotas geradas pelo roteador
]
