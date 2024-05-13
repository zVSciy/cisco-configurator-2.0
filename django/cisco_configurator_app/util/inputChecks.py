from ..models import Router_Interfaces
import re

ip_pattern = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
sm_pattern = r'^((255|254|252|248|240|224|192|128|0)\.){3}(255|254|252|248|240|224|192|128|0)$'

def get_interfaces(device_type):
    if device_type == 'router':
        return Router_Interfaces.objects.filter(router_id=1)
    elif device_type == 'switch':
        return Router_Interfaces.objects.filter(router_id=2)

def checkHostname(hostname):
    if isinstance(hostname, str):
        return hostname
    else: return ''

def checkBanner(banner):
    if isinstance(banner, str):
        return banner
    else: return ''

def checkIntShutdown(shutdown):
    if shutdown == 'true':
        return True
    else: return False

def checkIntDescription(description):
    if isinstance(description, str):
        return description
    else: return ''

def checkIntIP(ip):
    if ip == None:
        return ''
    if re.match(ip_pattern, ip):
        return ip
    else: return ''

def checkIntSM(sm):
    if sm == None:
        return ''
    if re.match(sm_pattern, sm):
        return sm
    else: return ''

def checkStaticRoutes(routes):
    if routes in ('', None):
        return ''
    validation = True
    splitted_routes = routes.split(';')
    for route in splitted_routes:
        route = route.split(',')
        targetNW = route[0]
        targetSM = route[1]
        nextHOP = route[2]
        if not re.match(ip_pattern, targetNW) or not re.match(sm_pattern, targetSM) or not re.match(ip_pattern, nextHOP):
            validation = False
    if validation:
        return routes
    else: return ''

def checkRIPversion(version):
    if version in ('1', '2'):
        return version
    else: return ''

def checkRIPsumState(state):
    if state in ('true', 'false'):
        if state == 'true':
            return True
        else: return False
    else: return ''

def checkRIPoriginateState(state):
    if state in ('true', 'false'):
        if state == 'true':
            return True
        else: return False
    else: return ''

def checkRIPnetworks(networks):
    if networks in ('', None):
        return ''
    validation = True
    splitted_networks = networks.split(';')
    for network in splitted_networks:
        network = network.split(',')
        network_ip = network[0]
        network_wcm = network[1]
        if not re.match(ip_pattern, network_ip) or not re.match(sm_pattern, network_wcm):
            validation = False
    if validation:
        return networks
    else: return ''

def checkDHCPpoolName(name):
    if isinstance(name, str):
        return name
    else: return ''

def checkDHCPnetworkIP(ip):
    if ip == None:
        return ''
    if re.match(ip_pattern, ip):
        return ip
    else: return ''

def checkDHCPnetworkSM(sm):
    if sm == None:
        return ''
    if re.match(sm_pattern, sm):
        return sm
    else: return ''

def checkDHCPgateway(gateway):
    if gateway == None:
        return ''
    if re.match(ip_pattern, gateway):
        return gateway
    else: return ''

def checkDHCPdns(dns):
    if dns == None:
        return ''
    if re.match(ip_pattern, dns):
        return dns
    else: return ''

def checkDHCPexcludedAreas(areas):
    if areas in ('', None):
        return ''
    validation = True
    splitted_areas = areas.split(';')
    for areas in splitted_areas:
        area = areas.split(',')
        from_ip = area[0]
        to_ip = area[1]
        if not re.match(ip_pattern, from_ip):
            validation = False
        if to_ip != '':
            if not re.match(ip_pattern, to_ip):
                validation = False
    if validation:
        return areas
    else: return ''

def checkNATingoing(int, device):
    for i in get_interfaces(device):
        if i.port_name == int:
            return int
    return ''

def checkNAToutgoing(int, device):
    for i in get_interfaces(device):
        if i.port_name == int:
            return int
    return ''

def checkACLnetworks(networks):
    if networks in ('', None):
        return ''
    validation = True
    splitted_networks = networks.split(';')
    for network in splitted_networks:
        network = network.split(',')
        network_ip = network[0]
        network_wcm = network[1]
        if not re.match(ip_pattern, network_ip) or not re.match(sm_pattern, network_wcm):
            validation = False
    if validation:
        return networks
    else: return ''