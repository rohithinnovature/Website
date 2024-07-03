# authentication/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('get_user_email/', views.get_user_email, name='get_user_email'),
    path('get_user_profile/', views.get_user_profile, name='get_user_profile'),
    path('signup2/', views.signup2, name='signup2'),

    #path('profile/', views.profile, name='profile'),
    # path('', views.empty_path, name='empty_path'),
]
