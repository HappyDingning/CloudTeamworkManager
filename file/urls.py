from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^picode/.*$', views.picode_code),
    path('image/<str:file_name>/', views.show_image),
    path('avatar/<int:randint>/', views.avatar),
    path('appendix/<int:task_id>/<str:file_name>/', views.appendix),
    path('rename_appendix/<int:task_id>/<int:appendix_id>/', views.rename),
    path('delete_appendix/<int:task_id>/<int:appendix_id>/', views.delete),
    path('overlay_appendix/<int:task_id>/<int:appendix_id>/', views.overlay),
    path('appendix_list/<int:task_id>/', views.table),
    path('personal_appendix/<int:task_id>/<str:file_name>/', views.personal_appendix),
    path('delete_personal_appendix/<int:task_id>/<int:file_index>/', views.delete_personal_appendix),
    path('personal_appendix_list/<int:task_id>/<int:user_id>/', views.personal_appendix_list),
]
