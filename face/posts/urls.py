from django.urls import path
from .views import post_comment_create_and_list_view,like_unlike_post,PostDeleteView,UpdatePostView

app_name="posts"

urlpatterns = [
    path('', post_comment_create_and_list_view,name="main-post-view"),   #profiles/myprofile ilk profiles faces dosyası içindeki url den diğer my profile ise profiles dosyası içindeki url den geliyor
    path('liked/', like_unlike_post,name="like-post-view"),
    path('<pk>/delete/', PostDeleteView.as_view(),name="post-delete"),
    path('<pk>/update/', UpdatePostView.as_view(),name="post-update"),
]