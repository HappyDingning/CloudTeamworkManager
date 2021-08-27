from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.forms import ValidationError
from django.forms.models import model_to_dict
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.middleware import csrf
from .forms import RegisterForm, LoginForm, ResetPasswordForm, extend_info, SetPasswordForm, my_clean_phone_number
from .forms import change_info as change_info_form
from .models import UserProfile
from .msgcode import sendcode
from task.models import task
import json
import time


def basic_info(request):
    info = {}

    if request.user.is_authenticated:
        info["is_login"] = True

        notifications = request.user.notifications.unread()
        notifications = notifications.values('id', 'actor_content_type', 'verb', 'description', 'timestamp', 'data')
        notifications = list(notifications)
        for i in notifications:
            i['timestamp'] = int(time.mktime(time.strptime(str(i['timestamp'])[:-7], "%Y-%m-%d %H:%M:%S")))
    
        info["unread_notifications"] = notifications

        notifications = request.user.notifications.read()
        notifications = notifications.values('id', 'actor_content_type', 'verb', 'description', 'timestamp', 'data')
        notifications = list(notifications)
        for i in notifications:
            i['timestamp'] = int(time.mktime(time.strptime(str(i['timestamp'])[:-7], "%Y-%m-%d %H:%M:%S")))

        info["read_notifications"] = notifications

        if request.user.has_perm("task.create_tasks"):
            info["is_creater"] = True
        else:
            info["is_creater"] = False

        user_profile = UserProfile.objects.get(user_id = request.user.id)
        if user_profile.name:
            info["perfected_info"] = True
            info["name"] = user_profile.name
        else:
            info["perfected_info"] = False
            info["name"] = None
    else:
        info["is_login"] = False

    return JsonResponse(info, safe = False)

def logoutAccount(request):
    auth.logout(request)
    return JsonResponse({"tip": "账户已退出", "status": 200}, safe = False)

def login_page(request):
    if request.method == "POST":
        forms = LoginForm(request.POST)

        if forms.is_valid():
            user = auth.authenticate(request, username = forms.cleaned_data['phone_number'], password = forms.cleaned_data['password'])
            if user:
                auth.login(request, user)
                return JsonResponse({"tip": "登录成功", "status": 200}, safe=False)
            return JsonResponse({"tip": "用户名或密码错误", "status": 400}, safe=False)
        return JsonResponse({"tip": "输入内容有误", "status": 400}, safe=False)

    if request.method == "DELETE":
         auth.logout(request)
         return HttpResponseRedirect("/account/login/")

def register_page(request):
    if request.user.is_authenticated:
        return JsonResponse({"tip": "账户已登录", "status": 200}, safe = False)

    if request.method == "POST":
        forms = RegisterForm(request.POST)

        if forms.is_valid():
            user = User.objects.create_user(username = forms.cleaned_data['phone_number'], password=forms.cleaned_data['password'])
            UserProfile.objects.create(user_id = user.id)
            return JsonResponse({"tip": "登录成功", "status": 200}, safe=False)
        return JsonResponse({"tip": list(forms.errors.values())[0][0], "status": 400}, safe=False)

def reset_password_page(request):
    if request.method == "POST":
        forms = ResetPasswordForm(request.POST)

        if forms.is_valid():
            user = User.objects.get(username = forms.cleaned_data["phone_number"])
            user.set_password(forms.cleaned_data["password"])
            user.save()
            return JsonResponse({"tip": "密码重置成功", "status": 200}, safe=False)
        return JsonResponse({"tip": list(forms.errors.values())[0][0], "status": 400}, safe=False)

@login_required
def set_password(request):
    if request.method == "POST":
        forms = SetPasswordForm(request.POST)
        user = request.user  # 不用动这里
        forms.user = request.user  # 不用动这里
        forms.answer = request.session.get('verify').upper()

        if forms.is_valid():
            user.set_password(forms.cleaned_data["new_password"])
            auth.logout(request)
            return JsonResponse({"tip": "密码修改成功", "status": 200}, safe=False)
        return JsonResponse({"tip": list(forms.errors.values())[0][0], "status": 400}, safe=False)

def check_phone_number(request):
    phone_number = request.POST.get("phone_number")

    try:
        my_clean_phone_number(phone_number)
    except ValidationError as e:
        return JsonResponse({"tip": e.message, "status": 400}, safe=False)
    return JsonResponse({"tip": "手机号码可用", "status": 200}, safe=False)

def sendmsgcode(request):
    def check_picode():
        answer = request.session.get('verify').upper()
        code = request.POST.get('picode').upper()

        if code == answer:
            auth.logout(request)
            return True
        return False

    if check_picode():
        sendcode(request.POST.get("phone_number"))
        return JsonResponse({"tip": "操作成功", "status": 200}, safe=False)
    return JsonResponse({"tip": "图形验证码校验失败", "status": 400}, safe=False)

@login_required
def space_page(request):
    target_userprofile = UserProfile.objects.get(user_id = request.user.id)
    target_user = request.user

    return JsonResponse({"info": {"name": target_userprofile.name, "phone_number": target_user.username, "gender": target_userprofile.sex, "student_id": target_userprofile.student_id, "birthday": target_userprofile.birthday, "email": target_userprofile.email, "major": target_userprofile.major, "grade": target_userprofile.grade, "room": target_userprofile.room, "home_address": target_userprofile.home_address, "guardian_phone": target_userprofile.guardian_phone, "introduction": target_userprofile.introduction, "user_id": target_user.id, "sex": target_userprofile.sex, "birthday": target_userprofile.birthday, "edit_status": "false", "edit_or_save": "编辑"}, "status": 200}, safe=False)

def home(request):
    return render(request, 'home.html')

@login_required
def perfect_info(request):
    if request.method == "GET":
        return render(request, "perfect_info.html")

    if request.method == "POST":
        user_info = UserProfile.objects.get(user_id = request.user.id)
        if not user_info.name:
            forms = extend_info(request.POST, instance=user_info)

            if forms.is_valid():
                forms.save()
                return JsonResponse({"tip": "信息录入成功", "status": 200}, safe=False)
            return JsonResponse({"tip": list(forms.errors.values())[0][0], "status": 400}, safe=False)
        return JsonResponse({"tip": "权限不足", "status": 400}, safe=False)

@login_required
def change_info(request):
    if request.method == "POST":
        user_info = UserProfile.objects.get(user_id = request.user.id)
        forms = change_info_form(request.POST, instance=user_info)

        if forms.is_valid():
            forms.save()
            return JsonResponse({"tip": "操作成功", "status": 200}, safe=False)
        return JsonResponse({"tip": list(forms.errors.values())[0][0], "status": 400}, safe=False)

@login_required
def task_list(request):
    user = UserProfile.objects.get(user_id = request.user.id)
    _task_list = json.loads(user.involved_projects)
    temp = [task.objects.filter(id = each).values("id", "task_name", "members", "task_status", "creator", "leaders")[0] for each in _task_list]
    for each_task in temp:
        members = json.loads(each_task["members"])
        each_task["members"] = [UserProfile.objects.get(user_id = each).name for each in members]
        each_task["is_creator"] = (bool)(request.user.id == each_task['creator'])
        each_task["is_leader"] = (bool)(request.user.id in json.loads(each_task['leaders']))
        each_task.pop('creator')
    return JsonResponse({"info": {"content": temp, "name": user.name, "create_task": request.user.has_perm('task.create_tasks')}, "status": 200}, safe=False)

def csrf_token(request):
	token = csrf.get_token(request)
	return JsonResponse({'info': token})
