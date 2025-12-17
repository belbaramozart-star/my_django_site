from django.db import models
from accounts.models import CustomUser
from offers.models import JobOffer

# 1.Choix du Statut de Candidature
class ApplicationStatus(models.TextChoices):
    # Statuts initiaux
    PENDING = 'PENDING', 'En attente de revue'
    REVIEW = 'REVIEW', 'En cours de revue'

    # Statuts intermédiaires
    INTERVIEW = 'INTERVIEW', 'Convoqué(e) en entretien'

    # Statuts finaux
    ACCEPTED = 'ACCEPTED', 'Accepté(e)'
    REJECTED = 'REJECTED', 'Refusé(e)'
    CANCELED = 'CANCELED', 'Annulé(e)'

# 2.Modèle Applicaion (La Candidature)
class Application(models.Model):
    # Le candidat (CustomUser)
    candidat = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='candidatures', 
    limit_choices_to={'user_type': 'CANDIDAT'}, verbose_name='Candidat')
    # L'offre à laquelle le candiadt postule
    offer = models.ForeignKey(JobOffer, on_delete=models.CASCADE, related_name='applications', verbose_name="Offre d'Emploi/Stage")
    # Lettre de motivation de motivation spécifique à l'offre (les CVsont sur le profil)
    lettre_motivation = models.FileField(upload_to='lettre_motivation/', null=True, blank=True, verbose_name="Lettre de Motivation")
    # Statut actuel de la candidature
    statut = models.CharField(max_length=10, choices=ApplicationStatus.choices, default=ApplicationStatus.PENDING, verbose_name="Statut Actuel")
    # Commentaires(visibles par l'entreprise)
    commentaires = models.TextField(blank=True, verbose_name="Notes de l'Entreprise")

    date_soumission = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Candidature pour {self.offer.titre} par {self.candidat.email}"
    
    class Meta:
        # Empecher un candidat de postuler 02 fois à la meme offre
        unique_together = ('candidat', 'offer')

        ordering = ['-date_soumission']
        verbose_name = "Candidature"
        verbose_name_plural = "Candidatures"

# 3. Modèle ApplicationHistory (Historique de Suivi) -- Enregistre les changements de statut de candidature
class ApplicationHistory(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='history', verbose_name="Candidature")
    old_status = models.CharField(max_length=10, choices=ApplicationStatus.choices, verbose_name="Ancien Statut")
    new_status = models.CharField(max_length=10, choices=ApplicationStatus.choices, verbose_name="Nouveau Statut")
    # Qui a effectué le changement(Admin/Recruteur)
    changed_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Modifié par")
    date_changement = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Changement de statut pour {self.application.id} le {self.date_changement.strftime('%Y -%m-%d')}"
    
    class Meta:
        ordering = ['-date_changement']
        verbose_name = "Historiquement de Candidature"
        verbose_name_plural = "Historiques de Candidatures"
