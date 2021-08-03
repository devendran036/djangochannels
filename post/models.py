from django.db import models
from django.contrib.auth.models import User
class userpost(models.Model):
    user=models.ForeignKey(User,null=True, blank=True, on_delete=models.CASCADE,related_name='userposted')
    post=models.FileField(upload_to='user_post/',null=True, blank=True)
    likes=models.ManyToManyField(User,blank=True)
    post_type=models.BooleanField(default=False)
    
    likecount=models.IntegerField(default=0)
    def __str__(self):
        return self.user.username
    def natural_key(self):
        return self.user.username
class Comments(models.Model):
    post=models.ForeignKey(userpost,on_delete=models.CASCADE,related_name='comments')
    comment=models.TextField()
    user=models.ForeignKey(User,null=True, blank=True, on_delete=models.CASCADE,related_name='usercommented')
    def __str__(self):
        return self.user.username


    
    


    
# Create your models here.
 
