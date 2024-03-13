"""
URL configuration for tour_recomm_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from api.views.UserView import *
from api.views.TouristView import *
from api.views.HistoryView import *
from api.views.RatingView import *
from api.views.RecommanderView import *

urlpatterns = [
    path('admin', admin.site.urls),
    path('api/v1/users', UserDetail.as_view()),
    path('api/v1/users/<int:id>', UserInfo.as_view()),
    path('api/v1/users/profile', UserProfile.as_view()),
    path('api/v1/users/login', UserLogin.as_view()),
    path('api/v1/users/changepw', UserChangePW.as_view()),

    path('api/v1/tourist', TouristDetail.as_view()),
    path('api/v1/tourist/<int:id>', TouristInfo.as_view()),

    path('api/v1/history', HistoryInfo.as_view()),

    path('api/v1/rating', RatingInfo.as_view()),

    path('api/v1/recommend', RecommanderInfo.as_view())
]
