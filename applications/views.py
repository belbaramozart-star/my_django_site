from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from accounts.models import UserType # Pour vérifier le type d'utilisateur
from offers.models import JobOffer
from .forms import ApplicationForm, ApplicationStatusForm
from .models import Application

@login_required
def apply_to_offer(request, offer_pk):
    """
    Gère la soumission d'une candidature pour une offre spécifique.
    """
    offer = get_object_or_404(JobOffer, pk=offer_pk)
    user = request.user

    # 🚨 1. Vérification de l'utilisateur : Seuls les candidats peuvent postuler
    if user.user_type != UserType.CANDIDATE:
        messages.error(request, "Seuls les comptes Candidat peuvent postuler à une offre.")
        return redirect('offers:offer_detail', pk=offer_pk)

    # 🚨 2. Vérification de la candidature déjà existante
    if Application.objects.filter(candidat=user, offer=offer).exists():
        messages.warning(request, "Vous avez déjà postulé à cette offre.")
        return redirect('offers:offer_detail', pk=offer_pk)

    if request.method == 'POST':
        # Instancier le formulaire avec les données POST et les fichiers (pour la LDM)
        form = ApplicationForm(request.POST, request.FILES) 
        
        if form.is_valid():
            # Ne pas enregistrer tout de suite pour injecter les FK
            application = form.save(commit=False)
            
            # 3. Injection des clés étrangères (crucial)
            application.candidat = user
            application.offer = offer
            application.save()
            
            messages.success(request, "Votre candidature a été soumise avec succès !")
            # Rediriger vers la page de suivi des candidatures (à créer plus tard)
            return redirect('offers:offer_list') 
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    
    else:
        # Affichage du formulaire initial
        form = ApplicationForm()

    context = {
        'form': form,
        'offer': offer
    }
    return render(request, 'applications/apply_form.html', context)

@login_required
def candidate_dashboard(request):
    """
    Affiche la liste des candidatures soumises par l'utilisateur (s'il est Candidat).
    """
    user = request.user
    
    # 🚨 1. Vérification du type d'utilisateur
    if user.user_type != UserType.CANDIDATE:
        messages.error(request, "Accès refusé. Cette page est réservée aux Candidats.")
        return redirect('core:index') # Rediriger vers la page d'accueil ou de profil

    # 2. Récupération des données
    # Récupère toutes les candidatures soumises par l'utilisateur connecté
    candidatures = Application.objects.filter(candidat=user).order_by('-date_soumission')

    context = {
        'candidatures': candidatures,
        'candidate_profile': user.candidateprofile # Accès direct au profil du candidat
    }
    
    return render(request, 'applications/candidate_dashboard.html', context)

@login_required
@require_POST
def update_application_status(request, offer_pk, application_pk):
    """
    Met à jour le statut d'une candidature spécifique (POST requis).
    """
    user = request.user
    
    if user.user_type != UserType.COMPANY:
        messages.error(request, "Action non autorisée.")
        return redirect('core:index')

    application = get_object_or_404(Application, pk=application_pk)
    offer = get_object_or_404(JobOffer, pk=offer_pk)

    # Vérification que le recruteur est bien le propriétaire de l'offre
    if offer.company != user.companyprofile or application.offer != offer:
        messages.error(request, "Accès non autorisé à cette ressource.")
        return redirect('accounts:company_dashboard')
        
    form = ApplicationStatusForm(request.POST, instance=application)
    
    if form.is_valid():
        form.save()
        messages.success(request, f"Le statut du candidat {application.candidat.email} a été mis à jour à {application.get_statut_display()}.")
    else:
        # Ceci ne devrait pas arriver si le formulaire est bien conçu
        messages.error(request, "Erreur lors de la mise à jour du statut.")

    # Rediriger vers la page de gestion des candidatures de l'offre
    return redirect('offers:manage_applications', offer_pk=offer_pk)

