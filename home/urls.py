from django.urls import path
from .views import *

urlpatterns = [
    path('', home_view, name="home"),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('reset-pwd/', password_reset_view, name='password_reset'),
]
