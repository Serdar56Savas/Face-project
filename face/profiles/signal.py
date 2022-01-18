from django.db.models.signals import post_save,pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile,Bag_kurma


@receiver(post_save,sender=User)        #reciver sinyali alan alıcı
def post_save_create_profile(sender,instance,created,**kwargs):
    print("sender:",sender)
    print("instance",instance)
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save,sender=Bag_kurma)
def post_save_add_to_friends(sender, instance, created, **kwargs):
    sender1=instance.sender
    reciver1=instance.reciver
    if instance.status =="accepted":
        sender1.friends.add(reciver1.user)
        reciver1.friends.add(sender1.user)
        sender1.save()
        reciver1.save()


#Arkadaş ekleme -çıkarma işlemi için
@receiver(pre_delete,sender=Bag_kurma)
def pre_delete_remove_friends(sender,instance,**kwargs):
    sender=instance.sender
    receiver=instance.reciver
    sender.friends.remove(receiver.user)
    receiver.friends.remove(sender.user)
    sender.save()
    receiver.save()






