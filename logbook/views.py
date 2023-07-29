from django.shortcuts import render, redirect, HttpResponse
from home.views import process_login, logout
from .models import *
from datetime import datetime, timedelta
from docs.create_document import create_practical_training_log_book as aidalog
import os

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
            updated_entries = Entry.objects.filter(logbook=logbook, is_updated=True)
            updated_entries_count = len(updated_entries)

            metadata['entries'] = entries
            metadata['entry_count'] = updated_entries_count
            # percentage of entries completed out of 5
            metadata['percentage'] = int((updated_entries_count / 5) * 100)
        except Entry.DoesNotExist:
            entries = None

            # get week operations   
        try:
            week_operations = Week_operation.objects.filter(logbook=logbook)
            metadata['week_operation_count'] = len(week_operations)

            # get only 2 week operations, max 30 characters for opeartions
            week_operations = week_operations[:2]
            for week_operation in week_operations:
                if len(week_operation.operation) > 30:
                    week_operation.operation = week_operation.operation[:50] + "..."

        except Week_operation.DoesNotExist:
            metadata['week_operation_count'] = 0
            week_operations = None

        metadata['week_operations'] = week_operations
        
        logbook_catalog.append(metadata)


    context = {
        "logbooks": logbook_catalog,
        "logbook_count": len(logbooks)
    }
    print(context)

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
        updated_entries = Entry.objects.filter(logbook=logbook, is_updated=True)
        updated_entries = len(updated_entries)

        metadata['entries'] = entries
        metadata['entry_count'] = len(entries)
        metadata['updated_entries'] = updated_entries
        
        print_state = False
        if updated_entries == 5: 
            print_state=True 

        # percentage of entries completed out of 5
        metadata['percentage'] = int((updated_entries / 5) * 100)
        metadata['print_state'] = print_state
    except Entry.DoesNotExist:
        entries = None

    # get week operations   
    try:
        week_operations = Week_operation.objects.filter(logbook=logbook)
        metadata['week_operation_count'] = len(week_operations)

        # get only 2 week operations, max 30 characters for opeartions
        week_operations = week_operations[:2]
        for week_operation in week_operations:
            if len(week_operation.operation) > 30:
                week_operation.operation = week_operation.operation[:50] + "..."

    except Week_operation.DoesNotExist:
        week_operations = None

    metadata['week_operations'] = week_operations

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
        # constraints. if date is not within logbook from_date and to_date, return error
        date_input = datetime.strptime(date_input, '%Y-%m-%d')
        logbook_from_date = datetime.combine(logbook.from_date, datetime.min.time())
        logbook_to_date = datetime.combine(logbook.to_date, datetime.max.time())

        if date_input < logbook_from_date or date_input > logbook_to_date:
            context = {
                'logbook': logbook,
                'form_errors': "Date must be within logbook start and end date."
            }
            return render(request, 'logbook/logbook_entry.html', context)

        # if date already exists, redirect to update with an error message and new content
        try:
            entry = Entry.objects.get(logbook=logbook, date=date_input)
            return redirect("/logbook/catalog/" + str(logbook_id) + "/entry/" + str(entry.id))
        except Entry.DoesNotExist:
            pass

        # if entries exceed 5, return error
        entries = Entry.objects.filter(logbook=logbook)
        if len(entries) >= 5:
            context = {
                'logbook': logbook,
                'form_errors': "Entries for this logbook have exceeded 5 that is (Monday to Friday)"
            }
            return render(request, 'logbook/logbook_entry.html', context)

        # get day name from date input
        date_input = request.POST['date_input']
        day_name = datetime.strptime(date_input, '%Y-%m-%d').strftime('%A')

        # create new entry
        Entry.objects.create(
            logbook=logbook,
            day=day_name,
            date=date_input,
            activity=activity_summary,
            is_updated=True)

        return redirect("/logbook/catalog/" + str(logbook_id))
    context = {
        'logbook': logbook
    }
    return render(request, 'logbook/logbook_entry.html', context)


def create_batch_entries(request, logbook_id):
    # check if user is logged in
    login_pass = is_allowed(request)
    if login_pass is not True:
        return login_pass

    logbook = Logbook.objects.get(id=logbook_id)
    # create entries from monday to friday with empty activity from logbook from date
    from_date = logbook.from_date
    to_date = logbook.to_date
    delta = to_date - from_date

    for i in range(delta.days + 1):
        date = from_date + timedelta(days=i)
        day_name = date.strftime('%A')
        Entry.objects.create(
            logbook=logbook,
            day=day_name,
            date=date,
            activity="** click update to edit **")

    return redirect("/logbook/catalog/" + str(logbook_id))

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
        entry.is_updated=True
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

    logbook.is_submitted=True
    logbook.save()

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
            'date': "dd/mm/yyyy",
            'activity': ""}

    # get operation and machinery
    operation_list = []
    try:
        week_operations = Week_operation.objects.filter(logbook=logbook)
        for week_operation in week_operations:
            operation_list.append(
                {"operation": week_operation.operation,
                "machinery": week_operation.machinery})
    except:
        pass
            
    
    department = student.department_name
    student_name = f"{student.user.last_name}, {student.user.first_name}"
    reg_no = student.registration_number 
    company = student.pt_location
    week_no = logbook.week_number 
    from_date = logbook.from_date
    to_date = logbook.to_date
    activity_diagram = logbook.activity_diagram
    generated_document = aidalog(department, student_name, reg_no, company, week_no, from_date, to_date, activity_dict, operation_list, activity_diagram)

    return download_generated_docx(request, generated_document)


def download_generated_docx(request, generated_file_path):
    file_path = generated_file_path
    file_name = os.path.basename(file_path)
    
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        return response



def operations_view(request, logbook_id):
    # check if user is logged in
    login_pass = is_allowed(request)
    if login_pass is not True:
        return login_pass

    student = Student.objects.get(user=request.user)
    logbook = Logbook.objects.get(student=student, id=logbook_id)
    try:
        week_operations = Week_operation.objects.filter(logbook=logbook)
        operation_count = len(week_operations)
    except:
        week_operations = False
        operation_count = 0
    

    if request.method == 'POST':
        operation_data = request.POST.get('operation', '') 
        machinery_data = request.POST.get('machinery', '')  
        
        if operation_data and machinery_data:  
            operation_instance = Week_operation(
                logbook=logbook,
                operation=operation_data,
                machinery=machinery_data
            )
            operation_instance.save()

    context={
        'logbook': logbook,
        'week_operations': week_operations,
        'operation_count': operation_count
    }

    return render(request, 'logbook/logbook_operations.html', context)


def operations_create_view(request, logbook_id):
    # check if user is logged in
    login_pass = is_allowed(request)
    if login_pass is not True:
        return login_pass

    student = Student.objects.get(user=request.user)
    logbook = Logbook.objects.get(student=student, id=logbook_id)
    
    if request.method == 'POST':
        operation_data = request.POST.get('operation', '') 
        machinery_data = request.POST.get('machinery', '')  
        
        if operation_data and machinery_data:  
            operation_instance = Week_operation(
                logbook=logbook,
                operation=operation_data,
                machinery=machinery_data
            )
            operation_instance.save()
        
        return redirect("/logbook/operations/"+str(logbook_id))

    context={
        'logbook': logbook,
    }

    return render(request, 'logbook/logbook_operations_create.html', context)

def operations_edit_view(request, logbook_id, operation_id):
    # check if user is logged in
    login_pass = is_allowed(request)
    if login_pass is not True:
        return login_pass

    student = Student.objects.get(user=request.user)
    logbook = Logbook.objects.get(student=student, id=logbook_id)
    week_operation = Week_operation.objects.get(logbook=logbook, id=operation_id)

    if request.method == 'POST':
        operation_data = request.POST.get('operation', '') 
        machinery_data = request.POST.get('machinery', '')  

        week_operation.operation = operation_data
        week_operation.machinery = machinery_data

        week_operation.save()
        
        return redirect("/logbook/operations/"+str(logbook_id))

    context={
        'logbook': logbook,
        'week_operation': week_operation
    }

    return render(request, 'logbook/logbook_operations_create.html', context)


def operations_delete_view(request, logbook_id, operation_id):
    # check if user is logged in
    login_pass = is_allowed(request)
    if login_pass is not True:
        return login_pass

    student = Student.objects.get(user=request.user)
    logbook = Logbook.objects.get(student=student, id=logbook_id)
    week_operation = Week_operation.objects.get(logbook=logbook, id=operation_id)
    week_operation.delete()

    return redirect("/logbook/operations/"+str(logbook_id))


def update_activity_diagram(request, logbook_id):
    # check if user is logged in
    login_pass = is_allowed(request)
    if login_pass is not True:
        return login_pass

    student = Student.objects.get(user=request.user)
    logbook = Logbook.objects.get(student=student, id=logbook_id)

    if request.method == 'POST':
        activity_diagram_file = request.FILES['diagram']
        logbook.activity_diagram = activity_diagram_file
        logbook.save()

        return redirect("/logbook/operations/"+str(logbook_id))

    context={
        'logbook': logbook,
    }

    return render(request, 'logbook/logbook_operations_diagram.html', context)