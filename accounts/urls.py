from django.urls import path, include
from . import views
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'accounts'

urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('logout/', views.UserLogout.as_view(), name='logout'),
    path('register/', views.UserRegister.as_view(), name='register'),
    path('change-password/', views.ChangePassword.as_view(), name='change-password'),
    path('reset-password/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]
