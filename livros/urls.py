from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LivroViewSet, AutorViewSet

router = DefaultRouter()
router.register('livros', LivroViewSet)
router.register('autores', AutorViewSet) # Novo endpoint

urlpatterns = [
    path('', include(router.urls)),
]
