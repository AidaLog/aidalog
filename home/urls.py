from django.urls import path
from home.views import home_view, signup_view, login_view, logout_view, password_reset_view

urlpatterns = [
    path('', home_view, name="home"),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('reset-pwd/', password_reset_view, name='password_reset'),
]
