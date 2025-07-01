from django.urls import path
from .views import ProfileCreateView, ProfileDetailView, get_my_profile,  update_my_profile
 
urlpatterns = [
    path('create/', ProfileCreateView.as_view(), name='profile-create'),
    path('me/', ProfileDetailView.as_view(), name='profile-detail'),
    path('me/', get_my_profile),
    path('me/update/', update_my_profile), 
]

