from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from.models import Profile,Bag_kurma
from .forms import ProfileModelForm
from django.views.generic import ListView,DetailView
from django.contrib.auth.models import User
from django.db.models import Q

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required
def home_view(reguest):
    user=reguest.user
    hello="hello world"

    context={
        "user":user,
        "hello":hello
    }
    return render(reguest,"main/home.html",context)
    #return HttpResponse("Merhaba Serdar")


@login_required
def profilim(request):

    profile = Profile.objects.get(user=request.user)
    form=ProfileModelForm(request.POST or None,request.FILES or None,instance=profile)
    confirm=False

    if request.method=="POST":
        if form.is_valid():
            form.save()
            confirm=True

    context={
        "profile":profile,
        "form":form,
        "confirm":confirm
    }
    return render(request,"profiles/myprofile.html",context)

@login_required
def invities_recived_view(request):
    profile = Profile.objects.get(user=request.user)
    qs=Bag_kurma.objects.invatations_recived(profile)
    results=list(map(lambda x:x.sender,qs))
    is_empty=False

    if len(results)==0:
        is_empty=True

    context={
        "qs":results,
        "is_empty":is_empty,
             }

    return render(request,"profiles/my_invities.html",context)



#arkadaşlık listeğinin kabul etmek için
@login_required
def accept_invatation(request):
    if request.method=="POST":
        pk=request.POST.get("profile_pk")
        sender=Profile.objects.get(pk=pk)
        receiver=Profile.objects.get(user=request.user)
        rel=get_object_or_404(Bag_kurma,sender=sender,reciver=receiver)
        if rel.status=="send":
            rel.status="accepted"
            rel.save()
    return redirect("profiles:my-invities-view")


#arkadaşlık listeğinin reddetmek için
@login_required
def reject_invatation(request):
    if request.method == "POST":
        pk = request.POST.get("profile_pk")
        receiver = Profile.objects.get(user=request.user)
        sender = Profile.objects.get(pk=pk)
        rel = get_object_or_404(Bag_kurma, sender=sender, reciver=receiver)
        rel.delete()
    return redirect("profiles:my-invities-view")


@login_required
def invite_profiles_list_view(request):
    user=request.user
    qs=Profile.objects.get_all_to_invate(user)

    context={"qs":qs}

    return render(request, "profiles/to_invite_list.html", context)


@login_required
def profile_list_view(request):
    user=request.user
    qs=Profile.objects.get_all_profiles(user)

    context={"qs":qs}
    return render(request,"profiles/profile_list.html",context)



class ProfileDetailView(LoginRequiredMixin,DetailView):
    model = Profile
    template_name = "profiles/detail.html"

    def get_object(self, slug=None):
        slug=self.kwargs.get("slug")
        profile=Profile.objects.get(slug=slug)
        return profile


    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        user=User.objects.get(username__iexact=self.request.user)
        profile=Profile.objects.get(user=user)

        rel_r=Bag_kurma.objects.filter(sender=profile)                 #alıcı bağ kuran
        rel_s=Bag_kurma.objects.filter(reciver=profile)                   #gönderici bağ kuran

        rel_reciver=[]
        rel_sender=[]

        for item in rel_r:
            rel_reciver.append(item.reciver.user)

        for item in rel_s:
            rel_sender.append(item.sender.user)

        context["rel_receiver"]=rel_reciver
        context["rel_sender"]=rel_sender
        context["posts"]=self.get_object().get_all_authors_posts()
        context["len_posts"]=True if len(self.get_object().get_all_authors_posts()) > 0 else False
        return context



class ProfileListView(LoginRequiredMixin,ListView):
    model = Profile
    template_name = "profiles/profile_list.html"
    context_object_name = "qs"

    def get_queryset(self):
        qs=Profile.objects.get_all_profiles(self.request.user)
        return qs

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        user=User.objects.get(username__iexact=self.request.user)
        profile=Profile.objects.get(user=user)

        rel_r=Bag_kurma.objects.filter(sender=profile)                 #alıcı bağ kuran
        rel_s=Bag_kurma.objects.filter(reciver=profile)                   #gönderici bağ kuran

        rel_reciver=[]
        rel_sender=[]

        for item in rel_r:
            rel_reciver.append(item.reciver.user)

        for item in rel_s:
            rel_sender.append(item.sender.user)

        context["rel_receiver"]=rel_reciver
        context["rel_sender"]=rel_sender
        context["is_empty"]=False

        if len(self.get_queryset())==0:
            context["is_empty"]=True

        return context


@login_required
def send_invatation(request):
    if request.method=="POST":
        pk=request.POST.get("profile_pk")
        user=request.user
        sender=Profile.objects.get(user=user)
        receiver=Profile.objects.get(pk=pk)

        rel=Bag_kurma.objects.create(sender=sender,reciver=receiver,status="send")

        return redirect(request.META.get("HTTP_REFERER"))

    return redirect("profiles:my-profile-view")

@login_required
def remove_from_friends(request):
    if request.method == "POST":
        pk = request.POST.get("profile_pk")
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Bag_kurma.objects.filter(Q(sender=sender) & Q(reciver=receiver) | Q(sender=receiver) & Q(reciver=sender))
        rel.delete()

        return redirect(request.META.get("HTTP_REFERER"))

    return redirect("profiles:my-profile-view")









