from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from post.models import *
class userupload(ModelForm):
    class Meta:
        model=userpost
        fields=['user','post','post_type']
        
