from django.urls import path
from core import views

# Create your views here.
urlpatterns = [
    path("icons/list/", views.GetIconListAPI.as_view()),
]
