from django.shortcuts import render, redirect
from home.views import process_login, logout
from .models import *
from datetime import datetime, timedelta

def logbook_home_view(request):
    # check if user is logged in
    login_pass = False
    if request.user.is_authenticated: login_pass = True

    context = {
        'login_pass' : login_pass
    }
    return render(request, 'logbook/logbook_home.html', context)


def profile_settings_view(request):
    # load form data
    if request.POST:
        # get form data
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        reg_number = request.POST['reg_number']
        year_of_study = request.POST['year_of_study']
        dept_name = request.POST['dept_name']
        company_name = request.POST['company_name']
        start_date = request.POST['start_date']

        # update user profile
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username
        user.save()

        # check if Student with user exists
        student = Student.objects.get(user=user)
        if student is None:
            # create new student
            student = Student()
            student.user = user
            student.registration_number = reg_number
            student.year_of_study = year_of_study
            student.department_name = dept_name
            student.university = "UDSM"
            student.pt_location = company_name
            student.practical_training_start_date = start_date
            student.save()
        else:
            # update student
            student.registration_number = reg_number
            student.year_of_study = year_of_study
            student.department_name = dept_name
            student.pt_location = company_name
            student.practical_training_start_date = start_date
            student.save()

        return redirect("/logbook")

    # get student information
    student = Student.objects.get(user=request.user)
    if student is  None:
        return redirect("/logbook/logbook_redirect_login")

    context = {
        'student' : student
    }

    return render(request, 'logbook/logbook_settings.html', context)

def logbook_catalog_view(request):
    if request.POST:
        return logbook_create_view(request)


    # get logbooks
    student = Student.objects.get(user=request.user)
    logbooks = Logbook.objects.filter(student=student)

    context = {
        "logbooks": logbooks,
        "logbook_count": len(logbooks)
    }

    return render(request, 'logbook/logbook_list.html', context)


def logbook_detail_view(request, logbook_id):
    return render(request, 'logbook/logbook_detail.html', {})


def logbook_create_view(request):
    # get student
    student = Student.objects.get(user=request.user)

    # Get the current date
    current_date = datetime.now().date() # Set the week number based on the ISO week number of the current date
    week_number = current_date.isocalendar()[1] # Calculate the start date (Monday) of the week for the given week number and year
    from_date = current_date - timedelta(days=current_date.isocalendar()[2] - 1)  # Calculate the end date (Friday) of the week for the given week number and year
    to_date = from_date + timedelta(days=4)
    # get passed form data
    week_activity = request.POST['week_activity']
    # if week activity is empty, set it to "Waiting for entries"
    # remove spaces in week_activity
    week_activity_clean = week_activity.strip()
    if week_activity_clean == "" or week_activity is None:
        week_activity = "Waiting for entries"

    # Create and return the Logbook instance
    Logbook.objects.create(
        student=student,
        week_number=week_number,
        from_date=from_date,
        to_date=to_date,
        week_activity=week_activity)

    return redirect("/logbook/catalog")

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


def signup_view(request):
    context = {}
    if request.POST:
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            context['form_errors'] = "username already exists"
        elif User.objects.filter(email=email).exists():
            context['form_errors'] = "email already exists"
        else:
            user = User.objects.create_user(username, email, password)
            user.save()

            # directly log in the user
            success = process_login(request, "/logbook_settings")
            if success is False:
                context['form_errors'] = "invalid username or password"
            else:
                return success # redirect to profile setup

    return render(request, 'home/signup.html', context)