from django.urls import path
from wallet import views

# Create your views here.
urlpatterns = [
    path("create/", views.CreateWalletAPI.as_view()),
    path("list/", views.GetWalletListAPI.as_view()),
    path("detail/<int:pk>/", views.GetWalletDetailAPI.as_view()),
    path("update/<int:pk>/", views.UpdateWalletAPI.as_view()),
    path("delete/<int:pk>/", views.DeleteWalletAPI.as_view()),
]
