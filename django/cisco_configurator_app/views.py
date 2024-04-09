from django.shortcuts import render
from .models import Router_Interfaces
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
 
def index(request):
    return render(request, 'index.html')

@csrf_exempt
def basic_config(request):
    config_option = {
        "device_type": request.POST.get('deviceType')
    }
    print(config_option)
    return render(request, 'configurations/basic_config.html', config_option)

routerID = 1
 
def interface(request):
    config_option = {
        "device_type": request.POST.get('deviceType'),
        "interfaces": Router_Interfaces.objects.filter(router_id=routerID)
    }
    return render(request, 'configurations/interface.html', config_option)

 
def etherchannel(request):
    config_option = {
        "device_type": request.POST.get('deviceType')
    }
    return render(request, 'configurations/etherchannel.html', config_option)

 
def vlan(request):
    config_option = {
        "device_type": request.POST.get('deviceType')
    }
    return render(request, 'configurations/vlan.html', config_option)

 
def ospf(request):
    config_option = {
        "device_type": request.POST.get('deviceType')
    }
    return render(request, 'configurations/ospf.html', config_option)

 
def rip(request):
    config_option = {
        "device_type": request.POST.get('deviceType')
    }
    return render(request, 'configurations/rip.html', config_option)

 
def static_routing(request):
    config_option = {
        "device_type": request.POST.get('deviceType')
    }
    return render(request, 'configurations/static_routing.html', config_option)

 
def nat(request):
    config_option = {
        "device_type": request.POST.get('deviceType'),
        "interfaces": Router_Interfaces.objects.filter(router_id=routerID)
    }
    return render(request, 'configurations/nat.html', config_option)

 
def dhcp(request):
    config_option = {
        "device_type": request.POST.get('deviceType')
    }
    return render(request, 'configurations/dhcp.html', config_option)

 
def acl_basic(request):
    config_option = {
        "device_type": request.POST.get('deviceType')
    }
    return render(request, 'configurations/acl_basic.html', config_option)

 
def acl_extended(request):
    config_option = {
        "device_type": request.POST.get('deviceType')
    }
    return render(request, 'configurations/acl_extendet.html', config_option)

 
def vtp_dtp(request):
    config_option = {
        "device_type": request.POST.get('deviceType')
    }
    return render(request, 'configurations/vtp_dtp.html', config_option)

 
def stp(request):
    config_option = {
        "device_type": request.POST.get('deviceType')
    }
    return render(request, 'configurations/stp.html', config_option)
