"""
URL configuration for cisco_configurator_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.shortcuts import redirect
from cisco_configurator_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/', admin.site.urls),
    path('index/', views.index, name='index_route'),
    path('', lambda request: redirect('index_route', permanent=False)),
    # routing of config pages
    path('basic-config/<str:device_type>/', views.basic_config, name='basic_config_route'),
    path('interface/<str:device_type>/', views.interface, name='interface_route'),
    path('etherchannel/<str:device_type>/', views.etherchannel, name='etherchannel_route'),
    path('vlan/<str:device_type>/', views.vlan, name='vlan_route'),
    path('ospf/<str:device_type>/', views.ospf, name='ospf_route'),
    path('rip/<str:device_type>/', views.rip, name='rip_route'),
    path('static-routing/<str:device_type>/', views.static_routing, name='static_routing_route'),
    path('nat/<str:device_type>/', views.nat, name='nat_route'),
    path('dhcp/<str:device_type>/', views.dhcp, name='dhcp_route'),
    path('acl-basic/<str:device_type>/', views.acl_basic, name='acl_basic_route'),
    path('acl-extended/<str:device_type>/', views.acl_extended, name='acl_extended_route'),
    path('vtp-dtp/<str:device_type>/', views.vtp_dtp, name='vtp_dtp_route'),
    path('stp/<str:device_type>/', views.stp, name='stp_route'),
    path('config/<str:device_type>/', views.get_inputs, name='get_inputs_route'),
    # path('transfer/', views.transfer_config, name='transfer_route'),
    # path('download/', views.download_config, name='download_route'),
]
