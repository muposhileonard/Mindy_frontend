from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from profileengine.views import ProfileDetailView

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authengine.urls')),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', include('profileengine.urls')),
    path('profile/<int:pk>/', ProfileDetailView.as_view()),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



