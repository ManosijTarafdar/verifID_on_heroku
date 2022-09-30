from django.http import HttpResponse
from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required 
from teachers import views as teacherAuthViews
from teachers import credentials as cred
from pymongo import MongoClient
import pyrebase
import qrcode
import os
from verifID.settings import HOME_DIR
from PIL import Image , ImageDraw , ImageFont
from .models import StudentData
from datetime import datetime as dt
import teachers.credentials
import teachers.views as teacherView
import requests
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
# from teachers.decorators import allowed_users

# Create your views here.
@login_required(login_url='home')
# @allowed_users(allowed_roles=['students'])
def home(request):
    group = request.user.groups.all()[0].name
    if group == 'students':
        pass
    else:
        return render(request,'teachers/maintainence.html',context = {'message':'Not Authorized'})
    fname = request.user.first_name
    lname = request.user.last_name
    fullname = fname + " " + lname
    email = request.user.email
    userObj = StudentData.objects.get(email = email)
    department = userObj.department
    year = userObj.year
    cid = userObj.collegeid
    context = {
        'fullname':fullname,
        'year':year,
        'department':department,
        'cid':cid,
    }
    return render(request,'students/dashboard.html',context)

def makeid(request):
    studentDataObject = StudentData.objects.all().get(email = request.user.email)
    # make qr
    qr_img = qrcode.make(studentDataObject.collegeid) 
    # os.chdir(os.path.join(HOME_DIR+"\\etc"))
    qr_img.save("etc/qr.jpg")
    # # make idcard
    template = Image.open("etc/template.png")
    draw = ImageDraw.Draw(template)
    font = ImageFont.truetype("etc/Ubuntu-Regular.ttf",size=26)
    draw.text((366,245),dt.now().strftime('%d/%m/%Y'),fill = "black",font=font)
    nameOfUser = studentDataObject.firstname + " " + studentDataObject.lastname
    draw.text((376,115),nameOfUser,fill = "black",font=font)
    draw.text((473,160),"STUDENT",fill = "black",font=font)
    draw.text((371,210),studentDataObject.department,fill = "black",font=ImageFont.truetype("etc/Ubuntu-Regular.ttf",size=20))
    pic = Image.open('etc/qr.jpg').resize((196,218),Image.ANTIALIAS)
    template.paste(pic,(61,116,257,334))
    template.save("etc/idCard.png")
    fireStoreObject = teacherView.fireStore()
    path = request.user.first_name + request.user.last_name + "/idCard.png"
    fireStoreObject.child(path).put("etc/idCard.png")
    fname = request.user.first_name
    lname = request.user.last_name
    teacherName = fname + lname
    downPath = teacherName+"/idCard.png"
    fireStoreObject = teacherView.fireStore()
    downloadURL = fireStoreObject.child(downPath).get_url(None)
    response = HttpResponse(content_type = "image/png")
    response['Content-Disposition'] = "attachment;filename=idCard.png"
    response.write(requests.get(downloadURL).content)
    return response

def myRoutine(request):
    userObj = StudentData.objects.get(email = request.user.email)
    stream = userObj.department
    year = userObj.year
    destinationPath = "routines/"+stream+"/"+year+"/"+'classroutine.png'
    fireStoreObject = teacherView.fireStore()
    imgurl =  fireStoreObject.child(destinationPath).get_url(None)
    context = {
        'image':imgurl,
    }
    return render(request,'students/myRoutine.html',context)

def myAttendance(request):
    return render(request,'students/maintainence.html',context = {'message':'Feature Coming Soon.'})

# @login_required(login_url='studentHome')
def announcements(request):
    myFireRDB = teacherAuthViews.fireData()
    dataList = myFireRDB.get()
    subDataList = list()
    dataListObject = list()
    for i in dataList:
        dataListObject.append(i.val()['subjectCode'])
        dataListObject.append(i.val()['date'])
        dataListObject.append(i.val()['teacher'])
        dataListObject.append(i.key())
        subDataList.append(dataListObject.copy())
        dataListObject.clear()
    context = {
        'dataList':subDataList[::-1],
    }
    return render(request,'students/myAnnouncements.html',context)

def view_announcement(request,id):
    myFireRDB = teacherAuthViews.fireData()
    dataList = myFireRDB.child(id).get()
    about = dataList.val()['text']
    return render(request,'students/details.html',context = {'message':about})

def assignments(request):
    # cluster URL
    clusterURL = "mongodb+srv://"+cred.MONGODB_USERNAME+":"+cred.MONGODB_PASSWORD+"@attendanccedb.vkkyk.mongodb.net/?retryWrites=true&w=majority"
    # setup connection with cluster
    myCluster = MongoClient(clusterURL,tls=True,tlsAllowInvalidCertificates=True)
    # setup connection with database
    myDB = myCluster["announcementData"]
    # setup connnection with collection
    collectionName = "collection01"
    myCollection = myDB[collectionName]
    dataList = myCollection.find({})
    subDataList = list()
    subDataListObject = list()
    for data in dataList:
        subDataListObject.append(data['subjectCode'])
        subDataListObject.append(data['about'])
        subDataListObject.append(data['datePosted'])
        subDataListObject.append(data['dateOfSubmit'])
        subDataListObject.append(data['filePath'])
        subDataList.append(subDataListObject.copy())
        subDataListObject.clear()
    context = {
        'dataList':subDataList[::-1],
    }
    return render(request,'students/myAssignments.html',context)

def update(request):
    if request.method == "POST":
        # newEmail = request.POST['email']
        newPhone = request.POST['phoneno']
        newAddr = request.POST['address']
        userObj = StudentData.objects.get(email = request.user.email)
        # userObj.email = newEmail
        userObj.phoneno = newPhone
        userObj.address = newAddr
        userObj.save()
        return redirect('home')
    # email = request.user.email
    phone = request.user.studentdata.phoneno
    address = request.user.studentdata.address
    context = {
        # 'email':email,
        'phone':phone,
        'address':address,
    }
    return render(request,'students/update.html',context)   

def updatePassword(request):
    if request.method == "POST":
        oldPass = request.POST['oldpassword']
        newPass = request.POST['newpassword']
        confNewPass = request.POST['confpassword']
        userPassword = request.user.password
        checkForAuth = check_password(oldPass,userPassword)
        if checkForAuth is False or newPass != confNewPass:
            return HttpResponse("Auth Denied")
        uname = request.user.username
        uobj = User.objects.get(username=uname)
        uobj.set_password(newPass)
        uobj.save()
        return redirect('updatePassword')   
    return render(request,'students/updatePassword.html')

def messageAdmin(request):
    if request.method == 'POST':
        message = request.POST['message']
        # cluster URL
        clusterURL = "mongodb+srv://"+teachers.credentials.MONGODB_USERNAME+":"+teachers.credentials.MONGODB_PASSWORD+"@attendanccedb.vkkyk.mongodb.net/?retryWrites=true&w=majority"
        # setup connection with cluster
        myCluster = MongoClient(clusterURL,tls=True,tlsAllowInvalidCertificates=True)
        # setup connection with database
        myDB = myCluster["adminMessage"]
        # setup connnection with collection
        myCollection = myDB["teachers"]
        timeStamp = dt.now().strftime('%d-%m-%y')
        data = {
            'Date':timeStamp,
            'Teacher':request.user.first_name + " " + request.user.last_name,
            'Message':message
        }
        myCollection.insert_one(data)
        return redirect('studentHome')
    return render(request,'students/messageAdmin.html')