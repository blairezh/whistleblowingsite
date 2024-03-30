from django.urls import path
from . import views
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView



app_name = "login"
urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html")),
    path('logout/', LogoutView.as_view()),
    path('userlanding/', views.user_landing_view),
    path('adminlanding/',views.admin_landing_view),
    path('report/', views.report),
    path('viewreports/', views.user_reports),
    path('viewreports/', views.admin_report_view),
    path('adminreportview/', views.admin_report_view),
]
