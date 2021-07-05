from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('validate-username/', csrf_exempt(views.UsernameValidationView.as_view()), name='validate-username'),
    path('validate-email/', csrf_exempt(views.EmailValidationView.as_view()), name='validate-email'),
    path('activate/<uidb64><token>/', views.AccountVerificationView.as_view(), name='activate-account'),
]