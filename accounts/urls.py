from django.urls import path
from .views import *


urlpatterns = [
    path('employee/register', EmployeeRegisterView.as_view(), name='employee_register_url'),
    path('employer/register', EmployerRegisterView.as_view(), name='employer_register_url'),
    path('profile/<int:id>', ProfileDetailView.as_view(), name='profile_detail_url'),
    # path('profile/<int:id>/edit', EmployerUpdateView.as_view(), name='employer_profile_edit_url'),
    path('profile/jobs', ProfileJobsPanelView.as_view(), name='profile_jobs_panel_url'),
    path('logout', UserLogoutView.as_view(), name='logout_url'),
    path('login', UserLoginView.as_view(), name='login_url'),
]

