from ..models import Router_Interfaces
import re

# return the interface names of router or switch
def get_interfaces(device_type):
    if device_type == 'router':
        return Router_Interfaces.objects.filter(router_id=1)
    elif device_type == 'switch':
        return Router_Interfaces.objects.filter(router_id=2)

ip_pattern = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
sm_pattern = r'^((255|254|252|248|240|224|192|128|0)\.){3}(255|254|252|248|240|224|192|128|0)$'

########################################################################

#region BASIC CONFIG

#checks the hostname input
def checkHostname(hostname):
    if isinstance(hostname, str):
        return hostname
    else: return ''

#checks the banner input
def checkBanner(banner):
    if isinstance(banner, str):
        return banner
    else: return ''

########################################################################

#region INTERFACES

#checks the interface shutdown state
def checkIntShutdown(shutdown):
    if shutdown == 'true':
        return True
    else: return False

#checks the interface description
def checkIntDescription(description):
    if isinstance(description, str):
        return description
    else: return ''

#checks the interface ip
def checkIntIP(ip):
    if type(ip) == str:
        if re.match(ip_pattern, ip):
            return ip
        return ''
    else: return ''

#checks the interface subnet mask
def checkIntSM(sm):
    if type(sm) == str:
        if re.match(sm_pattern, sm):
            return sm
        return ''
    else: return ''

########################################################################

#region STATIC ROUTING

#checks the static routing input string
def checkStaticRoutes(routes):
    if type(routes) != str or routes == '':
        return ''
    validation = True
    splitted_routes = routes.split(';')
    if splitted_routes[-1] == '':
        splitted_routes.pop()
    for route in splitted_routes:
        route = route.split(',')
        if len(route) != 3:
            validation = False
            break
        targetNW = route[0]
        targetSM = route[1]
        nextHOP = route[2]
        if not re.match(ip_pattern, targetNW) or not re.match(sm_pattern, targetSM) or not re.match(ip_pattern, nextHOP):
            validation = False
    if validation:
        return routes
    else: return ''

########################################################################

#region RIP

#checks if rip version is 1 or 2
def checkRIPversion(version):
    if version in ('1', '2'):
        return version
    else: return ''

#checks the rip auto summary state
def checkRIPsumState(state):
    if state in ('true', 'false'):
        if state == 'true':
            return True
        else: return False
    else: return ''

#checks the rip originate state
def checkRIPoriginateState(state):
    if state in ('true', 'false'):
        if state == 'true':
            return True
        else: return False
    else: return ''

#checks the rip network string
def checkRIPnetworks(networks):
    if type(networks) != str or networks == '':
        return ''
    validation = True
    splitted_networks = networks.split(';')
    if splitted_networks[-1] == '':
        splitted_networks.pop()
    for network in splitted_networks:
        if not re.match(ip_pattern, network):
            validation = False
    if validation:
        return networks
    else: return ''

########################################################################

#region DHCP

#checks DHCP pool name
def checkDHCPpoolName(name):
    if isinstance(name, str):
        return name
    else: return ''

#checks DHCP network ip
def checkDHCPnetworkIP(ip):
    if type(ip) == str:
        if re.match(ip_pattern, ip):
            return ip
        return ''
    else: return ''

#checks DHCP network sm
def checkDHCPnetworkSM(sm):
    if type(sm) == str:
        if re.match(sm_pattern, sm):
            return sm
        return ''
    else: return ''

#checks DHCP gateway ip
def checkDHCPgateway(gateway):
    if type(gateway) == str:
        if re.match(ip_pattern, gateway):
            return gateway
        return ''
    else: return ''

#checks DHCP dns ip
def checkDHCPdns(dns):
    if type(dns) == str:
        if re.match(ip_pattern, dns):
            return dns
        return ''
    else: return ''

#checks DHCP excluded areas (from - to)
def checkDHCPexcludedAreas(areas):
    if type(areas) != str or areas == '':
        return ''
    validation = True
    areas_str = areas
    splitted_areas = areas.split(';')
    if splitted_areas[-1] == '':
        splitted_areas.pop()
    for areas in splitted_areas:
        area = areas.split(',')
        if len(area) != 2:
            validation = False
            break
        from_ip = area[0]
        to_ip = area[1]
        if not re.match(ip_pattern, from_ip):
            validation = False
        if to_ip != '':
            if not re.match(ip_pattern, to_ip):
                validation = False
    if validation:
        return areas_str
    else: return ''

########################################################################

#region NAT

#checks the NAT ingoing interface
def checkNATingoing(int):
    for i in get_interfaces('router'):
        if i.port_name == int:
            return int
    return ''

#checks the NAT outgoing interface
def checkNAToutgoing(int):
    for i in get_interfaces('router'):
        if i.port_name == int:
            return int
    return ''

#checks if both NAT interfaces are correct
def checkNATinterfaces(int1, int2):
    if '' not in (checkNATingoing(int1), checkNAToutgoing(int2)):
        if int1 == int2:
            return ''
        return [int1, int2]
    return ''

#checks the ACL network string
def checkNATnetworks(networks):
    if type(networks) != str or networks == '':
        return ''
    validation = True
    networks_str = networks
    splitted_networks = networks.split(';')
    if splitted_networks[-1] == '':
        splitted_networks.pop()
    for network in splitted_networks:
        network = network.split(',')
        if len(network) != 2:
            validation = False
            break
        network_ip = network[0]
        network_wcm = network[1]
        if not re.match(ip_pattern, network_ip) or not re.match(sm_pattern, network_wcm):
            validation = False
    if validation:
        return networks_str
    else: return ''

########################################################################

#region OSPF

#checks the ospf process id
def checkOSPFprocess(id):
    if type(id) == str:
        if id.isdigit():
            return id
        return ''
    else: return ''

#checks the ospf router id
def checkOSPFrouterID(ip):
    if ip == None:
        return ''
    if re.match(ip_pattern, ip):
        return ip
    return ''

#checks the ospf auto summary state
def checkOSPFsumState(state):
    if state in ('true', 'false'):
        if state == 'true':
            return True
        else: return False
    else: return ''

#checks the ospf originate default route state
def checkOSPForiginateState(state):
    if state in ('true', 'false'):
        if state == 'true':
            return True
        else: return False
    else: return ''

#checks the ospf networks
def checkOSPFnetworks(networks):
    if type(networks) != str or networks == '':
        return ''
    validation = True
    networks_str = networks
    splitted_networks = networks.split(';')
    if splitted_networks[-1] == '':
        splitted_networks.pop()
    for network in splitted_networks:
        network = network.split(',')
        if len(network) != 3:
            validation = False
            break
        network_ip = network[0]
        network_wcm = network[1]
        area_id = network[2]
        if not re.match(ip_pattern, network_ip) or not re.match(sm_pattern, network_wcm) or not area_id.isdigit():
            validation = False
    if validation:
        return networks_str
    else: return ''

########################################################################

#region BASIC ACL

def checkBasicACLs(acls):
    if type(acls) != str or acls == '':
        return ''
    validation = True
    acls_str = acls
    splitted_acls = acls.split(';')
    if splitted_acls[-1] == '':
        splitted_acls.pop()
    for acl in splitted_acls:
        acl = acl.split(',')
        if len(acl) != 4:
            validation = False
            break
        acl_id = acl[0]
        acl_decision = acl[1]
        acl_ip = acl[2]
        acl_sm = acl[3]
        if not acl_id.isdigit() or not acl_decision in ('permit', 'deny') or not re.match(ip_pattern, acl_ip) or not re.match(sm_pattern, acl_sm):
            validation = False
    if validation:
        return acls_str
    else: return ''

########################################################################

#region EXTENDED ACL

def checkExtendedACLs(acls):
    if type(acls) != str or acls == '':
        return ''
    validation = True
    acls_str = acls
    splitted_acls = acls.split(';')
    if splitted_acls[-1] == '':
        splitted_acls.pop()
    for acl in splitted_acls:
        acl = acl.split(',')
        if len(acl) != 7:
            validation = False
            break
        acl_id = acl[0]
        acl_decision = acl[1]
        acl_source_ip = acl[2]
        acl_source_wm = acl[3]
        acl_dest_ip = acl[4]
        acl_dest_wm = acl[5]
        acl_port = acl[6]
        if not acl_id.isdigit() or not acl_decision in ('permit', 'deny') or not re.match(ip_pattern, acl_source_ip) or not re.match(sm_pattern, acl_source_wm) or not re.match(ip_pattern, acl_dest_ip) or not re.match(sm_pattern, acl_dest_wm) or not int(acl_port) >= 1 or not int(acl_port) <= 65535:
            validation = False
    if validation:
        return acls_str
    else: return ''
