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

cm = ConfigManager(configFilePath="running-config")

# return the interface names of router or switch
def get_interfaces(device_type):
    if device_type == 'router':
        return Router_Interfaces.objects.filter(router_id=1)
    elif device_type == 'switch':
        return Router_Interfaces.objects.filter(router_id=2)

# every function named after an configuration possibility calles the correspondig site and gives the needed data to the site via the config_option dict


# function to get config data to basic-config site
@csrf_exempt
def basic_config(request, device_type, config_mode): 

    input_data = cm.getDeviceInfo()

    config_option = {
        "device_type": device_type,
        "interfaces":  get_interfaces(device_type),
        "config_mode": config_mode,
        "hostname": input_data.hostname, 
        "banner": input_data.motd #! banner motd is not getting read out of the config properly
    }

    return render(request, 'configurations/basic_config.html', config_option)


# function to get config data to interface site
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
    # interface_list.append(Interface('FastEthernet0/0','1.1.1.1','2.2.2.2',False,False,'Test',True)) 
    # interface_list.append(Interface('FastEthernet0/1','5.5.5.5','2.2.2.2',False,False,'Fa0/1',False))

    for interface in config_option['interfaces']:
        interface_from_config = cm.getInterface(interface.port_name)
        interface_list.append(interface_from_config)

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


# def vlan(request, device_type, config_mode):

#     config_option = {
#         "device_type": device_type,
#         "interfaces":  get_interfaces(device_type),
#         "config_mode": config_mode,
#         "vlans": '1,gfhfgh;11,hallo;',# replace with real data from config if site gets invoked (mind the format)
#         "vlan_interfaces":'Ethernet0/0,access,1;Ethernet0/1,trunk,1,11:12;'# replace with real data from config if site gets invoked (mind the format)
#         #Acces Interface Fomrat: [Interface],[access],[vlan_id];
#         #Trunking Interface Fomrat: [Interface],[trunk],[native_vlan_id],[allowed_vlan:allowed_vlan...];
#     }
#     return render(request, 'configurations/vlan.html', config_option)


# function to get config data to ospf site
def ospf(request, device_type, config_mode):

    input_data = cm.getAllOSPFConfig()

    if len(input_data) == 0:
        config_option = {
            "device_type": device_type,
            "interfaces":  get_interfaces(device_type),
            "config_mode": config_mode,
            "process": '',
            "router_id": '',
            "ospf_networks": '' 
        }
    else:
        config_option = {
            "device_type": device_type,
            "interfaces":  get_interfaces(device_type),
            "config_mode": config_mode,
            "process": input_data[0].ospfProcess,# string number #!by now GUI only supports 1 ospf process 
            "router_id": input_data[0].ospfRouterID, # IP-Address
            "ospf_networks": '' 
        }

        for network in input_data[0].ospfNetworks:
            config_option['ospf_networks'] += f"{network['networkID']},{network['networkWM']},{network['area']};"

    return render(request, 'configurations/ospf.html', config_option)


# function to get config data to rip site
def rip(request, device_type, config_mode):

    input_data = cm.getRIPConfig()

    config_option = {
        "device_type": device_type,
        "interfaces":  get_interfaces(device_type),
        "config_mode": config_mode,
        "rip_state": 'true', #always 'true' (ignore)
        "rip_version": input_data.ripVersion, # must be 1 or 2
        "rip_sum_state": input_data.ripSumState, #True or False
        "rip_originate_state": input_data.ripOriginate, #True or False
        "rip_networks": '' #Network string
    }

    # get inputs

    formatted_rip_networks = ''

    for network in input_data.ripNetworks:
        formatted_rip_networks += network + ','

    config_option['rip_networks'] = formatted_rip_networks[:-1]

    return render(request, 'configurations/rip.html', config_option)


# function to get config data to static_routing site
def static_routing(request, device_type, config_mode):

    input_data = cm.getStaticRoutes()

    config_option = {
        "device_type": device_type,
        "interfaces":  get_interfaces(device_type),
        "config_mode": config_mode,
        "static_routes": '' # replace with real data from config if site gets invoked
    }

    for route in input_data.routes:
        config_option['static_routes'] += f"{route['targetNw']},{route['targetSm']},{route['nextHop']};"

    return render(request, 'configurations/static_routing.html', config_option)


# function to get config data to nat site
def nat(request, device_type, config_mode):

    input_data_NAT = cm.getNATConfig()
    input_data_ACL = cm.getACLConfig()
    input_data_Interfaces = cm.getAllInterfaces()

    config_option = {
        "device_type": device_type,
        "interfaces":  get_interfaces(device_type),
        "config_mode": config_mode,
        "nat_state": 'true', #always true (ignore)
        "ingoing_interface": '', 
        "outgoing_interface": '', 
        "networks":'' 
    }

    # get inputs

    for interface in input_data_Interfaces:
        if interface.ipNatInside == True:
            config_option['ingoing_interface'] = interface.interface
        if interface.ipNatOutside == True:
            config_option['outgoing_interface'] = interface.interface

    for acl in input_data_ACL.ACLs:
        if acl['id'] == input_data_NAT.accessList:
            config_option['networks'] += f"{acl['ip']},{acl['sm']};"

    
    return render(request, 'configurations/nat.html', config_option)


# function to get config data to dhcp site
def dhcp(request, device_type, config_mode):

    input_data = cm.getDhcpConfig("pool")

    config_option = {
        "device_type": device_type,
        "interfaces":  get_interfaces(device_type),
        "config_mode": config_mode,
        "dhcp_state": 'true', # always true (ignore)
        "dhcp_poolName": input_data.dhcpPoolName,# replace with real
        "dhcp_Network": input_data.dhcpNetworkIP +','+ input_data.dhcpNetworkSM,# replace with real
        "dhcp_defaultGateway": input_data.dhcpGateway,# replace with real
        "dhcp_DNS_server": input_data.dhcpDNS,# replace with real
        "dhcp_excluded_Adresses": ''# replace with real
    }

    for area in input_data.areas:
        config_option['dhcp_excluded_Adresses'] += f"{area['AreaFromIP']},{area['AreaToIP']};"

    if config_option['dhcp_Network'] == ',':
        config_option['dhcp_Network'] = ''

    return render(request, 'configurations/dhcp.html', config_option)


# function to get config data to basic acl site
def acl_basic(request, device_type, config_mode):

    input_data = cm.getACLConfig()

    config_option = {
        "device_type": device_type,
        "interfaces":  get_interfaces(device_type),
        "config_mode": config_mode,
        "ACLs": '' # replace with real ACLs that gets loaded from the exampleConfig when the site gets invoked (mind the format)
    }

    for acl in input_data.ACLs:
        config_option['ACLs'] += f"{acl['id']},{acl['permitDeny']},{acl['ip']},"
        if 'sm' in acl:
            config_option['ACLs'] += acl['sm'] + ';'
        else:
            config_option['ACLs'] += ';'

    return render(request, 'configurations/acl_basic.html', config_option)


# function to get config data to extendet acl site
def acl_extended(request, device_type, config_mode):

    input_data = cm.getAllACLConfig()

    config_option = {
        "device_type": device_type,
        "interfaces":  get_interfaces(device_type),
        "config_mode": config_mode,
        "ACLs":''
    }

    for acl in input_data: 
        for rule in acl.aclList:
            config_option['ACLs'] += f"{acl.aclRuleName},{rule['permitDeny']},{rule['sourceIP']},{rule['sourceWM']},{rule['destIP']},{rule['destWM']},{rule['port']};"

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


# empties the running-config file every time the index page is called
def index(request):
    emptyConfigFile('running-config',cm=cm)
    return render(request, 'index.html')


# return an array with all config objects
def create_objects(cm):
    return [
        cm.getDeviceInfo(), 
        cm.getAllInterfaces(), 
        cm.getStaticRoutes(), 
        cm.getRIPConfig(), 
        cm.getDhcpConfig("172"), #! hardcoded for now, 172 is the default id for the dhcp config
        cm.getNATConfig(),
        cm.getACLConfig(),
    ]


# gets the inputs from the POST request of the fronend and writes them into the config
def get_inputs(request, device_type, config_mode):
    config_option = {
        'device_type': device_type,
        'config_mode': config_mode,
        'interfaces':  get_interfaces(device_type)
    }

    load_ip = request.POST.get('loadFromIpAddress')
    load_user = request.POST.get('loadFromUsername')
    load_pw = request.POST.get('loadFromPassword')

    script_dir = os.path.dirname(os.path.realpath(__file__))
    # join the script directory with the file path
    # outputPath = outputPath if outputPath != None else filePath
    # filePath = os.path.join(script_dir, filePath)
    runningConfigPath = os.path.join(script_dir, 'util/running-config')
    
    if os.path.getsize(runningConfigPath) == 0:
        if(config_option.get('config_mode') == 'new'):
            if(config_option.get('device_type') == 'router'):
                copyConfigFile('template-config-router.txt','running-config', cm = cm)
            elif(config_option.get('device_type') == 'switch'):
                copyConfigFile('template-config-switch.txt','running-config', cm = cm)
        elif(config_option.get('config_mode') == 'load'):
            transfer_config(load_ip, load_user, load_pw, direction='get')

    config_objects = create_objects(cm)

########################################################################

    #basic config
    hostname = request.POST.get('hidden_hostname')
    banner = request.POST.get('hidden_banner')

    #check values
    if '' not in (checkHostname(hostname), checkBanner(banner)):

        config_objects[0].hostname = checkHostname(hostname)
        config_objects[0].motd = checkBanner(banner)
        cm.writeDeviceInfo(config_objects[0])

########################################################################

    #interfaces
    for i in config_option["interfaces"]:
        interfaces_shutdown = request.POST.get('hidden_' + i.port_name + '_shutdown')
        interfaces_description = request.POST.get('hidden_' + i.port_name + '_description')
        interfaces_ip = request.POST.get('hidden_' + i.port_name + '_ip')
        interfaces_sm = request.POST.get('hidden_' + i.port_name + '_sm')

        #check values
        if '' not in (checkIntShutdown(interfaces_shutdown), checkIntDescription(interfaces_description), checkIntIP(interfaces_ip), checkIntSM(interfaces_sm)):

            for j in config_objects[1]:
                if j.interface == i.port_name:
                    j.shutdown = checkIntShutdown(interfaces_shutdown)
                    j.description = checkIntDescription(interfaces_description)
                    j.ip = checkIntIP(interfaces_ip)
                    j.sm = checkIntSM(interfaces_sm)
                    cm.writeInterface(j)

########################################################################

    #static routing
    static_routes = request.POST.get('hidden_staticRouting_info_for_transfer')

    #check values
    if '' != checkStaticRoutes(static_routes):

        config_objects[2].getRoutes(checkStaticRoutes(static_routes))
        cm.writeStaticRoutes(config_objects[2])

########################################################################

    #rip
    rip_version = request.POST.get('hidden_dropdown_rip_version')
    rip_sum_state = request.POST.get('hidden_sum_state')
    rip_originate_state = request.POST.get('hidden_originate_state')
    rip_networks = request.POST.get('hidden_networks_input_routing')

    #check values
    if '' not in (checkRIPversion(rip_version), checkRIPsumState(rip_sum_state), checkRIPoriginateState(rip_originate_state), checkRIPnetworks(rip_networks)):

        rip_sum_state = True if rip_sum_state == 'true' else False
        rip_originate_state = True if rip_originate_state == 'true' else False

        config_objects[3].ripVersion = checkRIPversion(rip_version)
        config_objects[3].ripSumState = rip_sum_state
        config_objects[3].ripOriginate = rip_originate_state
        config_objects[3].ripNetworks = config_objects[3].getNetworks(checkRIPnetworks(rip_networks))
        cm.writeRIPConfig(config_objects[3])

########################################################################

    #dhcp
    dhcp_poolName = request.POST.get('hidden_dhcp_poolName')
    dhcp_network_IP = ''
    dhcp_network_SM = ''
    network = request.POST.get('hidden_dhcp_Network')
    try:
        dhcp_network_IP = network.split(',')[0]
        dhcp_network_SM = network.split(',')[1]
    except:
        dhcp_network_IP = ""
        dhcp_network_SM = ""
    dhcp_dG = request.POST.get('hidden_dhcp_dG') 
    dhcp_dnsServer = request.POST.get('hidden_dhcp_dnsServer') 
    dhcp_excludedAreas = request.POST.get('hidden_dhcp_info_for_transfer') 

    #check values
    if '' not in (checkDHCPpoolName(dhcp_poolName), checkDHCPnetworkIP(dhcp_network_IP), checkDHCPnetworkSM(dhcp_network_SM), checkDHCPgateway(dhcp_dG), checkDHCPdns(dhcp_dnsServer), checkDHCPexcludedAreas(dhcp_excludedAreas)):

        config_objects[4].dhcpPoolName = checkDHCPpoolName(dhcp_poolName)
        config_objects[4].dhcpNetworkIP = checkDHCPnetworkIP(dhcp_network_IP)
        config_objects[4].dhcpNetworkSM = checkDHCPnetworkSM(dhcp_network_SM)
        config_objects[4].dhcpGateway = checkDHCPgateway(dhcp_dG)
        config_objects[4].dhcpDNS = checkDHCPdns(dhcp_dnsServer)
        config_objects[4].getAreas(checkDHCPexcludedAreas(dhcp_excludedAreas))
        cm.writeDhcpConfig(config_objects[4])

########################################################################

    #vlan
        # vlan_vlans = request.POST.get('hidden_vlan_info_for_transfer')
        # vlan_interfaces = request.POST.get('hidden_vlan_interfaces_info_for_transfer')

########################################################################

    #nat
    nat_ingoing = request.POST.get('hidden_nat_ingoing')
    nat_outgoing = request.POST.get('hidden_nat_outgoing')
    acl_networks = request.POST.get('hidden_nat_info_for_transfer')

    #check values
    if '' not in (checkNATingoing(nat_ingoing, device_type), checkNAToutgoing(nat_outgoing, device_type), checkACLnetworks(acl_networks)):

        current_interfaces = cm.getAllInterfaces()

        for i in current_interfaces:
            if i.interface == nat_ingoing:
                i.ipNatInside = True
            if i.interface == nat_outgoing:
                i.ipNatOutside = True
            cm.writeInterface(i)

        config_objects[5].interface = nat_outgoing
        config_objects[5].accessList = '1'
        cm.writeNATConfig(config_objects[5])

        current_acls = cm.getACLConfig()

        to_remove = []
        for i, acl in enumerate(current_acls.ACLs):
            if acl.get("id") == '1':
                to_remove.append(i)
        for index in reversed(to_remove):
            del current_acls.ACLs[index]

        acl_networks = acl_networks.split(';')
        for i, network in enumerate(acl_networks):
            if len(network) == 0:
                continue
            acl_networks[i] = '1,permit,' + network
        acl_networks = ';'.join(acl_networks)
        current_acls.getACLs(acl_networks) # adding acls to ACLs list
        cm.writeACLConfig(current_acls)

########################################################################

    ip = request.POST.get('hidden_ip')
    user = request.POST.get('hidden_user')
    pw = request.POST.get('hidden_pw')

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
        return redirect(reverse(forward_to + '_route', kwargs={'device_type': device_type, 'config_mode': config_mode}))
    else:
        return redirect('index_route')
