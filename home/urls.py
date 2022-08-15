from xml.etree.ElementInclude import include
from django.urls import path , include
from . import views

urlpatterns = [
    path('', views.homePage, name='home'),
    path('teacherDashboard/',include('teachers.urls')),
    path('logout/',views.logoutUser,name = 'logout'),
    path('register/',views.registerUser,name = 'register'),
    path('studentDashboard/',include('students.urls'))
]