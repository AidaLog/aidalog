from django.shortcuts import render


def logbook_home_view(request):
    return render(request, 'logbook/logbook_home.html', {})
    