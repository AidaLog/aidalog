from django.urls import path
from home.views import home_view
from .views import (
    profile_settings_view,
    logbook_catalog_view,
    delete_logbook,
    logbook_detail_view,
    create_entry_view,
    update_entry_view,
    create_batch_entries,
    logbook_redirect_login,
    logbook_logout_redirect,
    generate_logbook,
    operations_view,
    operations_create_view,
    operations_edit_view,
    operations_delete_view,
    update_activity_diagram,
)

urlpatterns = [
    # Home
    path("", home_view, name="logbook_home"),
    # User Settings
    path("logbook_settings/", profile_settings_view, name="logbook_settings"),
    # Logbook Catalog
    path("catalog/", logbook_catalog_view, name="logbook_catalog"),
    path("catalog/<int:logbook_id>/", logbook_detail_view, name="logbook_detail"),
    path("catalog/<int:logbook_id>/delete/", delete_logbook, name="logbook_delete"),
    # Logbook Entries
    path("catalog/<int:logbook_id>/entry/", create_entry_view, name="entry_create"),
    path(
        "catalog/<int:logbook_id>/entry/<int:entry_id>/",
        update_entry_view,
        name="entry_update",
    ),
    path(
        "catalog/<int:logbook_id>/batch/",
        create_batch_entries,
        name="entry_batch_create",
    ),
    # Redirect Views
    path("redirect/login/", logbook_redirect_login, name="logbook_redirect_login"),
    path("redirect/logout/", logbook_logout_redirect, name="logbook_logout_redirect"),
    # Logbook Generation
    path("aidalog/<int:logbook_id>/", generate_logbook, name="logbook_generate"),
    # Operations
    path("operations/<int:logbook_id>/", operations_view, name="operations_list"),
    path(
        "operations/<int:logbook_id>/create/",
        operations_create_view,
        name="operations_create",
    ),
    path(
        "operations/<int:logbook_id>/<int:operation_id>/edit/",
        operations_edit_view,
        name="operations_edit",
    ),
    path(
        "operations/<int:logbook_id>/<int:operation_id>/delete/",
        operations_delete_view,
        name="operations_delete",
    ),
    # Diagram
    path(
        "catalog/<int:logbook_id>/diagram/update/",
        update_activity_diagram,
        name="diagram_update",
    ),
]
