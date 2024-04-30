from django.shortcuts import render
from .models import Router_Interfaces
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.urls import reverse
from .util.configManager import ConfigManager
from .util.deviceClasses import *

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
    #! reset running-config file content
    return render(request, 'index.html')

def create_objects(cm):
    return [
        cm.getDeviceInfo(), 
        cm.getAllInterfaces(), 
        cm.getStaticRoutes(), 
        cm.getRIPConfig(), 
        cm.getDhcpConfig(), 
        cm.getNATConfig()
    ]

def get_inputs(request, device_type, config_mode):
    config_option = {
        'device_type': device_type,
        'config_mode': config_mode,
        'interfaces':  get_interfaces(device_type)
    }

    forward_to = request.POST.get('hidden_forward_to')

    #! if file leer
    if(config_option.get('config_mode') == 'create'):
        if(config_option.get('device_type') == 'router'):
            #! template-config-router in running-config
            pass
        elif(config_option.get('device_type') == 'switch'):
            #! template-config-switch in running-config
            pass
    elif(config_option.get('config_mode') == 'load'):
        #! loaded-config in running-config
        pass

    cm = ConfigManager('running-config')
    config_objects = create_objects(cm)


########################################################################

    #basic config
    hostname = request.POST.get('hidden_hostname')
    banner = request.POST.get('hidden_banner')

    #! serversided check for hostname and banner

    config_objects[0].hostname = hostname
    config_objects[0].banner = banner
    cm.writeDeviceInfo(config_objects[0])

########################################################################


    nat_ingoing = request.POST.get('hidden_nat_ingoing')
    nat_outgoing = request.POST.get('hidden_nat_outgoing')  

    #Interfaces
    Interface_List = [] # ! List to store the Interfaces as an Interface Object in 

    if request.POST.get('hidden_'+config_option["interfaces"][0].port_name+'_shutdown') != '':
        for i in config_option["interfaces"]:
            interfaces_shutdown = request.POST.get('hidden_'+i.port_name+'_shutdown')
            interfaces_description = request.POST.get('hidden_'+i.port_name+'_description')
            interfaces_ip = request.POST.get('hidden_'+i.port_name+'_ip')
            interfaces_sm = request.POST.get('hidden_'+i.port_name+'_sm')
            nat_inside = False
            nat_outside = False
            if nat_ingoing == i.port_name:
                nat_inside = True
            if nat_outgoing == i.port_name:
                nat_outside = True
                
            interfaces_shutdown = True if interfaces_shutdown == 'true' else False

            Interface_List.append(Interface(i.port_name, interfaces_ip, interfaces_sm, nat_inside, nat_outside, interfaces_description, interfaces_shutdown))

    print(Interface_List)
    ##DEBUG
    # FastEthernet01_shutdown = True
    # FastEthernet00_shutdown = True

    # if(nat_ingoing and nat_outgoing):
    #     if(nat_ingoing == 'FastEthernet00' and nat_outgoing == 'FastEthernet01'):
    #         fe00 = cM.getInterface("FastEthernet0/0")
    #         fe01 = cM.getInterface("FastEthernet0/1")
    #         fe00.ipNatInside = True
    #         fe00.ipNatOutside = False

    #         fe01.ipNatInside = False
    #         fe01.ipNatOutside = True
    #         cM.writeInterface(fe00)
    #         cM.writeInterface(fe01)
    #     else:
    #         fe00 = cM.getInterface("FastEthernet0/0")
    #         fe01 = cM.getInterface("FastEthernet0/1")
    #         fe00.ipNatInside = False
    #         fe00.ipNatOutside = True

    #         fe01.ipNatInside = True
    #         fe01.ipNatOutside = False
    #         cM.writeInterface(fe00)
    #         cM.writeInterface(fe01)
    # elif (FastEthernet00_ip):
    #     cM.writeInterface(Interface('FastEthernet0/0', FastEthernet00_ip, FastEthernet00_sm, False, False, FastEthernet00_description, FastEthernet00_shutdown))
    #     cM.writeInterface(Interface('FastEthernet0/1', FastEthernet01_ip, FastEthernet01_sm, False, False, FastEthernet01_description, FastEthernet01_shutdown))

    #nat
    nat_status = request.POST.get('hidden_nat_status')  #true = on | false = off
    # acl_networks = request.POST.get('hidden_nat_info_for_transfer') 
    if(nat_status and nat_ingoing and nat_outgoing):
        cM.writeNATConfig(NAT(nat_outgoing, '2'))

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

    dl_or_tf = request.POST.get('hidden_dl_or_tf')
    ip = request.POST.get('hidden_ip')
    user = request.POST.get('hidden_user')
    pw = request.POST.get('hidden_pw')

    response = ''

    if dl_or_tf == 'download':
        response = download_config()
    elif dl_or_tf == 'transfer':
        response = transfer_config(ip, user, pw)

    if response:
        return response




    # exception for the index route bc index can`t handle the device type
    if forward_to != 'index':
        return redirect(reverse(forward_to + '_route', kwargs={'device_type': device_type}))
    else:
        return redirect('index_route')




