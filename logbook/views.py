from django.shortcuts import render, redirect
from home.views import process_login, logout

def logbook_home_view(request):
    # check if user is logged in
    login_pass = False
    if request.user.is_authenticated: login_pass = True

    context = {
        'login_pass' : login_pass
    }
    return render(request, 'logbook/logbook_home.html', context)


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


def logbook_redirect_login(request):
    context = {}
    if request.POST:
        success = process_login(request, "/logbook")
        if success is False:
            context['form_errors'] = "invalid username or password"
        else:
            return success

    return render(request, 'home/login.html', context)


def logbook_logout_redirect(request):
    logout(request)
    return redirect('/logbook')