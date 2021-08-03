from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from register.forms import CreateUserForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from register.models import *
from post.models import *
from friendrequest.models import FriendList,FriendRequest
from django.http import HttpResponse
from django.db.models import Q
def create(request):
    if request.user.is_authenticated:
        return redirect('home')
    form=UserCreationForm()
    if request.method=='POST':
        form=UserCreationForm(request.POST)
      
        if form.is_valid():
            user=form.save()
            name=form.cleaned_data['username']
            passs=form.cleaned_data['password1']
           
            user=authenticate(request,username=name,password=passs)
            login(request,user)
            FriendList.objects.create(user=request.user)
            
            profiledata.objects.create(user=request.user,name=name)
            
            
          
          
  
     
    context={'form':form}
    
    return render(request, 'signup.html',context)

def logoutuser(request):
    logout(request)
    return redirect('login')

def signin(request):
     if request.user.is_authenticated:
        return redirect('home')
     if request.method=='POST':
         name=request.POST.get('name')
         passs=request.POST.get('pass')
         user=authenticate(request,username=name,password=passs)
         if user is not None:
             login(request,user)
             
             
             return redirect('home')
    
     return render(request,'signin.html')

    



@login_required(login_url='/login')
def newsfeed(request):
    return render(request,'newsfeed.html')

@login_required(login_url='/login')
def apicheck(request):
    return render(request,'newlook.html')

def viewpost(request,profile,postid=None):
    t=FriendList.objects.filter(user=request.user).values_list('friends',flat=True)
    r=profiledata.objects.get(user__username=profile)
    if FriendList.objects.filter(user__username=profile,friends=request.user.id).exists():
        if postid:
            post=userpost.objects.filter(id=postid)
            likes=post.filter(likes__in=t).values_list('id','likes__username')[0:5]
            post=post.values_list('user__username','id','likecount','post')
            
        

        else:
            post=userpost.objects.filter(user__username=profile).order_by('-id')
            likes=post.filter(likes__in=t).values_list('id','likes__username')[0:5]
            post=post[0:5]
            post=post.values_list('user__username','id','likecount','post')
        return render(request,'sharepage.html',context={'post':post,'likes':likes,'profile':r,'e':True})
    else:
        if postid:
            post=userpost.objects.filter(id=postid,post_type=True)
            if post:
                likes=post.filter(likes__in=t).values_list('id','likes__username')[0:5]
                post=post.values_list('user__username','id','likecount','post')
            else:
                return render(request,'sharepage.html',context={'private':'yes'})
                
            
        

        else:
            post=userpost.objects.filter(user__username=profile,post_type=True).order_by('-id')
            likes=post.filter(likes__in=t).values_list('id','likes__username')[0:5]
            post=post[0:5]
            post=post.values_list('user__username','id','likecount','post')
        context={'post':post,'likes':likes,'profile':r}
        if FriendRequest.objects.filter(sender__username=profile,receiver=request.user).exists():
                context['c']=True
        elif FriendRequest.objects.filter(sender=request.user,receiver__username=profile).exists():
                context['r']=True
    
        return render(request,'sharepage.html',context)
       
            
            
        
    return render(request,'sharepage.html',context={'private':'yes'})
       
    
        
