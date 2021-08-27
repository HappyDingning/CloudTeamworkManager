# coding:utf-8
import xadmin
from xadmin import views
from .models import *
from xadmin.plugins.auth import UserAdmin
from django.contrib.auth.models import User

class BaseSettings(object):
    enable_themes = True
    use_bootswatch = True

class GlobalSettings(object):
    site_title = 'CloudTeamworkManager'
    site_footer = '振翅云顶之上，极目星辰大海'
    menu_style = 'accordion'


class UserProfileAdmin(UserAdmin):
    # search_fields = ['学号','姓名','年级','方向','邮箱','username','家庭住址','监护人电话']
    list_display = ['学号','姓名','年级','方向','邮箱','username','家庭住址','监护人电话']
    # list_filter = ['学号','姓名','年级','方向','邮箱','username','家庭住址','监护人电话']


class UserInfoAdmin(object):
    
    list_display = ['name','student_id','major','sex','grade','email','room','home_address','guardian_phone']
    list_filter = ['name','student_id','major','sex','grade','email','room']
    search_fields = ['name','student_id','major','sex','grade','email','room']

xadmin.site.register(User,UserProfileAdmin)
xadmin.site.register(UserProfile,UserInfoAdmin)
xadmin.site.register(views.BaseAdminView,BaseSettings)
xadmin.site.register(views.CommAdminView,GlobalSettings)
