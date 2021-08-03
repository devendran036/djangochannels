from django.http import HttpResponse
from django.shortcuts import render
from friendrequest.models import FriendList,FriendRequest
from friendrequest.utilies import get_friend
from register.models import inboxorder
from django.db.models import Q
# Create your views here.
from django.contrib.auth.models import User
def send(request):
     print()
     if request.method=='POST':
          name=request.POST.get('username')
          name=User.objects.get(pk=name)
          d=FriendRequest(sender=request.user,receiver=name)
          d.save()
          return HttpResponse('ok done')
     else:
          friendlist=FriendList.objects.filter(user=request.user,friends__isnull=False).values_list('friends')
          friendrequest=FriendRequest.objects.filter(Q(sender=request.user)|Q(receiver=request.user))
          
          account=User.objects.exclude(id__in=friendlist)
         
         
          
          
     return render(request,'friendrequest.html',context={'show':account})
       
def showing(request):
     if request.method=="POST":
          namee=request.POST.get('username')
          username=FriendRequest.objects.get(sender=namee,receiver=request.user)
          
          FriendList.objects.get(user=request.user.id).friends.add(namee)
          FriendList.objects.get(user=namee).friends.add(request.user.id)
        

          
          inboxorder.objects.create(hashtag=request.user.id+int(namee))
          username.delete()

          
          return HttpResponse('done')
     else:
          req=FriendRequest.objects.filter(receiver=request.user)
         
          
          context={'req':req}
          return render(request,'showingfriendreq.html',context)
     
def myfriend(request):
     friend_list=FriendList.objects.filter(friends=request.user)
     return HttpResponse(friend_list)
     
        
    
        
def display(request):
     return render(request,'newt.html')
     
    
   


# Create your views here.
