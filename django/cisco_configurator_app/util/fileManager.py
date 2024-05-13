from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from netmiko import ConnectHandler, SCPConn
from django.http import FileResponse, HttpResponseBadRequest
from .configManager import ConfigManager
import os

local_config_file = './util/running-config'
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
            scp_conn.scp_put_file(local_config_file, remote_config_file)
        elif direction == 'get':
            scp_conn.scp_get_file(remote_config_file, local_config_file)
        else: raise ValueError('Invalid direction.')
        net_conn.disconnect()
    except Exception as ex:
        print(ex)
        return HttpResponseBadRequest(ex)

def download_config():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    local_config_file = os.path.join(script_dir, 'running-config')
    try:
        return FileResponse(open(local_config_file, 'rb'), as_attachment=True, filename='config.txt')
    except Exception as ex:
        print(ex)
        return HttpResponseBadRequest(ex)

def emptyConfigFile(file, cm: ConfigManager):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    file = os.path.join(script_dir, file)
    try:
        with open(file, 'w') as f: 
            f.write('')
        cm.configEditor.readFile()
    except Exception as ex:
        print(ex)
        return HttpResponseBadRequest(ex)

def copyConfigFile(src_file, dest_file, cm: ConfigManager):
    try:
        script_dir = os.path.dirname(os.path.realpath(__file__))
        src_dir = os.path.join(script_dir, src_file)
        dest_dir = os.path.join(script_dir, dest_file)
        with open(src_dir, 'r') as src:
            with open(dest_dir, 'w') as dest:
                dest.write(src.read())

        cm.configEditor.readFile()
    except Exception as ex:
        print(ex)
        return HttpResponseBadRequest(ex)
