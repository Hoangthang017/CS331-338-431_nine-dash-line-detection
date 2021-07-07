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


def predictImage(request):
    fileObj = request.FILES['filePath']
    fs = FileSystemStorage()
    filePathName = fs.save(fileObj.name, fileObj)
    filePathName = fs.url(fileObj)
    testimage = '.' + filePathName
    funtion.predict(testimage)
    filename = 'image/ttttt.jpg'
    context={'filename':filename,'predictedLabel':'test', 'a' : '2'}
    return render(request, 'index.html', context)
