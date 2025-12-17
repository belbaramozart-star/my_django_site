from django.urls import path
from .views import OfferListView, OfferDetailView, create_offer, manage_applications

app_name = "offers"

urlpatterns = [
    path('', OfferListView.as_view(), name='offer_list'),
    path('<int:pk>', OfferDetailView.as_view(), name='offer_detail'),
    path('creer/', create_offer, name='create_offer'),
    path('<int:offer_pk>', manage_applications, name='manage_applications'),
]
