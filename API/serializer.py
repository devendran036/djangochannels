from rest_framework import serializers
from register.models import  *
from friendrequest.models import *
from django.db.models import Q

from post.models import *
class showmessage(serializers.ModelSerializer):
    class Meta:
        model=messagesave
        fields='__all__'
class imgupload(serializers.ModelSerializer):
    class Meta:
        model=messagepost
        fields=['image_upload']
class showfriends(serializers.ModelSerializer):
    friends=serializers.CharField(source='user.username')
 
    class Meta:
        model=FriendList
        fields=['user','friends']
class requests(serializers.ModelSerializer):
    sender=serializers.CharField(source='sender.username') 
    receiver=serializers.CharField(source='receiver.username')
    class Meta:
        
        model=FriendRequest
        fields=['sender','receiver']
class profileinfo(serializers.ModelSerializer):
    class Meta:
        
        model=profiledata
        fields='__all__'
class displaypost(serializers.ModelSerializer):
    user=serializers.CharField(source='user.username',read_only=True)
    
   
    class Meta:
        model=userpost
        fields='__all__'
class publicpost(serializers.ModelSerializer):
    user=serializers.CharField(source='user.username')
    likes=serializers.SerializerMethodField('get_likes')
    comments=serializers.SerializerMethodField('get_comments')
   
    def get_likes(self,obj):
        qs = FriendList.objects.filter(user=self.context.get("user_id")).values_list('friends',flat=True)
        r=userpost.objects.filter(pk__in=self.context.get("postid"),likes__in=qs).values_list('likes',flat=True)
        return r
    def get_comments(self,obj):
          qs = FriendList.objects.filter(user=self.context.get("user_id")).values_list('friends',flat=True)
          t=Comments.objects.filter(post=obj,user__in=qs).values_list('comment',flat=True)
          return t

    class Meta:
        model=userpost
        fields=['id','user','post','likecount','likes','comments']
class getcoments(serializers.ModelSerializer):
    user=serializers.CharField(source='user.username')
    class Meta:
        model=Comments
        fields=['id','user','comment','post']
class messagelocked(serializers.ModelSerializer):
    

    class Meta:
        model=lockedmessage
        fields='__all__'
class chatbox(serializers.ModelSerializer):
    class Meta:
        model=inboxorder
        fields=['status','hashtag','msgcount']
  

        
        

     



    


    

