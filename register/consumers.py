import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import async_to_sync
from channels.auth import login
from channels.layers import get_channel_layer
from register.models import messagesave,profiledata,inboxorder
from friendrequest.models import FriendList
import asyncio
from django.db.models import F
from django.contrib.auth.models import User
class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_name=self.scope['url_route']['kwargs']['id']
        self.room_group_name='user_%s' % self.room_name
       
        
    
        
        await self.channel_layer.group_add(self.room_group_name,self.channel_name)
        await makeonline(self.scope['user'])

        await self.accept()
       
       

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.scope['user'].username, self.channel_name)
        r= await makeoffline(self.scope['user'])
        e=json.loads(r)
        for d in e:
            await self.channel_layer.group_send('user_'+str(d),{'type':'off','user':self.scope['user'].id})
        
             
     

    async def receive(self, text_data):
        a=json.loads(text_data)
    
        if a['type']=='userms':
            a['id']=await savemessage(a['hashtag'],self.scope['user'],a['msg'],a['mty'],a['seen'])
            await self.send_json(a)
        elif a['type']=='sel':
            r={'type':'re','user':a['user']}
            
            await self.send_json(r)
        
    
        await self.channel_layer.group_send(a['username'],a)
        
        
      
        
            
        
            
              
    async def sel(self,data):
        if data['seen']:
            await makeseen(data['hashtag'])
        await self.send_json(data)
    async def off(self,data):
      
        await self.send_json(data)
    async def unsel(self,data):
      
        await self.send_json(data)
    async def userms(self,data):
        
        
      
        await self.send_json(data)
    async def videocall(self,data):
        await self.send_json(data)

    async def show_ac(self,data):
      
        await self.send_json(data)
    async def seton(self,data):
        await self.send_json(data)
    async def videocall(self,data):
        await self.send_json(data)
    


@database_sync_to_async 
def savemessage(hashid,rec,msg,mty,seen):
    r=messagesave.objects.create(hashtag=hashid,receiver=rec,messagd=msg,messagetype=mty)
    r.save()
    if seen:
        t=inboxorder.objects.get(hashtag=hashid)
        t.status=False
        t.messageid=r.id
        t.msgcount+=1
        t.save()
    
    else:
        t=inboxorder.objects.get(hashtag=hashid)
        t.messageid=r.id
        t.save()
    

    return r.id
@database_sync_to_async 
def makeseen(hashtag):
    inboxorder.objects.filter(hashtag=hashtag).update(status=True,msgcount=0)

@database_sync_to_async 
def makeonline(ouser):
   




    profiledata.objects.filter(user=ouser).update(online_status=True)
@database_sync_to_async 
def makeoffline(ouser):
    
    profiledata.objects.filter(user=ouser).update(online_status=False)
    w=FriendList.objects.filter(user=ouser).values_list('friends')
    r=profiledata.objects.filter(user__in=w,online_status=True)
    e=[]
    if r:
        for notification in r.all():
            e.append(notification.user.id)
        
    return json.dumps(e)
    