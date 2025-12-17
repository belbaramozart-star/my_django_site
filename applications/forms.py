from django import forms
from .models import Application, ApplicationStatus

class ApplicationForm(forms.ModelForm):
    """
    Formulaire permettant au candidat de soumettre sa candidature pour une offre.
    """
    class Meta:
        model = Application
        # Nous n'affichons que le champ facultatif (lettre_motivation)
        # Les champs 'candidat' et 'offer' seront remplis dans la vue.
        fields = ('lettre_motivation',) 
        
    def init(self, *args, **kwargs):
        super().init(*args, **kwargs)
        # Facultatif : personnaliser le widget pour l'upload de fichier
        self.fields['lettre_motivation'].widget.attrs.update({
            'class': 'form-control-file',
            'required': False # Rendre explicitement le champ non obligatoire
        })

class ApplicationStatusForm(forms.ModelForm):
    """
    Formulaire simple pour permettre au recruteur de mettre à jour le statut.
    """
    class Meta:
        model = Application
        fields = ('statut',)
        # Utiliser un Select pour la liste déroulante
        widgets = {
            'statut': forms.Select(choices=ApplicationStatus.choices),
        }