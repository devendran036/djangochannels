from django.urls import path,include
from django.conf.urls import url
from friendrequest import views
urlpatterns = [path('addfriend',views.send),path('myfriend',views.myfriend),path('showrequest',views.showing),path('test',views.display)]
