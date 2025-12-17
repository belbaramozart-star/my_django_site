from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('register/<str:user_type>/', views.register_user, name="register"),
    path('entreprise/tableau-de-bord/', views.company_dashboard, name="company_dashboard"),
    path('profil/mise-a-jour/', views.update_profile, name='update_profile'),
]
