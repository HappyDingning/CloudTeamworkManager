# coding:utf-8
import xadmin
from .models import *
from xadmin import views
'''
task_name = models.CharField(max_length=20, verbose_name="任务名")
publish_date = models.DateField(auto_now_add=True)
deadline = models.DateField(verbose_name='结束时间')
task_status = models.IntegerField(verbose_name='任务状态', choices=((0, '已挂起'), (-1, '已结束'), (1, '进行中')))
members = models.CharField(max_length=200, verbose_name='成员', default="[]")
all_members = models.CharField(max_length=200, verbose_name='参加过项目的成员', default="[]")
creator = models.IntegerField(verbose_name='创建者')
leaders = models.CharField(max_length=20, verbose_name='组长', default="[]")
task_description = models.CharField(max_length=200, verbose_name='任务描述', default="")
task_need = models.CharField(max_length=1000, verbose_name='任务需求', default="")
task_schedule = models.TextField(verbose_name='时间安排', default='[]')
task_progress = models.TextField(verbose_name='任务进度', default="[]")
task_comment = models.TextField(verbose_name='任务评价', default="[]")
appendixes = models.CharField(max_length=200, verbose_name='附件', default="[]")
'''
class taskAdmin(object):
    list_display=['task_name','publish_date','task_status','deadline','leaders','members','task_description','task_progress','task_comment','appendixes']
    search_fields = ['task_name','task_status','leaders','members','task_progress']
    list_filter = ['publish_date','deadline','task_status','leaders','creator','members']

class BaseSettings(object):
    enable_themes = True
    use_bootswatch = True

class GlobalSettings(object):
    site_title = 'CloudTeamworkManager'
    site_footer = u'振翅云顶之上，极目星辰大海'
    menu_style = 'accordion'

xadmin.site.register(task,taskAdmin)
