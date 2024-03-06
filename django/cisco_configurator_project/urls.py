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
    path('basic-config/', views.basic_config, name='basic_config_route'),
    path('interface/', views.interface, name='interface_route'),
    path('etherchannel/', views.etherchannel, name='etherchannel_route'),
    path('vlan/', views.vlan, name='vlan_route'),
    path('ospf/', views.ospf, name='ospf_route'),
    path('rip/', views.rip, name='rip_route'),
    path('static-routing/', views.static_routing, name='static_routing_route'),
    path('nat/', views.nat, name='nat_route'),
    path('dhcp/', views.dhcp, name='dhcp_route'),
    path('acl-basic/', views.acl_basic, name='acl_basic_route'),
    path('acl-extended/', views.acl_extended, name='acl_extended_route'),
    path('vtp-dtp/', views.vtp_dtp, name='vtp_dtp_route'),
    path('stp/', views.stp, name='stp_route'),
]
