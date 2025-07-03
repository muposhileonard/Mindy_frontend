from django.urls import path
from .views import ProfileCreateView, ProfileDetailView, get_my_profile,  update_my_profile
from .views import download_my_data  # 👈 add this line
urlpatterns = [
    path('create/', ProfileCreateView.as_view(), name='profile-create'),
    path('me/', ProfileDetailView.as_view(), name='profile-detail'),
    path('me/', get_my_profile),
    path('me/update/', update_my_profile), 
    path('profile/download/', download_my_data),
]

