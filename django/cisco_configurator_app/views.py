from django.shortcuts import render
from .models import Router_Interfaces
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.urls import reverse
from .util.configManager import ConfigManager
from .util.deviceClasses import *
from .util.fileManager import *

# Create your views here.

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def basic_config(request, device_type):
    config_option = {
        "device_type": device_type
    }
    #print(config_option)
    return render(request, 'configurations/basic_config.html', config_option)

routerID = 1

def interface(request, device_type):
    config_option = {
        "device_type": device_type,
        "interfaces": Router_Interfaces.objects.filter(router_id=routerID)
    }
    return render(request, 'configurations/interface.html', config_option)

 
def etherchannel(request, device_type):
    config_option = {
        "device_type": device_type
    }
    return render(request, 'configurations/etherchannel.html', config_option)

 
def vlan(request, device_type):
    config_option = {
        "device_type": device_type
    }
    return render(request, 'configurations/vlan.html', config_option)

 
def ospf(request, device_type):
    config_option = {
        "device_type": device_type
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

 
def acl_basic(request, device_type):
    config_option = {
        "device_type": device_type
    }
    return render(request, 'configurations/acl_basic.html', config_option)

 
def acl_extended(request, device_type):
    config_option = {
        "device_type": device_type
    }
    return render(request, 'configurations/acl_extendet.html', config_option)

 
def vtp_dtp(request, device_type):
    config_option = {
        "device_type": device_type
    }
    return render(request, 'configurations/vtp_dtp.html', config_option)

 
def stp(request, device_type):
    config_option = {
        "device_type": device_type
    }
    return render(request, 'configurations/stp.html', config_option)

def get_inputs(request, device_type):
    config_option = {
        "device_type": device_type
    }

    cM = ConfigManager('exampleConfig.txt')

    forward_to = request.POST.get('hidden_forward_to')

    #basic config
    hostname = request.POST.get('hidden_hostname')
    banner = request.POST.get('hidden_banner')
    if(hostname and banner):
        cM.writeDeviceInfo(DeviceInfo(hostname, banner))

    #Interfaces
    nat_ingoing = request.POST.get('hidden_nat_ingoing')
    nat_outgoing = request.POST.get('hidden_nat_outgoing')  

    FastEthernet00_shutdown = request.POST.get('hidden_FastEthernet0/0_shutdown')  #true = on | false = off
    FastEthernet00_description = request.POST.get('hidden_FastEthernet0/0_description')
    FastEthernet00_ip = request.POST.get('hidden_FastEthernet0/0_ip')  
    FastEthernet00_sm = request.POST.get('hidden_FastEthernet0/0_sm')  
    FastEthernet01_shutdown = request.POST.get('hidden_FastEthernet0/1_shutdown')  #true = on | false = off
    FastEthernet01_description = request.POST.get('hidden_FastEthernet0/1_description')
    FastEthernet01_ip = request.POST.get('hidden_FastEthernet0/1_ip')  
    FastEthernet01_sm = request.POST.get('hidden_FastEthernet0/1_sm') 

    ##DEBUG
    FastEthernet01_shutdown = True
    FastEthernet00_shutdown = True

    if(nat_ingoing and nat_outgoing):
        if(nat_ingoing == 'FastEthernet00' and nat_outgoing == 'FastEthernet01'):
            cM.writeInterface(Interface('FastEthernet0/0', FastEthernet00_ip, FastEthernet00_sm, True, False, FastEthernet00_description, FastEthernet00_shutdown))
            cM.writeInterface(Interface('FastEthernet0/1', FastEthernet01_ip, FastEthernet01_sm, False, True, FastEthernet01_description, FastEthernet01_shutdown))
        else:
            cM.writeInterface(Interface('FastEthernet0/0', FastEthernet00_ip, FastEthernet00_sm, False, True, FastEthernet00_description, FastEthernet00_shutdown))
            cM.writeInterface(Interface('FastEthernet0/1', FastEthernet01_ip, FastEthernet01_sm, True, False, FastEthernet01_description, FastEthernet01_shutdown))
    else:
        cM.writeInterface(Interface('FastEthernet0/0', FastEthernet00_ip, FastEthernet00_sm, False, False, FastEthernet00_description, FastEthernet00_shutdown))
        cM.writeInterface(Interface('FastEthernet0/1', FastEthernet01_ip, FastEthernet01_sm, False, False, FastEthernet01_description, FastEthernet01_shutdown))

    #nat
    nat_status = request.POST.get('hidden_nat_status')  #true = on | false = off
    # acl_networks = request.POST.get('hidden_nat_info_for_transfer') 
    if(nat_status and nat_ingoing and nat_outgoing):
        cM.writeNATConfig(NAT(nat_outgoing, '0'))

    #dhcp
    dhcp_status = request.POST.get('hidden_dhcp_status')  #true = on | false = off
    dhcp_poolName = request.POST.get('hidden_dhcp_poolName')
    dhcp_network = request.POST.get('hidden_dhcp_Network')
    if dhcp_network:
        dhcp_network_IP = dhcp_network.split(',')[0]
        dhcp_network_SM = dhcp_network.split(',')[1]
    dhcp_dG = request.POST.get('hidden_dhcp_dG') 
    dhcp_dnsServer = request.POST.get('hidden_dhcp_dnsServer') 
    dhcp_info_for_transfer = request.POST.get('hidden_dhcp_info_for_transfer') 
    if(dhcp_status and dhcp_poolName and dhcp_network and dhcp_dG and dhcp_dnsServer and dhcp_info_for_transfer):
        cM.writeDhcpConfig(DHCP(dhcp_network_IP, dhcp_network_SM, dhcp_dG, dhcp_dnsServer, dhcp_info_for_transfer, dhcp_poolName))

    #rip
    rip_state = request.POST.get('hidden_rip_state')
    rip_version = request.POST.get('hidden_dropdown_rip_version')
    rip_sum_state = bool(request.POST.get('hidden_sum_state'))
    rip_originate_state = bool(request.POST.get('hidden_originate_state'))
    rip_networks = request.POST.get('hidden_networks_input_routing')
    if(rip_state and rip_version and rip_sum_state and rip_originate_state and rip_networks):
        cM.writeRIPConfig(RipRouting(rip_version, rip_sum_state, rip_originate_state, rip_networks))

    #static routing
    static_routes = request.POST.get('hidden_staticRouting_info_for_transfer')
    if(static_routes):
        cM.writeStaticRoutes(StaticRoute(static_routes))

    # exception for the index route bc index can`t handle the device type
    if forward_to != 'index':
        return redirect(reverse(forward_to + '_route', kwargs={'device_type': device_type}))
    else:
        return redirect(reverse(forward_to + '_route'))

def download_config(request):
  download_config(request)

def transfer_config(request):
  transfer_config(request)