from django.shortcuts import render

# Create your views here.
from django.core.files.storage import FileSystemStorage
from django.urls import conf
import os

import funtion
from funtion import Config

def index(request):
    context={'a': 1}
    return render(request, 'index.html', context)

name = 0
def predictImage(request):
    global name
    name += 1
    fileObj = request.FILES['filePath']
    tan = request.POST['cars']
    print(tan)
    fs = FileSystemStorage()
    filePathName = fs.save(fileObj.name, fileObj)
    filePathName = fs.url(fileObj)
    testimage = '.' + filePathName
    if(tan == '1'):
        filename = funtion.predict(testimage)
    else:
        filename = funtion.predict_Yolo(testimage)
    # filename = 'image/ttttt'+ str(name) +'.jpg'
    context={'filename':filename,'predictedLabel':'test', 'a' : '2'}
    return render(request, 'index.html', context)
