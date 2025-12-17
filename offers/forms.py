from django import forms
from .models import JobOffer, OfferType, Skill, ContractType

class JobOfferForm(forms.ModelForm):
    """
    Formulaire permettant à une entreprise de créer et publier une offre.
    """
    # 1. Champ pour la sélection des compétences (rendu sous forme de cases à cocher)
    #skills = forms.ModelMultipleChoiceField(queryset=Skill.objects.all().order_by('nom'), widget=forms.CheckboxSelectMultiple, required=False, label="Compétences Requises" )
    
    # 2. Pour le champ date_expiration, on utilise un widget adapté
    date_expiration = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Date Limite de Candidature"
    )

    class Meta:
        model = JobOffer
        # Exclure 'company', 'date_publication', et 'is_active' car ils sont remplis dans la vue
        exclude = ('company', 'date_publication', 'is_active',) 
        
        # Surcharge des étiquettes (facultatif)
        labels = {
            'titre': 'Titre de l\'Offre',
            'offer_type': 'Type d\'Opportunité',
            'contract_type': 'Type de Contrat',
            'remuneration': 'Rémunération (€ ou devise locale)',
        }

        fields = [
            'titre', 'description', 'localisation', 'contract_type', 'date_expiration', 'remuneration', 'required_skills'
        ]
        
    def init(self, *args, **kwargs):
        super().init(*args, **kwargs)
        # S'assurer que OfferType est bien visible
        self.fields['offer_type'].queryset = OfferType.objects.all()