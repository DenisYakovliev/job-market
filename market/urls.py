from django.urls import path

from .views import *


urlpatterns = [
    path('', home_page, name='home_page_url'),
    path('jobs/', jobs_list, name='jobs_list_url'),
    path('jobs/create/', JobCreate.as_view(), name='job_create_url'),
    path('jobs/<int:job_id>', JobDetail.as_view(), name='job_detail_url'),
    path('jobs/<int:job_id>/update', JobUpdate.as_view(), name='job_update_url'),
    path('jobs/<int:job_id>/delete', JobDelete.as_view(), name='job_delete_url'),
    path('jobs/<int:job_id>/cancel', JobCancel.as_view(), name='job_cancel_url'),
]
