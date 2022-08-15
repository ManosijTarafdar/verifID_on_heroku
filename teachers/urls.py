from django import views
from django.contrib import admin
from django.urls import path , include
from . import views

urlpatterns = [
    path('',views.dashboard, name='dashboard'),
    path('routine/',views.routineTeacher, name='routineTeacher'),
    path('postAnnouncement/',views.announcement, name='postAnnouncement'),
    path('postAssignment/',views.uploadAssignment, name='postAssignment'),
    path('recordAttendance/',views.attendance, name='recordAttendance'),
    path('id/',views.myid, name='myId'),
    path('download/',views.get_routineDownloaded, name='downloadRoutine'),
    path('myid/',views.get_idDownloaded, name='downloadid'),
    path('archive/',views.archive,name = 'archive'),
    path('sendMessage/',views.sendMessage,name = 'adminMessage'),
    path('updatePassword/',views.updatePassword,name = 'updatePassword'),
    path('updateProfile/',views.updateProfile,name = 'updateProfile'),
    #test path
    path('test/',views.test,name = 'test'),
]