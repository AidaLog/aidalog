from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate

def home_view(request):
    return render(request, "home/index.html")

# signup view
def signup_view(request):
    return render(request, 'home/signup.html')


def logout_view(request):
    logout(request)
    return redirect(".")


def process_login(request, redirect_path="/"):
    username = request.POST['email']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect(redirect_path)
    else:
        return False
            

def login_view(request):
    context = {}
    if request.POST:
        success = process_login(request, "/")
        if success is False:
            context['form_errors'] = "invalid username or password"
        else:
            return success

    return render(request, 'home/login.html', context)

