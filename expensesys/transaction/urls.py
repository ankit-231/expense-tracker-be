from django.urls import path, include
from transaction import views

# Create your views here.
urlpatterns = [
    path("create/", views.CreateTransactionAPI.as_view()),
    path("list/", views.GetTransactionListAPI.as_view()),
    path("list/paginated/", views.GetTransactionListPaginatedAPI.as_view()),
    path("update/<int:pk>/", views.UpdateTransactionAPI.as_view()),
    path("detail/<int:pk>/", views.GetTransactionDetailAPI.as_view()),
    path("delete/<int:pk>/", views.DeleteTransactionAPI.as_view()),
    path(
        "category/",
        include(
            (
                [
                    path("create/", views.CreateTransactionCategoryAPI.as_view()),
                    path(
                        "list/<str:category_type>/",
                        views.GetTransactionCategoryListAPI.as_view(),
                    ),
                    path(
                        "update/<int:pk>/", views.UpdateTransactionCategoryAPI.as_view()
                    ),
                    path(
                        "delete/<int:pk>/", views.DeleteTransactionCategoryAPI.as_view()
                    ),
                ],
                "category",
            ),
        ),
    ),
    path(
        "statistics/monthly/<int:year>/<int:month>/",
        views.GetMonthlyStatisticsAPI.as_view(),
    ),
]
