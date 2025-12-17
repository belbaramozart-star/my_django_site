from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

# Définition des types d'utilisateurs
class UserType(models.TextChoices):
    CANDIDATE = 'CANDIDAT', 'Candidat'
    COMPANY = 'ENTREPRISE', 'Entreprise'

# Gestionnaire d'utilisateurs
class CustomUserManager(BaseUserManager):
    """
        Gestionnaire personnalisé pour la création d'utilisateurs et de super-utilisateurs
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'addresse email doit etre fournie")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True.')
        
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name='Addresse Email')
    first_name = models.CharField(max_length=150, blank=True, verbose_name='Prénom')
    last_name = models.CharField(max_length=150, blank=True, verbose_name='Nom')
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    user_type = models.CharField(max_length=15, choices=UserType.choices, default=UserType.CANDIDATE, verbose_name="Type de compte")
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    #has_profile = models.BooleanField(default=False)
    objects = CustomUserManager()

    # Définit le champ utilisé pour la connexion
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    # Champ requis désormais lors de la création d'un super-utilisateur (en ligne de commande)
    # L'email sera requis car c'est le USERNAME_FIELD
    REQUIRED_FIELDS = ['first_name', 'last_name',]

    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'
    
    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
class CandidateProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, limit_choices_to={'user_type': UserType.CANDIDATE})
    nom = models.CharField(max_length=100, blank=True)
    prenom = models.CharField(max_length=100, blank=True)
    ville = models.CharField(max_length=100, blank=True)
    telephone = models.CharField(max_length=100, blank=True)
    cv = models.FileField(upload_to='cvs/', blank=True, null=True)
    bio = models.TextField(blank=True, verbose_name="Biographie")

    def __str__(self):
        return f"Profil de {self.user.get_full_name() or self.user.email}"
    
class CompanyProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, limit_choices_to={'user_type': UserType.COMPANY})
    nom_entreprise = models.CharField(max_length=100, unique=True)
    adresse = models.CharField(max_length=255, blank=True, verbose_name="Addresse")
    secteur_activite = models.CharField(max_length=255)
    description = models.TextField(verbose_name="Description de l'entreprise")
    site_web = models.URLField(max_length=200, null=True)
    telephone = models.CharField(max_length=100, blank=True)

