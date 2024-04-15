from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from netmiko import ConnectHandler, SCPConn
from django.http import FileResponse, HttpResponseBadRequest
import os

config_file = './django/cisco_configurator_app/util/exampleConfig'

def transfer_config(ip, user, pw):
    try:
        target = {
            'device_type': 'cisco_ios',
            'host': ip,
            'username': user,
            'password': pw,
        }
        net_conn = ConnectHandler(**target)
        scp_conn = SCPConn(net_conn)
        scp_conn.scp_transfer_file(config_file, 'system:running-config')
        net_conn.disconnect()
    except Exception as ex:
        print(ex)
        return HttpResponseBadRequest(ex)

def download_config():
    try:
        return FileResponse(open(config_file, 'rb'), as_attachment=True, filename='config.txt')
    except Exception as ex:
        print(ex)
        return HttpResponseBadRequest(ex)