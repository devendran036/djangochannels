from django.shortcuts import render
from post.models import *
from post.form import *
def post(request):
    return render(request,'post.html')
def uploadpost(request):
    if request.method=='POST':
        if request.POST.get('public'):
            r=userpost.objects.create(user=request.user,post_type=True,post=request.FILES['file'])
            r.save()
        else:
            r=userpost.objects.create(user=request.user,post=request.FILES['file'])
            r.save()

    return render(request,'upload.html')


# Create your views here.
