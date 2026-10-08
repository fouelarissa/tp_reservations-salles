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
        fields = ['nom', 'capacite', 'batiment']
    

class ReservationSerializer(serializers.ModelSerializer):

    # Le champ d'une réservation par un utilisateur
    utilisateur = serializers.ReadOnlyField(source='utilisateur.username')

    class Meta:
        model = Reservation
        fields = ['salle', 'date_debut', 'date_fin', 'motif', 'statut', 'cree_le']

    def validate(self, data):
        # Récupérèrer les données
        if 'salle' in data:
            salle = data['salle']
        elif self.instance:
            salle = self.instance.salle
        else:
            raise serializers.ValidationError("La salle est obligatoire.")
        
        # verifie si la date de debut existe ou pas
        if 'date_debut' in data:
            date_debut = data['date_debut']
        elif self.instance:
            date_debut = self.instance.date_debut
        else:
            raise serializers.ValidationError("La date de début est obligatoire.")

        # les donnees de la requete de la date de fin existe ou pas?
        if 'date_fin' in data:
            date_fin = data['date_fin']
        elif self.instance:
            date_fin = self.instance.date_fin
        else:
            raise serializers.ValidationError("La date de fin est obligatoire.")

        # le statut de la reservation
        if 'statut' in data:
            statut = data['statut']
        elif self.instance:
            statut = self.instance.statut
        else:
            statut = 'CONFIRMEE'

        # validation de cohérence des dates
        if date_debut >= date_fin:
            raise serializers.ValidationError("La date de début doit être posterieure à la date de fin.")

        #  validation de la reservation futur quelle soit en cours ou annulé
        if statut == 'ANNULEE':
            return data

        # les réservations actives ou en cours de la salle
        reservations_existantes = Reservation.objects.filter(salle=salle)
        
        # il y'a aucun créneau même si la reservation est annulée
        reservations_existantes = reservations_existantes.exclude(statut='ANNULEE')

        #on exclut la réservation elle-même pour éviter le chevauchement avec soi-même
        if self.instance:
            reservations_existantes = reservations_existantes.exclude(id=self.instance.id)

        if reservations_existantes.exists():
            raise serializers.ValidationError("La salle est déjà réservée sur ce créneau horaire.")

        return data
    