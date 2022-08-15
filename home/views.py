from django.shortcuts import redirect, render
from django.contrib.auth import authenticate , login , logout
from django.http import HttpResponse
from teachers.models import TeacherData
import uuid,re
# Create your views here.
def homePage(request):
    # If already logged in
    if request.user.is_authenticated:
        group = request.user.groups.all()[0].name
        if group == 'teachers':
            return redirect('teacherDashboard/')
        elif group == 'students':
            return redirect('studentDashboard/')
        else:
            return HttpResponse("NOT AUTHORIZED")
    # Initial login
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        userobj = authenticate(request,username=username, password = password)
        if userobj is not None:
            login(request,userobj)
            group = request.user.groups.all()[0].name
            if group == 'teachers':
                return redirect('teacherDashboard/')
            elif group == 'students':
                return redirect('studentDashboard/')
            else:
                return HttpResponse("NOT AUTHORIZED")
    return render(request,'home/landing.html')

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    teacher = "False"
    student = 'False'
    try:
        teacher = request.POST['teacher']
    except:
        try:
            student = request.POST['student']
        except:
            pass
    if request.method == "POST" and teacher == "True":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        collegeid = request.POST['collegeid']
        designation = request.POST['designation']
        department = request.POST['department']
        phone = request.POST['phone']
        address = request.POST['address']
        macAddress = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        teacherDataObject = TeacherData(collegeid = collegeid,firstname = fname,lastname = lname,email = email,designation = designation,department = department,phoneno = phone,address = address,deviceid = macAddress)
        teacherDataObject.save()
    return render(request,'home/register.html')