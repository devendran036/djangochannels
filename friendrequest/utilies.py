from friendrequest.models import FriendRequest
def get_friend(sender,receiver):
    try:
        return FriendRequest.objects.get(sender=sender,receiver=receiver,isactive=True)
    except FriendRequest.DoesNotExist:
        return False
