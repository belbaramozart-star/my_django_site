from django.db import models

# Stocke les messages envoyés via le formulaire de contact
class ContactMessage(models.Model):
    nom_expediteur = models.CharField(max_length=50)
    email_expediteur = models.EmailField()
    sujet = models.CharField(max_length=150)
    date_envoi = models.DateTimeField(auto_now_add=True)
    traite = models.BooleanField(default=False)

    def __str__(self):
        return f"Message de {self.nom_expediteur} - {self.sujet}"
