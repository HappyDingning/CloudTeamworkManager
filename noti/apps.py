from django.apps import AppConfig


class NotiConfig(AppConfig):
    name = 'noti'
    verbose_name = '站内消息'

    # def ready(self):
    #     super(NotiConfig, self).ready()
    #     from . import signals
