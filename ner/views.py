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
        processed_paragraph = generate_ner_data(recognitions)
        context = {
            'graph_layout' : graph_layout,
            'message' : msg,
            'image' : image,
            'paragraph' : processed_paragraph
        }

        return render(request, 'ner/index.html', context)

    context={
        'graph_layout' : graph_layout,
        'message' : "the second part is about projects carried by youths in the AI sector, the third part is the response of the survey that was carried at the University of Dodoma, College of Informatics and Virtual Education (CIVE) on how experts, lecturers, and students perceive the future of AI and how it will affect their lives and the last part is on obstacles that will affect the adaption of the technology",
        'image': "/media/output.png"
    }
    return render(request, 'ner/index.html', context)