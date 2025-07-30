from django.test import TestCase

# Create your tests here.
from views import get_week_entries

w = get_week_entries(week_number=1)
print(w)