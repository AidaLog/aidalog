from django.urls import path
from .views import *

urlpatterns = [
    path('', logbook_home_view, name='logbook_home'),
    path('settings/', profile_settings_view, name='logbook_settings'),
    path('catalog/', logbook_catalog_view, name='logbook_catalog'),
    path('catalog/<int:logbook_id>/', logbook_detail_view, name='logbook_detail'),
    path('catalog/<int:logbook_id>/entry/', create_entry_view, name='logbook_entry'),
    path('catalog/<int:logbook_id>/entry/<int:entry_id>/', update_entry_view, name='logbook_entry'),
    path('logbook_redirect_login/', logbook_redirect_login, name='logbook_redirect_login'),
    path('logbook_logout_redirect/', logbook_logout_redirect, name='logbook_logout_redirect')
]