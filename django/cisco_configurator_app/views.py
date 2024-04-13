from django.shortcuts import render
from .models import Router_Interfaces
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.urls import reverse

# Create your views here.
 
def index(request):
    return render(request, 'index.html')

@csrf_exempt
def basic_config(request, device_type):
    config_option = {
        "device_type": device_type
    }
    print(config_option)
    return render(request, 'configurations/basic_config.html', config_option)

routerID = 1
 
def interface(request, device_type):
    config_option = {
        "device_type": device_type,
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

 
def rip(request, device_type):
    config_option = {
        "device_type": device_type
    }
    return render(request, 'configurations/rip.html', config_option)

 
def static_routing(request, device_type):
    config_option = {
        "device_type": device_type
    }
    return render(request, 'configurations/static_routing.html', config_option)

 
def nat(request, device_type):
    config_option = {
        "device_type": device_type,
        "interfaces": Router_Interfaces.objects.filter(router_id=routerID)
    }
    return render(request, 'configurations/nat.html', config_option)

 
def dhcp(request, device_type):
    config_option = {
        "device_type": device_type
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

def get_inputs(request, device_type):
    config_option = {
        "device_type": device_type
    }
    forward_to = request.POST.get('hidden_forward_to')

    #basic config
    hostname = request.POST.get('hidden_hostname')
    banner = request.POST.get('hidden_banner')

    #Interfaces
    FastEthernet00_shutdown = request.POST.get('hidden_FastEthernet0/0_shutdown')  #true = on | false = off
    FastEthernet00_description = request.POST.get('hidden_FastEthernet0/0_description')
    FastEthernet00_ip = request.POST.get('hidden_FastEthernet0/0_ip')  
    FastEthernet00_sm = request.POST.get('hidden_FastEthernet0/0_sm')  

    FastEthernet01_shutdown = request.POST.get('hidden_FastEthernet0/1_shutdown')  #true = on | false = off
    FastEthernet01_description = request.POST.get('hidden_FastEthernet0/1_description')
    FastEthernet01_ip = request.POST.get('hidden_FastEthernet0/1_ip')  
    FastEthernet01_sm = request.POST.get('hidden_FastEthernet0/1_sm') 

    #NAT
    nat_status = request.POST.get('hidden_nat_status')  #true = on | false = off
    nat_ingoing = request.POST.get('hidden_nat_ingoing')
    nat_outgoing = request.POST.get('hidden_nat_outgoing')  
    acl_networks = request.POST.get('hidden_nat_info_for_transfer') 

    #dhcp
    dhcp_status = request.POST.get('hidden_dhcp_status')  #true = on | false = off
    dhcp_poolName = request.POST.get('hidden_dhcp_poolName')
    dhcp_Network = request.POST.get('hidden_dhcp_Network')  
    dhcp_dG = request.POST.get('hidden_dhcp_dG') 
    dhcp_dnsServer = request.POST.get('hidden_dhcp_dnsServer') 
    dhcp_info_for_transfer = request.POST.get('hidden_dhcp_info_for_transfer') 

    #rip
    rip_state = request.POST.get('hidden_rip_state')  #true = on | false = off
    rip_networks = request.POST.get('hidden_networks_input_routing')
    rip_version = request.POST.get('hidden_dropdown_rip_version')
    rip_auto_sum_state = request.POST.get('hidden_sum_state')
    rip_originate_state = request.POST.get('hidden_originate_state')

    #static routing
    static_routing_routes = request.POST.get('hidden_staticRouting_info_for_transfer')


    # return render(request, 'configurations/'+forward_to+'.html', config_option)
    return redirect(reverse(forward_to + '_route', kwargs={'device_type': device_type}))