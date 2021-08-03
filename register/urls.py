from django.urls import path,include
from django.conf.urls import url
from . import views
urlpatterns=[path('<str:profile>/post/',views.viewpost),
path('<str:profile>/post/<int:postid>/',views.viewpost),
    path('signup',views.create),
    path('',views.newsfeed,name='home'),
    
    path('login/',views.signin,name='login'),
    path('chat/',views.apicheck),
    path('logout/',views.logoutuser),
 
    ]
