from django.db import models
from accounts.models import CompanyProfile
from taggit.managers import TaggableManager
from datetime import date, timedelta

class Skill(models.Model):
    nom = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name = "Compétence"
        verbose_name_plural = "Compétences"

class OfferType(models.Model):
    nom = models.CharField(max_length=50, unique=True, verbose_name="Type d'Offre")

    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name = "Type d'Offre"
        verbose_name_plural = "Types d'Offres"

class ContractType(models.TextChoices):
    CDI = 'CDI', 'contract à Durée Indéterminée'
    CDD = 'CDD', 'Contract à Durée Déterminée'
    INTERIM = 'INTERIM', 'Intérim'
    STAGE = 'STAGE', 'Stage'
    FREELANCE = 'FREELANCE', 'Freelance/ Consultant'

class JobOffer(models.Model):
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, related_name='published_offers', verbose_name='Entreprise')
    #offer_type = models.ForeignKey(OfferType, on_delete=models.SET_NULL, null=True, verbose_name="Type d'Opportunité")
    required_skills = TaggableManager(related_name='job_offers', verbose_name="Compétences Requises", help_text='', blank=True)
    titre = models.CharField(max_length=255)
    description = models.TextField()
    exigences = models.TextField(verbose_name="Exigences/ Qualifications")
    contract_type = models.CharField(max_length=15, choices=ContractType.choices, default=ContractType.STAGE, verbose_name="Type de contract")
    remuneration = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Rémunération")
    localisation = models.CharField(max_length=100, verbose_name="Ville/ Région")
    date_publication = models.DateField(auto_now_add=True)
    date_expiration = models.DateField(verbose_name="Date Limite de Candidature", default=date.today()+timedelta(days=30))
    is_active = models.BooleanField(default=True, verbose_name="Active")

    def __str__(self):
        return f"{self.titre} chez {self.company.nom_entreprise}"
    
    class Meta:
        ordering = ['-date_publication']
        verbose_name = "Offre"
        verbose_name_plural = "Offres"
