from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('', views.dashboard, name='admin_dashboard'),

    # Projects
    path('projects/', views.projects_list, name='admin_projects_list'),
    path('projects/add/', views.ProjectCreateView.as_view(), name='admin_project_add'),
    path('projects/<int:pk>/edit/', views.ProjectUpdateView.as_view(), name='admin_project_edit'),
    path('projects/<int:pk>/delete/', views.ProjectDeleteView.as_view(), name='admin_project_delete'),

    # Blogs
    path('blogs/', views.blogs_list, name='admin_blogs_list'),
    path('blogs/add/', views.BlogCreateView.as_view(), name='admin_blog_add'),
    path('blogs/<int:pk>/edit/', views.BlogUpdateView.as_view(), name='admin_blog_edit'),
    path('blogs/<int:pk>/delete/', views.BlogDeleteView.as_view(), name='admin_blog_delete'),

    # Services
    path('services/', views.services_list, name='admin_services_list'),
    path('services/add/', views.ServiceCreateView.as_view(), name='admin_service_add'),
    path('services/<int:pk>/edit/', views.ServiceUpdateView.as_view(), name='admin_service_edit'),
    path('services/<int:pk>/delete/', views.ServiceDeleteView.as_view(), name='admin_service_delete'),

    # Jobs
    path('jobs/', views.jobs_list, name='admin_jobs_list'),
    path('jobs/add/', views.JobCreateView.as_view(), name='admin_job_add'),
    path('jobs/<int:pk>/edit/', views.JobUpdateView.as_view(), name='admin_job_edit'),
    path('jobs/<int:pk>/delete/', views.JobDeleteView.as_view(), name='admin_job_delete'),

    # Messages
    path('messages/', views.messages_list, name='admin_messages_list'),
    path('messages/<int:pk>/', views.message_detail, name='admin_message_detail'),
    path('messages/<int:pk>/delete/', views.message_delete, name='admin_message_delete'),

    # Clients
    path('clients/', views.clients_list, name='admin_clients_list'),
    path('clients/add/', views.ClientCreateView.as_view(), name='admin_client_add'),
    path('clients/<int:pk>/', views.client_detail, name='admin_client_detail'),
    path('clients/<int:pk>/edit/', views.ClientUpdateView.as_view(), name='admin_client_edit'),
    path('clients/<int:pk>/delete/', views.ClientDeleteView.as_view(), name='admin_client_delete'),

    # Client Projects
    path('client-projects/', views.client_projects_list, name='admin_client_projects_list'),
    path('client-projects/add/', views.ClientProjectCreateView.as_view(), name='admin_client_project_add'),
    path('client-projects/<int:pk>/', views.client_project_detail, name='admin_client_project_detail'),
    path('client-projects/<int:pk>/edit/', views.ClientProjectUpdateView.as_view(), name='admin_client_project_edit'),
    path('client-projects/<int:pk>/delete/', views.ClientProjectDeleteView.as_view(), name='admin_client_project_delete'),

    # Analytics
    path('analytics/', views.analytics_page, name='admin_analytics'),
    path('analytics/data/', views.analytics_data, name='admin_analytics_data'),
]