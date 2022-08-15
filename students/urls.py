from django import views
from django.contrib import admin
from django.urls import path , include
from . import views

urlpatterns = [
    path('',views.home,name='studentHome'),
    path('myID',views.makeid,name='myID'),
    path('myRoutine',views.myRoutine,name='myRoutine'),
    path('myAttendance',views.myAttendance,name='myAttendance'),
    path('myAnnouncements/',views.announcements,name='announcementHome'),
    path('viewAnnouncement/<str:id>/',views.view_announcement,name='viewAnnouncement'),
    path('myAssignments/',views.assignments,name='assignmentsHome'),
    path('update/',views.update,name='update'),
    path('updatePassword/',views.updatePassword,name='updatePasswordStudent'),
    path('messageAdmin/',views.messageAdmin,name='messageAdmin'),
]