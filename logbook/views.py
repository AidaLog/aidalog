from django.shortcuts import render


def logbook_home_view(request):
    return render(request, 'logbook/logbook_home.html', {})


def profile_settings_view(request):
    return render(request, 'logbook/logbook_settings.html', {})

def logbook_catalog_view(request):
    return render(request, 'logbook/logbook_list.html', {})


def logbook_detail_view(request, logbook_id):
    return render(request, 'logbook/logbook_detail.html', {})


def logbook_create_view(request):
    # create new logbook then redirect to logbook_detail
    pass

def create_entry_view(request, logbook_id):
    # create new entry then redirect to logbook_detail
    return render(request, 'logbook/logbook_entry.html', {})


def update_entry_view(request, logbook_id, entry_id):
    # update entry then redirect to logbook_detail
    return render(request, 'logbook/logbook_entry.html', {})