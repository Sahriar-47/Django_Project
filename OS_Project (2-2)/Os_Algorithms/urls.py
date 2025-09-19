"""
URL configuration for Os_Algorithms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Algorithms import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name="index"),
    path('fcfs/',views.fcfs,name="fcfs"),
    path('priority/', views.priority, name='priority'),
    path('sjf/',views.sjf, name="sjf"),
    path('p_sjf/',views.preemptive_sjf, name="preemptive_sjf"),
    path('rr/',views.round_robin,name="round_robin"),
    path('bkr/',views.bankers,name = "bankers_form"),
    path('fcfs_disk/', views.fcfs_disk_scheduling, name='fcfs_disk'),
    path('sstf_disk/', views.sstf_disk_scheduling, name='sstf_disk'),
    path('scan_disk/', views.scan_disk_scheduling, name='scan_disk'),
    path('cscan_disk/', views.cscan_disk_scheduling, name='cscan_disk'),
    path('look_disk/', views.look_disk_scheduling, name='look_disk'),
    path('clook_disk/', views.look_disk_scheduling, name='clook_disk'),
]
