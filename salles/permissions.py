"""Tache 4 : permissions personnalisees.

A FAIRE :
  - IsOwnerOrReadOnly : lecture pour tous, modification/suppression
    reservee a l'auteur de la reservation (obj.utilisateur).
"""
from rest_framework import permissions  # noqa: F401  (a utiliser)

class IsOwnerOrReadOnly(permissions.BasePermission):
     def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.utilisateur == request.user

# Permission personnalisée pour les Salles.
class IsStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff     

# TODO : votre code ici
