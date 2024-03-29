"""todo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.db import router
from django.urls import path,include
from api.views import ToDoView,ToDoModelView,UsersView
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register("todo",ToDoView,basename="todo")
router.register("api/v1/todo",ToDoModelView,basename="mtodo")
router.register("api/v1/users",UsersView,basename="users")
urlpatterns = [
    path('admin/', admin.site.urls),
    path("web/",include("todoweb.urls"))
]+router.urls
