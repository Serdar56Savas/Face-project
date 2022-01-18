from django.urls import path
from .views import profilim,invities_recived_view,profile_list_view,\
    invite_profiles_list_view,ProfileListView,send_invatation,\
    remove_from_friends,accept_invatation,reject_invatation,ProfileDetailView


app_name = "profiles"

urlpatterns = [
    path('', ProfileListView.as_view(),name="all-profiles-view"),
    path('my-profile/', profilim,name="my-profile-view"),   #profiles/myprofile ilk profiles faces dosyası içindeki url den diğer my profile ise profiles dosyası içindeki url den geliyor
    path('my-invities/', invities_recived_view,name="my-invities-view"),
    path('to-invite/', invite_profiles_list_view,name="invite-profiles-view"),
    path('send-invite/', send_invatation,name="send-invite-view"),
    path('remove-friend/', remove_from_friends,name="remove-friend-view"),
    path('<slug>/', ProfileDetailView.as_view(),name="profile-detail-view"),
    path('my-invities/accept', accept_invatation,name="accept-invite"),
    path('my-invities/reject', reject_invatation,name="reject-invite"),
]