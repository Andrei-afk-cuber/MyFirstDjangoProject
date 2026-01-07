"""
URL configuration for DjangoProject project.

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

from vacancies import views as vacancies_views
from users import views as users_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('vacancies/', vacancies_views.VacancyView.as_view()),
    path('vacancies/<int:pk>', vacancies_views.VacancyDetailView.as_view()),
    path('users/', users_views.UserView.as_view()),
    path('users/<int:pk>', users_views.UserDetailView.as_view()),
]
