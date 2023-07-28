from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    university = models.CharField(max_length=255)
    department_name = models.CharField(max_length=255)
    registration_number = models.CharField(max_length=255)
    year_of_study = models.IntegerField()
    pt_location = models.CharField(max_length=255)
    practical_training_start_date = models.DateField(blank=True, null=True)
    logbook_print_count = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class Logbook(models.Model):
    student = models.ForeignKey(Student, related_name='logbooks', on_delete=models.CASCADE)
    week_number = models.IntegerField()
    from_date = models.DateField()
    to_date = models.DateField()
    is_submitted = models.BooleanField(default=False, verbose_name="Logbook Printed")
    week_activity = models.TextField(blank=True)
    activity_diagram = models.FileField(upload_to="activity_diagrams", null=True, blank=True)
    def __str__(self):
        return f'Logbook week:{self.week_number}'


class Entry(models.Model):
    logbook = models.ForeignKey(Logbook, related_name='entries', on_delete=models.CASCADE)
    day = models.CharField(max_length=255)
    date = models.DateField()
    activity = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_updated = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.day} - {self.date}'


class Week_operation(models.Model):
    logbook = models.ForeignKey(Logbook, related_name='week_operations', on_delete=models.CASCADE)
    operation = models.TextField(blank=True)
    machinery = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_updated = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.operation}'

        