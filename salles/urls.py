"""Tache 3 : brancher les ViewSets sur un DefaultRouter.

Les routes attendues sont (prefixe /api/ deja fourni par config/urls.py) :
  /api/salles/            /api/salles/{id}/
  /api/reservations/      /api/reservations/{id}/
  /api/salles/{id}/occupation/
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SalleViewSet, ReservationViewSet

router = DefaultRouter()
router.register(r'salles', SalleViewSet, basename='salle')
router.register(r'reservations', ReservationViewSet, basename='reservation')

urlpatterns = [
    path('', include(router.urls)),
]

# TODO : votre code ici