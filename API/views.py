from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status,generics
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from API.serializer import *
from register.models import  messagesave,profiledata,messagepost
from django.core import serializers
from post.models import userpost
from friendrequest import *
from django.db.models import Q
from django.db.models import F
from django.contrib.auth.models import User
import json
from django.shortcuts import get_object_or_404
from django.db.models import Max,Count
from django.utils.timezone import now
from itertools import chain
from django.contrib.auth import authenticate

from rest_framework.renderers import JSONRenderer

@api_view(['GET'])
def apiOverview(request,requestid,hashid):
    if request.user.id==hashid-requestid:
        t=inboxorder.objects.get(hashtag=hashid)
        if request.method=='GET':
            messages=messagesave.objects.filter(hashtag=hashid).order_by('-id')[0:6]
            ser=showmessage(messages,many=True)
            return Response(ser.data)
    return HttpResponse("Alert unknow user acess!")
@api_view(['POST'])
def savmsg(request,requestid,hashid):
    if request.user.id==hashid-requestid:
        r=inboxorder.objects.get(hashtag=hashid)
        r.status=False
        r.msgcount+=1
       
        if(request.data['second']):
            r.lastactive=now()
       
        request.data['receiver']=requestid
        request.data['hashtag']=hashid
        ser=showmessage(data=request.data)
        if ser.is_valid():
           
            mid=ser.save()
            r.messageid=mid.id
        return Response(ser.data['id'])
    return Response({"Error":"You have no acces to insert messages"})
@api_view(['GET'])
def showfriend(request):
    r=FriendList.objects.filter(friends=request.user)
    ser=showfriends(r,many=True)
    return Response(ser.data)
@api_view(['GET'])
def getprofileinfo(request,requestid):
     re=profiledata.objects.filter(user=requestid)
     t=profileinfo(re,many=True)
     return Response(t.data)
@api_view(['GET'])
def showrequest(request):
    r=FriendRequest.objects.filter(receiver=request.user)
    ser=requests(r,many=True)
    return Response(ser.data)
@api_view(['GET'])
def getpost(request,start,end):
    t=FriendList.objects.filter(user=request.user.id).values_list('friends',flat=True)
    post=userpost.objects.filter(user__in=t).order_by('-id')
    likes=post.filter(likes__in=t).values_list('pk','likes__username')[0:5]
   
    post=post[0:5]
    r=post.values_list('id')
    y=Comments.objects.filter(post__in=r,user__in=t)
   
    if not y:
        comm=getcoments(y,many=True)
    else:
        y=Comments.objects.filter(post__in=r)
        comm=getcoments(y,many=True)
    ser=displaypost(post,many=True)
    
   
    return Response({'data':ser.data,'LCM':likes,'Comments':comm.data})



@api_view(['GET'])
def pubpost(request):
    post=userpost.objects.filter(~Q(user=request.user),post_type=True).order_by('-pk')[0:5]
    r=post.values_list('pk',flat=True)
    ser=publicpost(post,context={'user_id': request.user.id,'postid':r},many=True)
     
    
    
    return Response(ser.data)

    
@api_view(['POST'])
def like(request,postid,lord):
    t=userpost.objects.get(pk=postid)
    if lord==0:
        t.likes.add(request.user)
        t.likecount=t.likes.count()
        t.save()
       
    elif lord==1:
        t.likes.remove(request.user)
        t.likecount-=1
        t.save()
        
    return Response("ok")
@api_view(['POST'])
def uploadpost(request):
    userpost.objects.create(post=request.data['post'],user=request.user,post_type=True)
    

    
     
     
    return Response({"Ok":"Sucess"})
@api_view(['POST'])
def comment(request,postid):
   
   
    r=Comments.objects.create(post_id=postid,comment=request.data,user=request.user)
    r.save()
    return Response({"ok":"sucess"})
@api_view(['POST'])
def locker(request,hashid,requestid):
    if request.method=="POST":
        if request.user.id==hashid-requestid:
                t=messagelocked(data=request.data)
                if t.is_valid():
                    r=t.save()
                    return Response({
                    "ok":r.id
                    })
    return Response({'Error':'a'})
@api_view(['POST'])
def getlocker(request,hashid,requestid):

    
   
    if request.user.id==hashid-requestid:
            
           
            user=authenticate(request,username=request.user.username,password=request.data['pass'])
            
            
            if user is not None:
                print('done')
                r=lockedmessage.objects.filter(pk=request.data['id'])
                t=messagelocked(r,many=True)
                return Response(t.data)
   
    return Response({"Error":"Invalid acess"})
@api_view(['GET'])
def chatinbox(request):
    r=FriendList.objects.filter(friends=request.user)
    re=r.annotate(hashtag=F('user')+request.user.id)
    t=inboxorder.objects.filter(hashtag__in=re.values_list('hashtag',flat=True)).order_by('-lastdate')[0:5]
    
    msg=messagesave.objects.filter(pk__in=t.values_list('messageid')).order_by('-id')
    tr=re.filter(hashtag__in=t.values_list('hashtag'))
    order=chatbox(t,many=True)
    ser=showfriends(tr,many=True)
    r=showmessage(msg,many=True)
    rer=profiledata.objects.filter(user__in=tr.values_list('user',flat=True))
    profile=profileinfo(rer,many=True)
 
  
    return Response({"Friends":ser.data,"order":order.data,'profile':profile.data,"message":r.data})

@api_view(['POST'])
def imageupload(request):
    r=imgupload(data=request.data)
    if r.is_valid():
        r.save()
    return  Response(r.data)
    



    
    
            
    
            
    


