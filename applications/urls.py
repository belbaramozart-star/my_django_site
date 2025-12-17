from django.urls import path
from .import views

app_name = "applications"

urlpatterns = [
    path('postuler/<int:offer_pk>/', views.apply_to_offer, name="apply_to_offer"),
    path('tableau-de-bord/', views.candidate_dashboard, name="candidate_dashboard"),
    path('status/<int:offer_pk>/candidature/<int:application_pk>/mise-a-jour', views.update_application_status, name='update_application_status'),
]