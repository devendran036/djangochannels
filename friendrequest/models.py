from django.db import models

# Create your models here.
from django.db import models

from django.conf import settings
from django.utils import timezone
# Create your models here.
from django.contrib.auth.models import User
class FriendList(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user")
   
    friends=models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name="friends")
     
 
    
    
    def __str__(self):
        return self.user.username
    def addfriend(self,account):
        if not account in self.friends.all():
            self.friends.add(account)
            
            
            self.save()
            
            
            
        
            
    def remove_friend(self,account):
        if account in self.friends.all():
            self.friends.remove(account)
    def  unfriend(self,removee):
        remove=self
        remove.remove_friend(removee)
        friendlist=FriendList.objects.get(user=removee)
        frinedslist.remove_friend(self.user)
    def is_mutual(self,friend):
        if freind in self.friends.all():
            return True
        else:
            return False
   
class FriendRequest(models.Model):
    sender=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="sender")
    receiver=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="receiver")
    isactive=models.BooleanField(blank=True,null=False,default=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.sender.username
    
    
        
        
