from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from netmiko import ConnectHandler, SCPConn

def transfer_config(request):
    try:
        target = {
            'device_type': 'cisco_ios',
            'host': request.POST.get('ip-address'),
            'username': request.POST.get('username'),
            'password': request.POST.get('password'),
        }
        net_conn = ConnectHandler(**target)
        scp_conn = SCPConn(net_conn)
        scp_conn.scp_transfer_file('exampleConfig.txt', 'system:running-config')
        net_conn.disconnect()
        return redirect('test_route')
    except Exception as ex:
        return HttpResponse(ex)

def download_config(request):
    try:
        with open('exampleConfig.txt', 'rb') as f:
            response = HttpResponse(f)
            response['content_type'] = "application/octet-stream"
            response['Content-Disposition'] = 'attachment; filename=' + \
                os.path.basename('exampleConfig.txt')
            return response
    except Exception as ex:
        return HttpResponse(ex)

