from django.shortcuts import render
from .engine.ner import *

# Create your views here.
def index(request):
    if request.POST:
        msg = request.POST['message']
        recognitions = entity_recognition(msg, 50),
        image = preview(prediction_labels=recognitions)
        context = {
            'message' : msg,
            'image' : image
        }
        return render(request, 'ner/index.html', context)

    context={
        'message' : "Let's explore your thoughts, write something here...",
        'image': "/media/output.png"
    }
    return render(request, 'ner/index.html', context)