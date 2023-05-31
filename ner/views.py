from django.shortcuts import render
from .engine.ner import *

# Create your views here.
def index(request):
    graph_layout = {
        1 : "Kamada Kawai",
        2 : "Circular",
        3 : "Spring",
        4 : "Spiral"
    }

    if request.POST:
        msg = request.POST['message']
        styl = int(request.POST['layout'])

        recognitions = entity_recognition(msg, 50),
        image = preview(prediction_labels=recognitions, style=styl)
        context = {
            'graph_layout' : graph_layout,
            'message' : msg,
            'image' : image
        }
        return render(request, 'ner/index.html', context)

    context={
        'graph_layout' : graph_layout,
        'message' : "Let's explore your thoughts, write something here...",
        'image': "/media/output.png"
    }
    return render(request, 'ner/index.html', context)