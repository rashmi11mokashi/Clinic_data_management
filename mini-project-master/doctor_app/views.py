from django.shortcuts import render

# Create your views here.

def doctor(request):
    return render(request,'doctor/index_doc.html')


def register(request):
    return render(request,'doctor/recep_reg.html')    

