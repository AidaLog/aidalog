from django.shortcuts import render, redirect
from home.views import process_login, logout
from .models import *
from datetime import datetime, timedelta

def is_allowed(request):
    if request.user.is_authenticated:
        return True
    else:
        return redirect("/logbook/logbook_redirect_login")


def logbook_home_view(request):
    # check if user is logged in
    login_pass = is_allowed(request)
    if login_pass is not True:
        login_pass = False

    # try to get student status
    try:
        student = Student.objects.get(user=request.user)
    except:
        student = None

    context = {
        'login_pass' : login_pass,
        'student' : student
    }
    return render(request, 'logbook/logbook_home.html', context)


def profile_settings_view(request):
    # check if user is logged in
    login_pass = is_allowed(request)
    if login_pass is not True:
        return login_pass

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
        try:
            student = Student.objects.get(user=user)
        except Student.DoesNotExist:
            student = None

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
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        student = None

    
    context = {
        'student' : student
    }

    return render(request, 'logbook/logbook_settings.html', context)


def logbook_catalog_view(request):
    # check if user is logged in
    login_pass = is_allowed(request)
    if login_pass is not True:
        return login_pass

    if request.POST:
        return logbook_create_view(request)

    # get student information
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        student = None

    if student is  None and request.user.is_authenticated:
        return redirect("/logbook/logbook_settings")
 
    # get logbooks
    logbooks = Logbook.objects.filter(student=student)
    logbook_catalog = []

    for logbook in logbooks:
        metadata = {}
        metadata['id'] = logbook.id
        metadata['week_number'] = logbook.week_number
        metadata['from_date'] = logbook.from_date

        # get entries from this logbook
        try:
            entries = Entry.objects.filter(logbook=logbook)
            metadata['entries'] = entries
            metadata['entry_count'] = len(entries)
            # percentage of entries completed out of 5
            metadata['percentage'] = int((len(entries) / 5) * 100)
        except Entry.DoesNotExist:
            entries = None

        

    context = {
        "logbooks": logbooks,
        "logbook_count": len(logbooks)
    }

    return render(request, 'logbook/logbook_list.html', context)


def logbook_detail_view(request, logbook_id):
    # check if user is logged in
    login_pass = is_allowed(request)
    if login_pass is not True:
        return login_pass

    return render(request, 'logbook/logbook_detail.html', {})


def logbook_create_view(request):
    # check if user is logged in
    login_pass = is_allowed(request)
    if login_pass is not True:
        return login_pass

    # get student
    student = Student.objects.get(user=request.user)
    # get training start date
    start_date = student.practical_training_start_date
    start_date_week_number = start_date.isocalendar()[1]
    # Get the current date
    current_date = datetime.now().date() 
    current_week_number = current_date.isocalendar()[1] 

    week_number = current_week_number - start_date_week_number
    if week_number == 0: week_number = 1

    from_date = current_date - timedelta(days=current_date.isocalendar()[2] - 1)  
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


def delete_logbook(request, logbook_id):
    pass


def create_entry_view(request, logbook_id):
    # check if user is logged in
    login_pass = is_allowed(request)
    if login_pass is not True:
        return login_pass

    # create new entry then redirect to logbook_detail
    return render(request, 'logbook/logbook_entry.html', {})


def update_entry_view(request, logbook_id, entry_id):
    # check if user is logged in
    login_pass = is_allowed(request)
    if login_pass is not True:
        return login_pass

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