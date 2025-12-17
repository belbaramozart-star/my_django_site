from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from .models import CandidateProfile, CompanyProfile, CustomUser, UserType

class LoginForm(AuthenticationForm):
    username = forms.CharField(label ='Email ou nom d\'utilisateur', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Mot de passe', strip=False, widget=forms.PasswordInput(attrs={'class':'form-control'}))

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'first_name', 'last_name')

        def __init__(self, *args, **kwargs):
            super().__init__(self, *args, **kwargs)
            if 'username' in self.fields:
                del self.fields['username']

        def save(self, commit=True):
            #print("form.save enclenché")
            # Gère la création du CustomUser et du profil associé(Candidat/Entreprise)
            user = super().save(commit=False)

            """# ---POINT DE CONTROLE 1: Etat Initial
            print("--- DEBOGAGE 1: AVANT AFFECTATION ---")
            print(f"User Email (input): {user.email}")
            print(f"User Username (input): {user.username}") # Doit etre vide ou None"""

            user.username = user.email

            """# ---POINT DE CONTROLE 2: Après Affectation
            print("--- DEBOGAGE 2: APRES AFFECTATION ---")
            print(f"User Email (input): {user.email}")
            print(f"User Username (input): {user.username}") # Doit etre user.email"""

            # l'email est utilisé comme nom d'utiilsateur par défaut si non-spécifié
            if not user.username:
                user.username = user.email

            if commit:
                user.save()
            
                """# ---POINT DE CONTROLE 3: Après Enregistrement
                print("--- DEBOGAGE 3: APRES ENREGISTREMENT ---")
                print("En l'occurence l'enregistrement a réussi")
                print(f"User Email (input): {user.email}")
                print(f"User Username (input): {user.username}") # Doit etre user.email"""

            # Création automatique du profil après l'enregistrement de l'utilisateur
            if user.user_type == UserType.CANDIDATE:
                from .models import CandidateProfile
                CandidateProfile.objects.create(user = user)
            elif user.user_type == UserType.COMPANY:
                from .models import CompanyProfile
                CompanyProfile.objects.create(user = user)
            
            return user
        
# --- 1. Formulaire du Profil Candidat ---
class CandidateProfileForm(forms.ModelForm):
    """Permet au candidat de mettre à jour son profil (CV inclus)."""
    class Meta:
        model = CandidateProfile
        fields = ('nom', 'prenom', 'ville', 'telephone', 'bio', 'cv')
        labels = {
            'cv': 'Télécharger votre CV (Fichier PDF ou DOCX)'
        }
    
    def init(self, *args, **kwargs):
        super().init(*args, **kwargs)
        # Rendre le champ CV non obligatoire pour la première modification si besoin
        self.fields['cv'].required = False 

# --- 2. Formulaire du Profil Entreprise ---
class CompanyProfileForm(forms.ModelForm):
    """Permet à l'entreprise de mettre à jour son profil."""
    class Meta:
        model = CompanyProfile
        fields = ('nom_entreprise', 'description', 'adresse', 'site_web', 'telephone')
        labels = {
            'description': 'Description de l\'entreprise',
            'site_web': 'Site Web (URL)'
        }