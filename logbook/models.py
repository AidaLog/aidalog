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

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class Logbook(models.Model):
    student = models.ForeignKey(Student, related_name='logbooks', on_delete=models.CASCADE)
    week_number = models.IntegerField()
    from_date = models.DateField()
    to_date = models.DateField()
    is_submitted = models.BooleanField(default=False)
    week_activity = models.TextField(blank=True)
    def __str__(self):
        return f'Logbook week:{self.week_number}'


class Entry(models.Model):
    logbook = models.ForeignKey(Logbook, related_name='entries', on_delete=models.CASCADE)
    day = models.CharField(max_length=255)
    date = models.DateField()
    activity = models.TextField()
    rating = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.day} - {self.date}'