from django.urls import path
from transaction import views

# Create your views here.
urlpatterns = [
    path("create/", views.CreateTransactionAPI.as_view()),
    path("list/", views.GetTransactionListAPI.as_view()),
]
