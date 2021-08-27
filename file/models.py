from django.db import models

class appendix(models.Model):
    name = models.CharField(max_length = 255, verbose_name = '文件名')
    upload_date = models.DateField(auto_now_add = True, verbose_name = '上传日期')
    task_id = models.IntegerField()
    publisher = models.IntegerField()
    size = models.IntegerField()

    class Meta:
        permissions = {
            ('edit_appendix', '编辑附件'),
            #('delete_appendix', '删除附件'),
        }

class personal_appendix(models.Model):
    detail = models.TextField(verbose_name = '私人附件详情', default = "[]")
    id = models.CharField(max_length = 15, primary_key = True)

    class Meta:
        permissions = {
            ('edit_personal_appendix', '编辑私人附件'),
            ('download_personal_appendix', '下载私人附件'),
            ('upload_personal_appendix', '下载私人附件'),
            # ('delete_personal_appendix', '删除私人附件'),
        }
        verbose_name = u'私人附件'
        verbose_name_plural = verbose_name
