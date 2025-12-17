from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import UserType
from .forms import JobOfferForm
from .models import JobOffer

class OfferListView(ListView):
    
    model = JobOffer

    template_name = 'offers/offer_list.html'
    context_object_name = 'offers'
    paginate_by = 10

    # Surcharge de la requete pour n'afficher que les offres actives
    def get_queryset(self):
        return JobOffer.objects.filter(is_active=True)

# Affiche les détails complets d'une offre d'emploi ou de stage
class OfferDetailView(DetailView):
    model = JobOffer
    template_name = 'offers/offer_detail.html'
    context_object_name = 'offer'

@login_required
def create_offer(request):
    """
    Permet à l'entreprise de publier une nouvelle offre.
    """
    #print("create_offer est exécuté")
    user = request.user
    
    # 🚨 1. Vérification du type d'utilisateur
    if user.user_type != UserType.COMPANY:
        messages.error(request, "Accès refusé. Seules les Entreprises peuvent publier des offres.")
        return redirect('core:index')
    elif user.user_type == UserType.COMPANY:
        # Vérifions si les champs critiques du profil sont renseignés
        profile = request.user.companyprofile
        if not profile.nom_entreprise or not profile.description:
            #print("Soit profile.nom_entreprise ou not profile.description n'est pas bien rempli")
            return redirect('accounts:update_profile')

    # Récupération du profil d'entreprise pour la liaison
    company_profile = user.companyprofile 
    
    if request.method == 'POST':
        print("--- DEBUG POST DATA ---")
        print("Compétences recues (required_skills):", request.POST.get('required_skills'))
        print("-----------------------")
        # Instancier le formulaire avec les données POST
        form = JobOfferForm(request.POST) 
        
        if form.is_valid():
            # Ne pas enregistrer tout de suite pour injecter la clé étrangère
            offer = form.save(commit=False)
            
            # 2. Lier l'offre au profil d'entreprise
            offer.company = company_profile
            offer.is_active = True # L'offre est active par défaut
            
            offer.save()
            
            # 3. Gérer la relation Many-to-Many (Compétences)
            form.save_m2m() # Nécessaire après l'enregistrement initial de l'offre
            
            messages.success(request, f"L'offre '{offer.titre}' a été publiée avec succès !")
            # Rediriger vers le tableau de bord de l'entreprise
            return redirect('accounts:company_dashboard') 
        
    else:
        # Affichage du formulaire initial
        form = JobOfferForm()

    context = {
        'form': form,
        'company_profile': company_profile
    }
    return render(request, 'offers/create_offer.html', context)

@login_required
def manage_applications(request, offer_pk):
    """
    Affiche la liste des candidatures pour une offre spécifique, 
    uniquement si l'utilisateur est le propriétaire de l'offre.
    """
    user = request.user
    
    if user.user_type != UserType.COMPANY:
        messages.error(request, "Accès refusé. Réservé aux Recruteurs.")
        return redirect('core:index')

    # 1. Récupérer l'offre ou 404
    offer = get_object_or_404(JobOffer, pk=offer_pk)

    # 2. Vérifier l'appartenance de l'offre
    if offer.company != user.companyprofile:
        messages.error(request, "Accès non autorisé à cette offre.")
        return redirect('accounts:company_dashboard')

    # 3. Récupérer toutes les candidatures pour cette offre
    applications = offer.applications.all().order_by('-date_soumission')
    
    context = {
        'offer': offer,
        'applications': applications,
    }
    
    return render(request, 'offers/manage_applications.html', context)

