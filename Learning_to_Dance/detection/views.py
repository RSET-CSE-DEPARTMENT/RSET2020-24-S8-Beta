from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from  django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
import datetime

from .models import *
import os
import shutil

#from ML import test_data

def download_generated_dance(request):
    # Replace '/path/to/your/video.mp4' with the actual path to your MP4 file.
    sel=uploads.objects.get(id=request.GET.get("id"))
    file_path = 'media/{}'.format(sel.result)
    print("filepath:",file_path)

    # Open the file in binary mode
    with open(file_path, 'rb') as file:
        # Read the file content
        file_content = file.read()

    # Create a response with the file content
    response = HttpResponse(file_content, content_type='video/mp4')

    # Set the 'Content-Disposition' header to trigger the download
    response['Content-Disposition'] = f'attachment; filename="{file_path.split("/")[-1]}"'

    return response

def first(request):
    return render(request,'index.html')

def index(request):
    return render(request,'index.html')

def register(request):
    return render(request,'register.html')

def registration(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        password=request.POST.get('password')

        reg=registerr(name=name,email=email,password=password)
        reg.save()
    return render(request,'index.html')

def login(request):
    return render(request,'login.html')

def addlogin(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    if email == 'admin@gmail.com' and password =='admin':
        request.session['logintdetail'] = email
        request.session['admin'] = 'admin'
        return render(request,'index.html')

    elif registerr.objects.filter(email=email,password=password).exists():
        userdetails=registerr.objects.get(email=request.POST['email'], password=password)
        if userdetails.password == request.POST['password']:
            request.session['uid'] = userdetails.id
        
        return render(request,'index.html')
        
    else:
        return render(request, 'login.html', {'success':'Invalid email id or Password'})
    
def logout(request):
    session_keys = list(request.session.keys())
    for key in session_keys:
        del request.session[key]
    return redirect(first)

def v_users(request):
    user = registerr.objects.all()
    return render(request, 'viewusers.html', {'result': user})

def test(request):
    return render(request,'test.html')

def addfile(request):
    if request.method=="POST":
        u_id = request.session['uid']
        
        file = request.FILES['file']

        try:
            os.remove("test.wav")
            shutil.rmtree("output")
        except:
            pass

        fs = FileSystemStorage(location="./")
        fs.save("test.wav",file)
        fs = FileSystemStorage()
        file = fs.save(file.name,file)


        #result=test_data.predict()
        os.system('python main.py -p test --input test.wav\
                   --cpk_path weights/generator.pt --audio_ckp weights/audio_classifier.pt --out_video output')
        file_content=""
        for i in ['ballet','michael','salsa']:
            file_path="output/{}/{}_combined.mp4".format(i,i)
            #print("file_path:",file_path)
            try:
                with open(file_path, 'rb') as files:
                    file_content = files.read()
                break
            except:
                pass
        
        """with open("output/michael/michael_black.mp4", 'rb') as files:
            file_content = files.read()"""

        fs = FileSystemStorage()
        file_content_as_file = ContentFile(file_content)
        filename=fs.save("step_generated.mp4", file_content_as_file)

        print("Result:",filename)

        cus=uploads(u_id=u_id,result=str(filename),file=file)
        cus.save()
        return redirect(index)
    
def v_result(request):
    uid=request.session['uid']
    user = uploads.objects.filter(u_id=uid)
    return render(request, 'viewresult.html', {'result': user})

def v_results(request):
    user = uploads.objects.all()
    return render(request, 'viewresult.html', {'result': user})


    

def live(request):
    return render(request,'live.html')