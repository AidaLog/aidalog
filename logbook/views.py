from django.shortcuts import render, redirect
from home.views import process_login, logout
from .models import *
from datetime import datetime, timedelta
from docs.create_document import create_practical_training_log_book as aidalog

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
        metadata['week_activity'] = logbook.week_activity

        # get entries from this logbook
        try:
            entries = Entry.objects.filter(logbook=logbook)
            metadata['entries'] = entries
            metadata['entry_count'] = len(entries)
            # percentage of entries completed out of 5
            metadata['percentage'] = int((len(entries) / 5) * 100)
        except Entry.DoesNotExist:
            entries = None

        logbook_catalog.append(metadata)


    context = {
        "logbooks": logbook_catalog,
        "logbook_count": len(logbooks)
    }

    return render(request, 'logbook/logbook_list.html', context)


def logbook_detail_view(request, logbook_id):
    # check if user is logged in
    login_pass = is_allowed(request)
    if login_pass is not True:
        return login_pass

    # get logbook
    logbook = Logbook.objects.get(id=logbook_id, student=Student.objects.get(user=request.user))
    metadata = {}

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
        'logbook': logbook,
        'metadata': metadata
    }
    return render(request, 'logbook/logbook_detail.html', context)


def logbook_create_view(request):
    # check if user is logged in
    login_pass = is_allowed(request)
    if login_pass is not True:
        return login_pass

    # get student
    student = Student.objects.get(user=request.user)

    # get data  passed form data
    week_activity = request.POST['week_activity']
    week_number = request.POST['week_number']
    from_date = request.POST['from_date']
    to_date = datetime.strptime(from_date, '%Y-%m-%d') + timedelta(days=4)

    # if week activity is empty, set it to "Waiting for entries"
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
    logbook = Logbook.objects.get(id=logbook_id, student=Student.objects.get(user=request.user))
    if logbook is None: return
    logbook.delete()
    return redirect("/logbook/catalog")


def create_entry_view(request, logbook_id):
    # check if user is logged in
    login_pass = is_allowed(request)
    if login_pass is not True:
        return login_pass

    logbook = Logbook.objects.get(id=logbook_id)
    # get form data
    if request.POST:
        date_input = request.POST['date_input']
        activity_summary = request.POST['activity_summary']

        # get day name from date input
        day_name = datetime.strptime(date_input, '%Y-%m-%d').strftime('%A')

        # create new entry
        Entry.objects.create(
            logbook=logbook,
            day=day_name,
            date=date_input,
            activity=activity_summary)

        return redirect("/logbook/catalog/" + str(logbook_id))
    context = {
        'logbook': logbook
    }
    return render(request, 'logbook/logbook_entry.html', context)


def update_entry_view(request, logbook_id, entry_id):
    # check if user is logged in
    login_pass = is_allowed(request)
    if login_pass is not True:
        return login_pass

    logbook = Logbook.objects.get(id=logbook_id)
    entry = Entry.objects.get(id=entry_id, logbook=logbook) 
     
    # get form data
    if request.POST:
        date_input = request.POST['date_input']
        activity_summary = request.POST['activity_summary']

        # get day name from date input
        day_name = datetime.strptime(date_input, '%Y-%m-%d').strftime('%A')

        entry.day=day_name
        entry.date=date_input
        entry.activity=activity_summary
        entry.save()

        return redirect("/logbook/catalog/" + str(logbook_id))

    context = {
        'logbook': logbook,
        'entry': entry,
        'entry_date': entry.date.strftime("%Y-%m-%d")
    }

    # update entry then redirect to logbook_detail
    return render(request, 'logbook/logbook_entry.html', context)


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



def generate_logbook(request, logbook_id):
    student = Student.objects.get(user=request.user)
    logbook = Logbook.objects.get(student=student, id=logbook_id)

    # collect activities
    activity_dict = {}
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    for day in days:
        entry = None
        try:
            entry = Entry.objects.get(logbook=logbook, day=day)
            activity_dict[day] = {
            'date': entry.date,
            'activity': entry.activity}
        except:
            activity_dict[day] = {
            'date': entry.date,
            'activity': ""}

        
    
    department = student.department_name
    student_name = f"{student.user.last_name}, {student.user.first_name}"
    reg_no = student.registration_number 
    company = student.pt_location
    week_no = logbook.week_number 
    from_date = logbook.from_date
    to_date = logbook.to_date
    aidalog(department, student_name, reg_no, company, week_no, from_date, to_date, activity_dict)
    return logbook_detail_view(request, logbook_id)