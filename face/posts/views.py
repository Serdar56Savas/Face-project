from django.shortcuts import render,redirect
from .models import Posts,Like
from profiles.models import Profile
from .forms import PostModelForm,CommentModelForm

from django.views.generic import UpdateView,DeleteView
from django.urls import reverse_lazy
from django.contrib import messages

from django.http import JsonResponse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required
def post_comment_create_and_list_view(request):

    profile=Profile.objects.get(user=request.user)
    qs=Posts.objects.all()

    p_form=PostModelForm()
    c_form=CommentModelForm()
    post_added=False

    if "submit_p_form" in request.POST:
        p_form=PostModelForm(request.POST,request.FILES)
        if p_form.is_valid():
            instance = p_form.save(commit=False)
            instance.author = profile
            instance.save()
            p_form = PostModelForm()
            post_added=True
        return redirect("posts:main-post-view")

    if "submit_c_form" in request.POST:
        c_form=CommentModelForm(request.POST)
        if c_form.is_valid():
            instance=c_form.save(commit=False)
            instance.user=profile
            instance.post=Posts.objects.get(id=request.POST.get("post_id"))
            instance.save()
            c_form=CommentModelForm()
            return redirect("posts:main-post-view")

    context={
        "qs":qs,
        "profile":profile,
        "p_form":p_form,
        "c_form":c_form,
        "post_added":post_added

    }
    return render(request,"posta/main.html",context)

@login_required
def like_unlike_post(request):
    user=request.user
    if request.method=="POST":
        post_id=request.POST.get("post_id")
        post_obj=Posts.objects.get(id=post_id)
        profile=Profile.objects.get(user=user)

        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
        else:
            post_obj.liked.add(profile)

        like,created=Like.objects.get_or_create(user=profile,post_id=post_id)

        if not created:
            if like.value=="Like":
                like.value="Unlike"
            else:
                like.value="Like"

        else:
            like.value="Like"

            post_obj.save()
            like.save()

        data={
            "value":like.value,
            "likes":post_obj.liked.all().count()
        }
        return JsonResponse(data,safe=False)

    return redirect("posts:main-post-view")


class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Posts
    template_name ="posts/delete.html"
    success_url = reverse_lazy("posts:main-post-view")

    def get_object(self,*args,**kwargs):
        pk=self.kwargs.get("pk")
        obj=Posts.objects.get(pk=pk)
        if not obj.author.user == self.request.user:
            messages.warning(self.request,"Bu g??nderiyi silmek i??in yetkiniz bulunmamaktad??r!")
        return obj


class UpdatePostView(LoginRequiredMixin,UpdateView):
    form_class = PostModelForm
    model = Posts
    template_name = "posts/update.html"
    success_url = reverse_lazy("posts:main-post-view")

    def form_valid(self, form):
        profile=Profile.objects.get(user=self.request.user) #sistemdeki kullan??c??y?? profile atad??k

        if form.instance.author==profile:
            return super().form_valid(form)  #profile ve author e??itse g??ncellesin
        else:                                #e??it de??ilse g??ncelleme hata mesaj??n?? g??stersin
            form.add_erro(None,"Bu g??nderiyi g??ncellemek i??in yetkiniz bulunmamaktad??r!")
            return super().form_invalid(form)
