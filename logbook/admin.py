from django.contrib import admin
from .models import Student, Logbook, Entry, Week_operation

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['user', 'university', 'department_name', 'registration_number', 'year_of_study', 'pt_location']

@admin.register(Logbook)
class LogbookAdmin(admin.ModelAdmin):
    list_display = ['student', 'week_number', 'from_date', 'to_date', 'is_submitted']

@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ['logbook', 'day', 'date', 'activity', 'created_at', 'updated_at']

@admin.register(Week_operation)
class OperationAdmin(admin.ModelAdmin):
    list_display = ['id', 'logbook', 'operation']