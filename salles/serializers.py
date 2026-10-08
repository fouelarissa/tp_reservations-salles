"""Tache 1 et 2 : serializers et validation.

A FAIRE :
  - SalleSerializer (ModelSerializer)
  - ReservationSerializer (ModelSerializer) :
      * le champ `utilisateur` est en LECTURE SEULE (il sera renseigne par la vue)
      * validation : `fin` strictement apres `debut`
      * validation : pas de chevauchement avec une autre reservation CONFIRMEE
        de la meme salle
"""
from rest_framework import serializers

from .models import Reservation, Salle  # noqa: F401  (a utiliser)

class SalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salle
        fields = ["id", "nom", "capacite", "batiment"]

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ["id", "salle", "utilisateur", "debut", "fin", "motif", "statut", "cree_le"]
        read_only_fields = ["utilisateur", "cree_le"]

    def validate(self, data):
        instance = self.instance
        salle = data.get("salle", instance.salle if instance else None)
        debut = data.get("debut", instance.debut if instance else None)
        fin = data.get("fin", instance.fin if instance else None)
        statut = data.get(
            "statut", instance.statut if instance else Reservation.Statut.CONFIRMEE
        )

        if fin <= debut:
            raise serializers.ValidationError(
                "l'heure de fin doit être posterieure à l'heure de debut."
            )

        if statut == Reservation.Statut.CONFIRMEE:
            conflits = Reservation.objects.filter(
                salle=salle,
                statut=Reservation.Statut.CONFIRMEE,
                debut__lt=fin,
                fin__gt=debut,
            )
            if instance:
                conflits = conflits.exclude(pk=instance.pk)
            if conflits.exists():
                raise serializers.ValidationError(
                    "Cette salle est deja reservee sur ce creneau."
                )
        return data

# TODO : votre code ici
