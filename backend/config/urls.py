"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from ideas import views
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from ideas.views import home, create, set_status

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home, name='home'),
    path('create/', create, name='create'),

    # ADMIN ACTION
    path('status/<int:idea_id>/<str:status>/', set_status, name='set_status'),

    # auth
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # commenti
    path("ideas/<int:idea_id>/comments/", views.get_comments),
    path("ideas/<int:idea_id>/comments/add/", views.add_comment),
]