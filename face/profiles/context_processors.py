from .models import Profile,Bag_kurma

def Profile_pic(request):
    if request.user.is_authenticated:
        profile_obj=Profile.objects.get(user=request.user)
        pic=profile_obj.avatar
        return {"picture":pic}
    return {}

def invatations_received_no(request):
    if request.user.is_authenticated:
        profile_obj=Profile.objects.get(user=request.user)
        qs_count=Bag_kurma.objects.invatations_recived(profile_obj).count()
        return {"invities_num":qs_count}
    return {}