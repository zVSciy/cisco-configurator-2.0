from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from netmiko import ConnectHandler, SCPConn
from django.http import FileResponse, HttpResponseBadRequest
import os

local_config_file = './django/cisco_configurator_app/util/running-config'
remote_config_file = 'system:running-config'

def transfer_config(ip, user, pw, direction='put'):
    try:
        target = {
            'device_type': 'cisco_ios',
            'host': ip,
            'username': user,
            'password': pw,
        }
        net_conn = ConnectHandler(**target)
        scp_conn = SCPConn(net_conn)
        if direction == 'put':
            scp_conn.scp_transfer_file(local_config_file, remote_config_file)
        elif direction == 'get':
            scp_conn.scp_transfer_file(remote_config_file, local_config_file)
        else: raise ValueError('Invalid direction.')
        net_conn.disconnect()
    except Exception as ex:
        print(ex)
        return HttpResponseBadRequest(ex)

def download_config():
    try:
        return FileResponse(open(local_config_file, 'rb'), as_attachment=True, filename='config.txt')
    except Exception as ex:
        print(ex)
        return HttpResponseBadRequest(ex)

def emptyConfigFile(file):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    file = os.path.join(script_dir, file)
    try:
        with open(file, 'w'): pass
    except Exception as ex:
        print(ex)
        return HttpResponseBadRequest(ex)

def copyConfigFile(src_file, dest_file):
    try:
        script_dir = os.path.dirname(os.path.realpath(__file__))
        src_dir = os.path.join(script_dir, src_file)
        dest_dir = os.path.join(script_dir, dest_file)
        with open(src_dir, 'r') as src:
            with open(dest_dir, 'w') as dest:
                dest.write(src.read())
    except Exception as ex:
        print(ex)
        return HttpResponseBadRequest(ex)