from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from notifications.signals import notify
from notifications.models import Notification
from dwebsocket.decorators import require_websocket, accept_websocket
from CloudTeamworkManager.total_class import WebSocket_Connections
import json
import time


# 类型定义: 1是系统消息，0是组内消息
@login_required
def delete_all_read(request):
    notifications = request.user.notifications.read()
    notifications.delete()
    return JsonResponse({"tip": "操作成功", "status": 200}, safe=False)

@login_required
def delete_target(request, notification_id):
    notification = Notification.objects.filter(id = notification_id)
    if request.user.id == notification[0].recipient.id:
        notification.delete()
        return JsonResponse({"tip": "操作成功", "status": 200}, safe=False)
    else:
        return JsonResponse({"tip": "权限不足", "status": 400}, safe=False)

@login_required
def get_read(request):
    notifications = request.user.notifications.read()
    notifications = notifications.values('id', 'actor_content_type', 'verb', 'description', 'timestamp', 'data')
    notifications = list(notifications)
    for i in notifications:
        i['timestamp'] = int(time.mktime(time.strptime(str(i['timestamp'])[:-7], "%Y-%m-%d %H:%M:%S")))

    return JsonResponse(notifications, safe=False)

@login_required
def get_unread(request):
    notifications = request.user.notifications.unread()
    notifications = notifications.values('id', 'actor_content_type', 'verb', 'description', 'timestamp', 'data')
    notifications = list(notifications)
    for i in notifications:
        i['timestamp'] = int(time.mktime(time.strptime(str(i['timestamp'])[:-7], "%Y-%m-%d %H:%M:%S")))
    
    return JsonResponse(notifications, safe=False)

@login_required
def mark_all_as_read(request):
    request.user.notifications.unread().mark_all_as_read()
    return JsonResponse({"tip": "操作成功", "status": 200}, safe=False)

@login_required
def mark_target_as_read(request, notification_id):
    notification = Notification.objects.get(id = notification_id)
    if request.user.id == notification.recipient.id:
        notification.mark_as_read()
        return JsonResponse({"tip": "操作成功", "status": 200}, safe=False)
    else:
        return JsonResponse({"tip": "权限不足", "status": 400}, safe=False)

@login_required
def notifications(request):
    read = list(request.user.notifications.read().values('data', 'verb', 'description', 'timestamp','id'))
    for i in read:
        i['timestamp'] = str(i['timestamp'])[:-7]
    unread = list(request.user.notifications.unread().values('data', 'verb', 'description', 'timestamp','id',))
    for i in unread:
        i['timestamp'] = str(i['timestamp'])[:-7]
    return JsonResponse({"info": {"read": read, "unread": unread}, "status": 200}, safe=False)

def send_test(request, type):
    global WebSocket_Connections
    actor = request.user
    noti = notify.send(actor, recipient=actor, verb='你好鸭，这是测试通知', description = "这是的是通知的正文部分", type=type)
    temp = WebSocket_Connections.get(request.user.id, None)
    if temp:
        try:
            temp.send(json.dumps({"id": noti[0][1][0].id, "verb": "你好鸭，这是测试通知", "description": noti[0][1][0].description, "timestamp": (int)(time.time()), "data": json.dumps(noti[0][1][0].data), "status": 200}).encode())
        except:
            pass
    return HttpResponse("OK")

@login_required
def get_target_type(request, type): 
    unread = request.user.notifications.unread()
    read = request.user.notifications.read()

    unread = unread.filter(data={"type": type})
    read = read.filter(data={"type": type})

    unread = list(unread.values('id', 'data', 'verb', 'description', 'timestamp'))
    read = list(read.values('id', 'data', 'verb', 'description', 'timestamp'))

    for i in read:
        i['timestamp'] = str(i['timestamp'])[:-7]

    for i in unread:
        i['timestamp'] = str(i['timestamp'])[:-7]

    return JsonResponse({"content": {"unread": unread, "read": read}, "status": 200}, safe=False)

@require_websocket
def messaging(request):
    global WebSocket_Connections
    WebSocket_Connections[request.user.id] = request.websocket

    while 1:
        try:
            message = request.websocket.wait()
        except:
            WebSocket_Connections.pop(request.user.id)
            print("client_offline")
            break

        if message:
            if json.loads(message)["status"] == 201:
                request.websocket.send(json.dumps({"tip": "server_online", "status": 201}).encode())
