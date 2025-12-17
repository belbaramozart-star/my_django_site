from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CandidateProfileForm, CompanyProfileForm, LoginForm, CustomUserCreationForm
from .models import CandidateProfile, CompanyProfile, UserType
from offers.models import JobOffer
from applications.models import Application

def login_user(request):
    """
    Gère la connexion de l'utilisateur (Candidat ou Entreprise).
    """
    if request.user.is_authenticated:
        # Si l'utilisateur est déjà connecté, le rediriger immédiatement
        if request.user.user_type == UserType.CANDIDATE:
            return redirect('applications:candidate_dashboard')
        elif request.user.user_type == UserType.COMPANY:
            return redirect('accounts:company_dashboard')
        else:
            return redirect('accounts:index') # Retour à l'accueil pour les admins/autres
        
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            # 1. Authentification
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            # Utilise l'email comme nom d'utilisateur dans notre CustomUser
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                # 2. Connexion réussie
                login(request, user)
                
                messages.success(request, f"Connexion réussie ! Bienvenue, {user.email}.")
                
                # 3. Redirection basée sur le type d'utilisateur
                if user.user_type == UserType.CANDIDATE:
                    return redirect('applications:candidate_dashboard')
                elif user.user_type == UserType.COMPANY:
                    return redirect('accounts:company_dashboard')
                else:
                    return redirect('core:index')
            
            # Ce bloc est rarement atteint si form.is_valid() a déjà géré l'échec d'authentification
            else:
                messages.error(request, "Erreur d'authentification. Vérifiez vos identifiants.")
        
        # Si le formulaire n'est pas valide (e.g., champs manquants)
        else:
            messages.error(request, "Email ou mot de passe invalide.")
    
    else:
        # Affichage du formulaire initial (méthode GET)
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})
        

def logout_user(request):
    logout(request)
    messages.info(request, "Vous êtes déconnecté. À bientôt !")
    return redirect("core:index")

def register_user(request, user_type):
    """
    Gère l'inscription d'un nouvel utilisateur (Candidat ou Entreprise) 
    et crée automatiquement son profil associé.
    """
    # Dans le cas ou l'utilisateur est deja connecte
    if request.user.is_authenticated:
        if request.user.user_type == UserType.CANDIDATE:
            return redirect('applications:candidate_dashboard')

        elif  request.user.user_type == UserType.COMPANY:
            return redirect('accounts:company_dashboard.html')

    # 1. Vérification du type d'utilisateur
    if user_type == 'candidat':
        type_choice = UserType.CANDIDATE
        dashboard_name = 'applications:candidate_dashboard'
        
    elif user_type == 'entreprise':
        type_choice = UserType.COMPANY
        dashboard_name = 'accounts:company_dashboard'
        
    else:
        messages.error(request, "Type d'utilisateur invalide.")
        return redirect('accounts:register', user_type='candidate') # Redirige vers la sélection de type
        

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        # DEBOGAGE VUE 1: On vérifie si la validation est lancée
        #print("VUE: Formulaire en cours de validation")
        if form.is_valid():

            # DEBOGAGE VUE 2: Si cela s'affiche, forms.py.save() est appelé
            print("VUE: Validation réussie, form.save va etre appelée")

            # Ne pas sauvegarder immédiatement pour injecter le type d'utilisateur
            user = form.save(commit=False)

            """# ---POINT DE CONTROLE 1: Etat Initial
            print("--- DEBOGAGE 1: AVANT AFFECTATION ---")
            print(f"User Email (input): {user.email}")
            print(f"User Username (input): {user.username}") # Doit etre vide ou None"""

            # Définition forcée de username
            user.username = user.email

            """ # ---POINT DE CONTROLE 2: Après Affectation
            print("--- DEBOGAGE 2: APRES AFFECTATION ---")
            print(f"User Email (input): {user.email}")
            print(f"User Username (input): {user.username}") # Doit etre user.email

            # DEBOGAGE VUE 2: Si cela s'affiche, forms.py.save() est appelé
            print("VUE: Validation réussie, form.save(commit=False) a été appelée")"""

            # 🚨 Injection du type d'utilisateur 🚨
            user.user_type = type_choice 
            user.save()

            # DEBOGAGE VUE 2: Si cela s'affiche, forms.py.save() est appelé
            #print("VUE: Validaation réussie user.save() a été appelée")
            
            """ # ---POINT DE CONTROLE 3: Après Enregistrement
            print("--- DEBOGAGE 3: APRES ENREGISTREMENT ---")
            print("En l'occurence l'enregistrement a réussi")
            print(f"User Email (input): {user.email}")
            print(f"User Username (input): {user.username}") # Doit etre user.email
            """
            # 3. Création automatique du Profil
            # Lier l'utilisateur à son profil spécifique (Candidat ou Entreprise)
            
            if user.user_type == UserType.CANDIDATE:
                # Création du profil Candidat avec les valeurs minimales
                CandidateProfile.objects.create(
                    user=user, 
                    nom=user.last_name or 'N/A', # Utilise les champs User si existants
                    prenom=user.first_name or 'N/A'
                )
            
            elif user.user_type == UserType.COMPANY:
                # Création du profil Entreprise avec le nom de l'entreprise
                CompanyProfile.objects.create(
                    user=user,
                    nom_entreprise=form.cleaned_data.get('nom_entreprise', user.email) 
                    # S'assurer d'adapter l'obtention du nom de l'entreprise si nécessaire
                )

            # Connexion et redirection
            # 🚨 NOTE : L'importation et l'appel de 'login' est nécessaire ici
            from django.contrib.auth import login
            login(request, user)
            
            messages.success(request, f"Compte créé avec succès ! Bienvenue.")
            return redirect(dashboard_name)
        """else:
            # DEBOGAGE VUE 3: Si cela s'affiche, la validation du formulaire a échoué
            print("VUE: Validation échouée. Erreurs: ", form.erros.as_data())"""
    
    else:
        # Affichage du formulaire vide (méthode GET)
        form = CustomUserCreationForm()

    context = {
        'form': form,
        'user_type_label': user_type.capitalize(),
    }

    return render(request, "accounts/register.html", context)

@login_required
def company_dashboard(request):
    """
    Affiche le tableau de bord pour l'utilisateur de type Entreprise.
    """
    user = request.user
    
    # 🚨 1. Vérification du type d'utilisateur
    if user.user_type != UserType.COMPANY:
        messages.error(request, "Accès refusé. Cette page est réservée aux Entreprises.")
        return redirect('core:index')

    # Récupération du profil d'entreprise (CompanyProfile)
    company_profile = user.companyprofile

    # 2. Récupération des données d'activité
    
    # Offres publiées par cette entreprise
    published_offers = JobOffer.objects.filter(company=company_profile).order_by('-date_publication')
    
    # Candidatures totales reçues pour TOUTES les offres de cette entreprise
    # On utilise la relation inverse définie dans JobOffer (related_name='applications')
    total_applications_received = Application.objects.filter(offer__in=published_offers).count()
    
    # Candidatures en attente de revue (PENDING)
    pending_applications_count = Application.objects.filter(
        offer__in=published_offers,
        statut='PENDING' # Assurez-vous que cette chaîne correspond à ApplicationStatus.PENDING
    ).count()

    context = {
        'company_profile': company_profile,
        'published_offers': published_offers,
        'total_applications_received': total_applications_received,
        'pending_applications_count': pending_applications_count,
    }
    
    return render(request, 'accounts/company_dashboard.html', context)

@login_required
def update_profile(request):
    """
    Permet à l'utilisateur (Candidat ou Entreprise) de mettre à jour son profil spécifique.
    """
    user = request.user
    
    # 1. Déterminer le profil et le formulaire à utiliser
    if user.user_type == UserType.CANDIDATE:
        profile = user.candidateprofile
        ProfileForm = CandidateProfileForm
        redirect_name = 'applications:candidate_dashboard' # Rediriger vers son dashboard
        user_type_label = "Candidat"
        
    elif user.user_type == UserType.COMPANY:
        profile = user.companyprofile
        ProfileForm = CompanyProfileForm
        redirect_name = 'accounts:company_dashboard' # Rediriger vers son dashboard
        user_type_label = "Entreprise"
        
    else:
        messages.error(request, "Type de profil non reconnu.")
        return redirect('core:index')

    # 2. Traitement de la soumission (POST)
    if request.method == 'POST':
        # 🚨 Important : Instancier avec l'instance existante et les fichiers pour le CV
        #print("Formulaire posté")
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        
        if form.is_valid():
            #print("Formulaire valide")
            form.save()
            messages.success(request, f"Votre profil {user_type_label} a été mis à jour avec succès !")
            return redirect(redirect_name)
        """else:
            print("Formulaire non valide ")"""
    # 3. Affichage initial (GET)
    else:
        # Instancier le formulaire avec les données existantes du profil
        #print("Formulaire non posté")
        form = ProfileForm(instance=profile)

    context = {
        'form': form,
        'user_type_label': user_type_label
    }
    
    
    return render(request, 'accounts/update_profile.html', context)
