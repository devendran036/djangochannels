from django.urls import path,include
from post import views
urlpatterns = [path('post/', views.post),path('upload',views.uploadpost)]
