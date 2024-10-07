from django.urls import path
from users import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

# Create your views here.
urlpatterns = [
    path("token/", views.MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("self/", views.GetUserMeDetail.as_view(), name="token_refresh"),
]
