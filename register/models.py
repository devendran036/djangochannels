from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from friendrequest.models import FriendList
# Create your models here.


    
        
class profiledata(models.Model):
    user=models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    profile_pic = models.ImageField(default="cover.jpg", null=True, blank=True)

    name=models.CharField(max_length=50,null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    totatfriends=models.IntegerField(default=0)
    totalpost=models.IntegerField(default=0)
  
    online_status=models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    @staticmethod
    def getoffline(user):
        a=FriendList.objects.filter(user=user).values_list('friends')
        r=profiledata.objects.filter(user__in=a,online_status=True)
        print(r)
        '''data={}
        data['user']=r.user'''
        return data

            
            


	
class FilesAdmin(models.Model):
    adminupload=models.FileField(upload_to='media')
    title=models.CharField(max_length=50)
    def __Str__(self):
        return self.title
class messagesave(models.Model):
    hashtag=models.IntegerField()
    messagd=models.TextField(blank=False)
    receiver=models.ForeignKey(User,on_delete=models.CASCADE,null=False,blank=False)
    messagedate= models.DateTimeField(auto_now_add=True, null=True) 
    messagetype=models.CharField(max_length=10,default='text')
   
   
    
    def __str__(self):
        return str(self.hashtag)
class lockedmessage(models.Model):
    message=models.TextField(blank=False)
class inboxorder(models.Model):
    lastdate= models.DateTimeField(auto_now=True, null=True)
    status=models.BooleanField(default=False)
    msgcount=models.IntegerField(default=0)
    hashtag=models.IntegerField()
    messageid=models.IntegerField(default=0)
    def __str__(self):
        return str(self.hashtag)
class messagepost(models.Model):
    image_upload=models.ImageField(upload_to='message_post/')
   


    
# Create your models here.
