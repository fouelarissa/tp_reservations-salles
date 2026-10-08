"""Charge des donnees de test : salles, utilisateurs, reservations.

Usage :
    python manage.py seed            # ne fait rien si des donnees existent deja
    python manage.py seed --reset    # efface salles/reservations puis recharge

Comptes crees (mot de passe commun : motdepasse123) : alice, bob, charlie
Super-utilisateur : admin / admin123
"""
from datetime import datetime, timezone

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from salles.models import Reservation, Salle

PASSWORD = "motdepasse123"


def dt(jour, heure, minute=0):
    """Date/heure UTC dans la semaine du lundi 2 novembre 2026."""
    return datetime(2026, 11, jour, heure, minute, tzinfo=timezone.utc)


class Command(BaseCommand):
    help = "Charge des donnees de test pour le TP reservations."

    def add_arguments(self, parser):
        parser.add_argument("--reset", action="store_true", help="Efface puis recharge")

    def handle(self, *args, **options):
        User = get_user_model()

        if options["reset"]:
            Reservation.objects.all().delete()
            Salle.objects.all().delete()
        elif Salle.objects.exists():
            self.stdout.write("Donnees deja presentes (utilisez --reset pour recharger).")
            return

        users = {}
        for name in ("alice", "bob", "charlie"):
            user, _ = User.objects.get_or_create(username=name)
            user.set_password(PASSWORD)
            user.save()
            users[name] = user

        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@example.com", "admin123")

        amphi = Salle.objects.create(nom="Amphi A", capacite=200, batiment="Bloc A")
        b12 = Salle.objects.create(nom="Salle B12", capacite=30, batiment="Bloc B")
        Salle.objects.create(nom="Labo Info 1", capacite=24, batiment="Bloc C")
        Salle.objects.create(nom="Salle de reunion", capacite=10, batiment="Bloc A")

        C, A = Reservation.Statut.CONFIRMEE, Reservation.Statut.ANNULEE
        rows = [
            (amphi, "alice", dt(2, 8), dt(2, 10), "Cours Django", C),
            (amphi, "bob", dt(2, 14), dt(2, 16), "Soutenance", C),
            (amphi, "alice", dt(3, 9), dt(3, 12), "Conference", C),
            (amphi, "bob", dt(4, 8), dt(4, 10), "Reunion annulee", A),
            (b12, "charlie", dt(2, 10), dt(2, 12), "TD Data Science", C),
        ]
        for salle, who, debut, fin, motif, statut in rows:
            Reservation.objects.create(
                salle=salle, utilisateur=users[who], debut=debut, fin=fin,
                motif=motif, statut=statut,
            )

        self.stdout.write(self.style.SUCCESS(
            f"{Salle.objects.count()} salles, {Reservation.objects.count()} reservations chargees."
        ))
