# import cv2
# import threading
from Camara.Code import VideoCamara as vc
from Camara.Code import VideoCamara2 as vc2
from django.http import StreamingHttpResponse
from django.shortcuts import render
#########################################
from django.views.decorators import gzip


#########################################

def inicio(request):
    return render(request, 'inicio.html')


@gzip.gzip_page
def testCamara(request):
    # return render(request,'Camara/index.html')
    ###########################################
    try:
        cam = vc.VideoCamara()
        return StreamingHttpResponse(vc.gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        pass
    return render(request, 'Camara/index.html')
    ###########################################


@gzip.gzip_page
def testCamara2(request):
    # return render(request,'Camara/index.html')
    ###########################################
    try:
        cam = vc2.VideoCamara2()
        return StreamingHttpResponse(vc2.gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        pass
    return render(request, 'Camara/index.html')
    ###########################################
