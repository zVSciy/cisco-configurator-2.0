from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html')

def basic_config(request):
    return render(request, 'configurations/basic_config.html')

def interface(request):
    return render(request, 'configurations/interface.html')

def etherchannel(request):
    return render(request, 'configurations/etherchannel.html')

def vlan(request):
    return render(request, 'configurations/vlan.html')

def ospf(request):
    return render(request, 'configurations/ospf.html')

def rip(request):
    return render(request, 'configurations/rip.html')

def static_routing(request):
    return render(request, 'configurations/static_routing.html')

def nat(request):
    return render(request, 'configurations/nat.html')

def dhcp(request):
    return render(request, 'configurations/dhcp.html')

def acl_basic(request):
    return render(request, 'configurations/acl_basic.html')

def acl_extended(request):
    return render(request, 'configurations/acl_extendet.html')

def vtp_dtp(request):
    return render(request, 'configurations/vtp_dtp.html')

def stp(request):
    return render(request, 'configurations/stp.html')
