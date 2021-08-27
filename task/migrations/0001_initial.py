# Generated by Django 2.2 on 2019-10-13 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.CharField(max_length=20, verbose_name='任务名')),
                ('publish_date', models.DateField(auto_now_add=True, verbose_name='发布时间')),
                ('deadline', models.DateField(verbose_name='结束时间')),
                ('task_status', models.IntegerField(choices=[(0, '已挂起'), (-1, '已结束'), (1, '进行中')], verbose_name='任务状态')),
                ('members', models.CharField(default='[]', max_length=200, verbose_name='成员')),
                ('all_members', models.CharField(default='[]', max_length=200, verbose_name='参加过项目的成员')),
                ('creator', models.IntegerField(verbose_name='创建者')),
                ('leaders', models.CharField(default='[]', max_length=20, verbose_name='组长')),
                ('task_description', models.CharField(default='', max_length=200, verbose_name='任务描述')),
                ('task_need', models.CharField(default='', max_length=1000, verbose_name='任务需求')),
                ('task_schedule', models.TextField(default='[]', verbose_name='时间安排')),
                ('task_progress', models.TextField(default='[]', verbose_name='任务进度')),
                ('task_comment', models.TextField(default='[]', verbose_name='任务评价')),
                ('appendixes', models.CharField(default='[]', max_length=200, verbose_name='附件')),
            ],
            options={
                'verbose_name': '任务详情',
                'verbose_name_plural': '任务详情',
                'permissions': {('edit_personal_comments', '编辑个人评价'), ('edit_task_progress', '编辑任务进度'), ('edit_task_comments', '编辑任务评价'), ('edit_task_schedule', '编辑任务时间表'), ('delete_appendix', '删除附件'), ('view_personal_schedule', '查看个人时间表'), ('view_personal_comments', '查看个人评价'), ('download_personal_appendix', '下载私人附件'), ('view_personal_progress', '查看个人进度'), ('create_tasks', '新建任务'), ('edit_appendix', '编辑附件'), ('edit_task', '编辑任务'), ('glance_over_task_details', '浏览任务详情')},
            },
        ),
    ]