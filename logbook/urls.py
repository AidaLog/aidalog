from django.urls import path
from .views import *

urlpatterns = [
    path('', logbook_home_view, name='logbook_home'),
    path('logbook_settings/', profile_settings_view, name='logbook_settings'),
    path('catalog/', logbook_catalog_view, name='logbook_catalog'),
    path('dispose/<int:logbook_id>/', delete_logbook, name='dispose_logbook'),
    path('catalog/<int:logbook_id>/', logbook_detail_view, name='logbook_detail'),
    path('catalog/<int:logbook_id>/entry/', create_entry_view, name='logbook_entry'),
    path('catalog/<int:logbook_id>/entry/<int:entry_id>/', update_entry_view, name='logbook_entry'),
    path('catalog/<int:logbook_id>/batch/', create_batch_entries, name='logbook_batch'),
    path('logbook_redirect_login/', logbook_redirect_login, name='logbook_redirect_login'),
    path('logbook_logout_redirect/', logbook_logout_redirect, name='logbook_logout_redirect'),
    path('aidalog/<int:logbook_id>/', generate_logbook, name='aidalog'),
    path('operations/<int:logbook_id>/', operations_view, name='operations'),
    path('operations-create/<int:logbook_id>/', operations_create_view, name='create_operations'),
    path('operations-update/<int:logbook_id>/<int:operation_id>/', operations_edit_view, name='update_operations'),
    path('operations-delete/<int:logbook_id>/<int:operation_id>/', operations_delete_view, name='delete_operations'),
    path('update-diagram/<int:logbook_id>/', update_activity_diagram, name='update_diagram'),
]