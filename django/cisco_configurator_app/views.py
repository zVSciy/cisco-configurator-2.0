from django.shortcuts import render
from .models import Router_Interfaces
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.urls import reverse
from .util.configManager import ConfigManager
from .util.deviceClasses import *
from .util.fileManager import *
from .util.inputChecks import *
import os

# Create your views here.

routerID = 1

def get_interfaces(device_type):
    if device_type == 'router':
        return Router_Interfaces.objects.filter(router_id=routerID)
    elif device_type == 'switch':
        return Router_Interfaces.objects.filter(router_id=routerID)



@csrf_exempt
def basic_config(request, device_type):

    config_option = {
        "device_type": device_type,
        "interfaces":  get_interfaces(device_type)
    }

    #print(config_option)
    return render(request, 'configurations/basic_config.html', config_option)



def interface(request, device_type):
    config_option = {
        "device_type": device_type,
        "interfaces":  get_interfaces(device_type)
    }
    return render(request, 'configurations/interface.html', config_option)

 
def etherchannel(request, device_type):
    config_option = {
        "device_type": device_type,
        "interfaces":  get_interfaces(device_type)
    }
    return render(request, 'configurations/etherchannel.html', config_option)

 
def vlan(request, device_type):
    config_option = {
        "device_type": device_type,
        "interfaces":  get_interfaces(device_type)
    }
    return render(request, 'configurations/vlan.html', config_option)

 
def ospf(request, device_type):
    config_option = {
        "device_type": device_type,
        "interfaces":  get_interfaces(device_type)
    }
    return render(request, 'configurations/ospf.html', config_option)

 
def rip(request, device_type):
    config_option = {
        "device_type": device_type,
        "interfaces":  get_interfaces(device_type)
    }
    return render(request, 'configurations/rip.html', config_option)

 
def static_routing(request, device_type):
    config_option = {
        "device_type": device_type,
        "interfaces":  get_interfaces(device_type)
    }
    return render(request, 'configurations/static_routing.html', config_option)

def nat(request, device_type):
    config_option = {
        "device_type": device_type,
        "interfaces":  get_interfaces(device_type)
    }
    return render(request, 'configurations/nat.html', config_option)

 
def dhcp(request, device_type):
    config_option = {
        "device_type": device_type,
        "interfaces":  get_interfaces(device_type)
    }
    return render(request, 'configurations/dhcp.html', config_option)

 
def acl_basic(request, device_type):
    config_option = {
        "device_type": device_type,
        "interfaces":  get_interfaces(device_type)
    }
    return render(request, 'configurations/acl_basic.html', config_option)

 
def acl_extended(request, device_type):
    config_option = {
        "device_type": device_type,
        "interfaces":  get_interfaces(device_type)
    }
    return render(request, 'configurations/acl_extendet.html', config_option)

 
def vtp_dtp(request, device_type):
    config_option = {
        "device_type": device_type,
        "interfaces":  get_interfaces(device_type)
    }
    return render(request, 'configurations/vtp_dtp.html', config_option)

 
def stp(request, device_type):
    config_option = {
        "device_type": device_type,
        "interfaces":  get_interfaces(device_type)
    }
    return render(request, 'configurations/stp.html', config_option)





def index(request):
    emptyConfigFile('running-config')
    return render(request, 'index.html')

def create_objects(cm):
    return [
        cm.getDeviceInfo(), 
        cm.getAllInterfaces(), 
        cm.getStaticRoutes(), 
        cm.getRIPConfig(), 
        cm.getDhcpConfig(), 
        cm.getNATConfig(),
        cm.getACLConfig(),
    ]

def get_inputs(request, device_type, config_mode):
    config_option = {
        'device_type': device_type,
        'config_mode': config_mode,
        'interfaces':  get_interfaces(device_type)
    }

    ip = request.POST.get('hidden_ip')
    user = request.POST.get('hidden_user')
    pw = request.POST.get('hidden_pw')

    if os.path.getsize('./util/running-config') == 0:
        if(config_option.get('config_mode') == 'create'):
            if(config_option.get('device_type') == 'router'):
                copyConfigFile('template-config-router.txt','running-config')
            elif(config_option.get('device_type') == 'switch'):
                copyConfigFile('template-config-switch.txt','running-config')
        elif(config_option.get('config_mode') == 'load'):
            transfer_config(ip, user, pw, direction='get')

    cm = ConfigManager('running-config')
    config_objects = create_objects(cm)


########################################################################

    #basic config
    hostname = request.POST.get('hidden_hostname')
    banner = request.POST.get('hidden_banner')

    config_objects[0].hostname = checkHostname(hostname)
    config_objects[0].banner = checkBanner(banner)
    cm.writeDeviceInfo(config_objects[0])

########################################################################

    #interfaces
    for i in config_option["interfaces"]:
        interfaces_shutdown = request.POST.get('hidden_' + i.port_name + '_shutdown')
        interfaces_description = request.POST.get('hidden_' + i.port_name + '_description')
        interfaces_ip = request.POST.get('hidden_' + i.port_name + '_ip')
        interfaces_sm = request.POST.get('hidden_' + i.port_name + '_sm')

        for j in config_objects[1]:
            if j.interface == i.port_name:
                j.shutdown == checkIntShutdown(interfaces_shutdown)
                j.description == checkIntDescription(interfaces_description)
                j.ip == checkIntIP(interfaces_ip)
                j.sm == checkIntSM(interfaces_sm)
                cm.writeInterface(j)

########################################################################

    #static routing
    static_routes = request.POST.get('hidden_staticRouting_info_for_transfer')

    config_objects[2].staticRouting = checkStaticRoutes(static_routes)
    cm.writeStaticRoutes(config_objects[2])

########################################################################

    #rip
    rip_version = request.POST.get('hidden_dropdown_rip_version')
    rip_sum_state = request.POST.get('hidden_sum_state')
    rip_originate_state = request.POST.get('hidden_originate_state')
    rip_networks = request.POST.get('hidden_networks_input_routing')

    config_objects[3].ripVersion = checkRIPversion(rip_version)
    config_objects[3].ripSumState = checkRIPsumState(rip_sum_state)
    config_objects[3].ripOriginate = checkRIPoriginateState(rip_originate_state)
    config_objects[3].ripNetworks = checkRIPnetworks(rip_networks)
    cm.writeRIPConfig(config_objects[3])

########################################################################

    #dhcp
    dhcp_poolName = request.POST.get('hidden_dhcp_poolName')
    dhcp_network_IP = ''
    dhcp_network_SM = ''
    with request.POST.get('hidden_dhcp_Network') as network:
        if network:
            dhcp_network_IP = network.split(',')[0]
            dhcp_network_SM = network.split(',')[1]
    dhcp_dG = request.POST.get('hidden_dhcp_dG') 
    dhcp_dnsServer = request.POST.get('hidden_dhcp_dnsServer') 
    dhcp_excludedAreas = request.POST.get('hidden_dhcp_info_for_transfer') 

    config_objects[4].dhcpPoolName = checkDHCPpoolName(dhcp_poolName)
    config_objects[4].dhcpNetworkIP = checkDHCPnetworkIP(dhcp_network_IP)
    config_objects[4].dhcpNetworkSM = checkDHCPnetworkSM(dhcp_network_SM)
    config_objects[4].dhcpGateway = checkDHCPgateway(dhcp_dG)
    config_objects[4].dhcpDNS = checkDHCPdns(dhcp_dnsServer)
    config_objects[4].dhcpExcludedAreas = checkDHCPexcludedAreas(dhcp_excludedAreas)
    cm.writeDhcpConfig(config_objects[4])

########################################################################

    #nat
    nat_ingoing = request.POST.get('hidden_nat_ingoing')
    nat_outgoing = request.POST.get('hidden_nat_outgoing')
    acl_networks = request.POST.get('hidden_nat_info_for_transfer')

    #! serversided check for nat values

    current_interfaces = cm.getAllInterfaces()

    for i in current_interfaces:
        if i.interface == nat_ingoing:
            i.ipNatInside = True
        if i.interface == nat_outgoing:
            i.ipNatOutside = True
        cm.writeInterface(i)

    config_objects[5].interfaceName = nat_outgoing
    config_objects[5].aclName = '1'
    cm.writeNATConfig(config_objects[5])

    current_acls = cm.getACLConfig()

    to_remove = []
    for i, acl in enumerate(current_acls.ACLs):
        if acl.id == '1':
            to_remove.append(i)
    for index in reversed(to_remove):
        del current_acls.ACLs[index]
    
    current_acls.getACLs(acl_networks) # adding acls to ACLs list
    cm.writeACLConfig(config_objects[6])

########################################################################


    response = ''

    dl_or_tf = request.POST.get('hidden_dl_or_tf')

    if dl_or_tf == 'download':
        response = download_config()
    elif dl_or_tf == 'transfer':
        response = transfer_config(ip, user, pw)

    if response:
        return response

    forward_to = request.POST.get('hidden_forward_to')
    # exception for the index route because index can`t handle the device type
    if forward_to != 'index':
        return redirect(reverse(forward_to + '_route', kwargs={'device_type': device_type}))
    else:
        return redirect('index_route')
