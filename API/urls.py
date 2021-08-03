from django.contrib import admin
from django.urls import path,include
from API import views
urlpatterns=[
    path('api/getmessages/<int:requestid>/<int:hashid>/',views.apiOverview),
     path('api/friend/',views.showfriend),
    path('api/request/',views.showrequest),
    path('api/msg/<int:requestid>/<int:hashid>/',views.savmsg),
    path('api/getpost/<int:start>/<int:end>',views.getpost),
    path('api/profileinfo/<int:requestid>/',views.getprofileinfo),
    path('api/likepost/<int:postid>/<int:lord>/',views.like),
    
    path('api/uploadpost/',views.uploadpost),
    path('api/publicpost/',views.pubpost),
    path('api/comment/<int:postid>/',views.comment),
    
    path('api/locker/<int:requestid>/<int:hashid>/',views.locker),
    path('api/chat/',views.chatinbox),
    path('api/getlocker/<int:requestid>/<int:hashid>/',views.getlocker),
    
 

    path('api/imageupload/',views.imageupload)
    
    ]
