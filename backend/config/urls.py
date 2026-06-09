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
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from ideas.views import home, create, set_status, CommentListCreateAPIView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Web Pages
    path('', home, name='home'),
    path('create/', create, name='create'),
    path('status/<int:idea_id>/<str:status_type>/', set_status, name='set_status'), # cambiato in status_type per evitare conflitti di nomi

    # Auth
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # API REST (DRF)
    # GET a questo url mostrerà i commenti, POST aggiungerà un commento
    path("ideas/<int:idea_id>/comments/", CommentListCreateAPIView.as_view(), name="idea-comments"),
    # Manteniamo il vecchio path POST per non rompere JS se fa chiamate esplicite a /add/
    path("ideas/<int:idea_id>/comments/add/", CommentListCreateAPIView.as_view(), name="idea-comments-add"),
]