from django.shortcuts import render
from .models import Router_Interfaces
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.urls import reverse
from .util.configManager import ConfigManager
from .util.deviceClasses import *
from .util.deviceClasses import Interface
from .util.fileManager import transfer_config
from .util.fileManager import download_config
6
# Create your views here.

routerID = 1

def get_interfaces(device_type):
    if device_type == 'router':
        return Router_Interfaces.objects.filter(router_id=1)
    elif device_type == 'switch':
        return Router_Interfaces.objects.filter(router_id=2)

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def basic_config(request, device_type, config_mode):

    config_option = {
        "device_type": device_type,
        "interfaces":  get_interfaces(device_type),
        "config_mode": config_mode,
        "hostname": 'test', #! replace 'test' with real hostname that gets loaded from the exampleConfig when the site gets invoked
        "banner": 'test'
    }

    # print(config_mode)
    return render(request, 'configurations/basic_config.html', config_option)



def interface(request, device_type, config_mode):
    config_option = {
        "device_type": device_type,
        "interfaces":  get_interfaces(device_type),
        "config_mode": config_mode,
        "interface_shutdowns": [],
        "interface_descriptions": [],
        "interface_ips": [],
        "interface_sms": []
    }


    #loading
    interface_list = [] # this List should be filled with Interface Objects (from the Class in the from deviceClasses file)

    # DEBUGGING :(
    interface_list.append(Interface('FastEthernet0/0','1.1.1.1','2.2.2.2',False,False,'Test',True)) 
    interface_list.append(Interface('FastEthernet0/1','5.5.5.5','2.2.2.2',False,False,'Fa0/1',False))

    for interface in interface_list:
        config_option["interface_shutdowns"].append(interface.shutdown) 
        config_option["interface_descriptions"].append(interface.description) 
        config_option["interface_ips"].append(interface.ip) 
        config_option["interface_sms"].append(interface.sm)

    return render(request, 'configurations/interface.html', config_option)

 
def etherchannel(request, device_type, config_mode):
    config_option = {
        "device_type": device_type,
        "interfaces":  get_interfaces(device_type),
        "config_mode": config_mode
    }
    return render(request, 'configurations/etherchannel.html', config_option)

 
def vlan(request, device_type, config_mode):
    config_option = {
        "device_type": device_type,
        "interfaces":  get_interfaces(device_type),
        "config_mode": config_mode,
        "vlans": '1,gfhfgh;11,hallo;',# replace with real data from config if site gets invoked (mind the format)
        "vlan_interfaces":'Ethernet0/0,access,1;Ethernet0/1,trunk,1,11:12;'# replace with real data from config if site gets invoked (mind the format)
        #Acces Interface Fomrat: [Interface],[access],[vlan_id];
        #Trunking Interface Fomrat: [Interface],[trunk],[native_vlan_id],[allowed_vlan:allowed_vlan...];
    }
    return render(request, 'configurations/vlan.html', config_option)

 
def ospf(request, device_type, config_mode):
    config_option = {
        "device_type": device_type,
        "interfaces":  get_interfaces(device_type),
        "config_mode": config_mode,
        "process": '5',# string number
        "router_id": '1.1.1.1', # IP-Address
        "ospf_networks": '1.1.1.1,2.2.2.2,0;3.3.3.3,4.4.4.4,0;' # replace with real data from config if site gets invoked (mind the format)
    }
    return render(request, 'configurations/ospf.html', config_option)

 
def rip(request, device_type, config_mode):
    config_option = {
        "device_type": device_type,
        "interfaces":  get_interfaces(device_type),
        "config_mode": config_mode,
        "rip_state": 'true', #'true' or 'false'
        "rip_version": '2', # must be 1 or 2
        "rip_sum_state": True, #True or False
        "rip_originate_state": False, #True or False
        "rip_networks": '1.1.1.1,2.2.2.2' #True or False
    }
    return render(request, 'configurations/rip.html', config_option)

 
def static_routing(request, device_type, config_mode):
    config_option = {
        "device_type": device_type,
        "interfaces":  get_interfaces(device_type),
        "config_mode": config_mode,
        "static_routes": '1.1.1.1,2.2.2.2,3.3.3.3;5.5.5.5,6.6.6.6,7.7.7.7;' # replace with real data from config if site gets invoked
    }
    return render(request, 'configurations/static_routing.html', config_option)

def nat(request, device_type, config_mode):
    config_option = {
        "device_type": device_type,
        "interfaces":  get_interfaces(device_type),
        "config_mode": config_mode,
        "nat_state": 'true', #replace 'true' with real nat_state that gets loaded from the exampleConfig when the site gets invoked (can be 'true' or 'false')
        "ingoing_interface": 'FastEthernet0/1', # replace with real
        "outgoing_interface": 'FastEthernet0/0', # repleace with real
        "networks":'1.1.1.1,2.2.2.2;3.3.3.3,4.4.4.4;' # replace with real
    }

    
    return render(request, 'configurations/nat.html', config_option)

 
def dhcp(request, device_type, config_mode):
    config_option = {
        "device_type": device_type,
        "interfaces":  get_interfaces(device_type),
        "config_mode": config_mode,
        "dhcp_state": 'true', #replace 'true' with real dhcp_state that gets loaded from the exampleConfig when the site gets invoked (can be 'true' or 'false')
        "dhcp_poolName": 'pool1',# replace with real
        "dhcp_Network": '10.0.0.0, 255.255.255.0',# replace with real
        "dhcp_defaultGateway": '10.0.0.1',# replace with real
        "dhcp_DNS_server": '8.8.8.8',# replace with real
        "dhcp_excluded_Adresses": '1.1.1.1,5.5.5.5;1.1.1.1,5.5.5.5;'# replace with real

    }
    return render(request, 'configurations/dhcp.html', config_option)

 
def acl_basic(request, device_type, config_mode):
    config_option = {
        "device_type": device_type,
        "interfaces":  get_interfaces(device_type),
        "config_mode": config_mode,
        "ACLs": '1,permit,1.1.1.1,2.2.2.2;2,permit,8.8.8.8,0.0.0.255;' #replace with real ACLs that gets loaded from the exampleConfig when the site gets invoked (mind the format)

    }
    return render(request, 'configurations/acl_basic.html', config_option)

 
def acl_extended(request, device_type, config_mode):
    config_option = {
        "device_type": device_type,
        "interfaces":  get_interfaces(device_type),
        "config_mode": config_mode,
        "ACLs":'1,permit,1.1.1.1,2.2.2.2,3.3.3.3,4.4.4.4,80;5,deny,5.5.5.5,6.6.6.6,7.7.7.7,8.8.8.8,443;'#replace with real ACLs that gets loaded from the exampleConfig when the site gets invoked (mind the format)
    }
    return render(request, 'configurations/acl_extendet.html', config_option)

 
def vtp_dtp(request, device_type, config_mode):
    config_option = {
        "device_type": device_type,
        "interfaces":  get_interfaces(device_type),
        "config_mode": config_mode
    }
    return render(request, 'configurations/vtp_dtp.html', config_option)

 
def stp(request, device_type, config_mode):
    config_option = {
        "device_type": device_type,
        "interfaces":  get_interfaces(device_type),
        "config_mode": config_mode
    }
    return render(request, 'configurations/stp.html', config_option)

def get_inputs(request, device_type, config_mode):# in this function the input that comes from the hidden form in the frontend gets made accessable for the backend
    config_option = {
        "device_type": device_type,
        "interfaces":  get_interfaces(device_type),
        "config_mode": config_mode
    }

    cM = ConfigManager('exampleConfig')

    forward_to = request.POST.get('hidden_forward_to')

    #inputs from the index site (load from ROuter Switch inputs)
    load_from_ipAddress = request.POST.get('loadFromIpAddress')
    load_from_username = request.POST.get('loadFromUsername')
    load_from_password = request.POST.get('loadFromPassword')

    #basic config
    hostname = request.POST.get('hidden_hostname')
    banner = request.POST.get('hidden_banner')
    if(hostname and banner):
        cM.writeDeviceInfo(DeviceInfo(hostname, banner))

    
    nat_ingoing = request.POST.get('hidden_nat_ingoing')
    nat_outgoing = request.POST.get('hidden_nat_outgoing')  

    #Interfaces
    Interface_List = [] # ! List to store the Interfaces as an Interface Object in 

    if request.POST.get('hidden_'+config_option["interfaces"][0].port_name+'_shutdown') != '':
        if request.POST.get('hidden_'+config_option["interfaces"][0].port_name+'_shutdown') != None:
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


    ##DEBUG
    # print(Interface_List)
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
    acl_networks = request.POST.get('hidden_nat_info_for_transfer') 
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

    #ospf
    ospf_info_for_transfer = request.POST.get('hidden_ospf_info_for_transfer')
    ospf_router_id = request.POST.get('hidden_ospf_router_id')
    ospf_process = request.POST.get('hidden_ospf_process')

    #basic acl
    basic_acl_info_for_transfer = request.POST.get('hidden_basic_acl_info_for_transfer')

    #extended acl
    extended_acl_info_for_transfer = request.POST.get('hidden_extended_acl_info_for_transfer')

    #vlan
    vlan_info_for_transfer = request.POST.get('hidden_vlan_info_for_transfer')
    vlan_interfaces_info_for_transfer = request.POST.get('hidden_vlan_interfaces_info_for_transfer')


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
        return redirect(reverse(forward_to + '_route', kwargs={'device_type': device_type, 'config_mode': config_mode}))
    else:
        return redirect('index_route')