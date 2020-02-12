from django.urls import path
from .views import *


urlpatterns = [
    path('employee/register', EmployeeRegisterView.as_view(), name='employee_register_url'),
    path('employer/register', EmployerRegisterView.as_view(), name='employer_register_url'),
    path('profile/', ProfileDetailView.as_view(), name='profile_detail_url'),
    path('profile/update', ProfileUpdateView.as_view(), name='profile_update_url'),
    path('profile/jobs', ProfileJobsPanelView.as_view(), name='profile_jobs_panel_url'),
    path('profile/jobs/data-download', ProfileDataDownload.as_view(), name='profile_data_download_url'),
    path('profile/applicants', ProfileApplicantsDetailView.as_view(), name='profile_applicants_detail_url'),
    path('admin/dashboard', AdminDashboardView.as_view(), name='admin_dashboard_url'),
    path('admin/dashboard/data-download', AdminDataDownload.as_view(), name='admin_data_download_url'),
    path('logout', UserLogoutView.as_view(), name='logout_url'),
    path('login', UserLoginView.as_view(), name='login_url'),
]

