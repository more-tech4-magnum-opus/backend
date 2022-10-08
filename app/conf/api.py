from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from marketplace.api.views import ListCreateProductApi, RetireUpdateDestroyProductApi
from users.api.views import ListCreateUserApi, CreateSeasonApi

urlpatterns = [
    path(
        "auth/",
        include(
            [
                path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
                path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
            ]
        ),
    ),
    path(
        "marketplace/",
        include(
            [
                path(
                    "product/",
                    ListCreateProductApi.as_view(),
                    name="list_create_product",
                ),
                path(
                    "product/<str:slug>",
                    RetireUpdateDestroyProductApi.as_view(),
                    name="get_update_destroy_product",
                ),
            ]
        ),
    ),
    path(
        "users/",
        include(
            [
                path("", ListCreateUserApi.as_view(), name="user_list_create"),
            ]
        ),
    ),
    path(
        'create_season/',
        include(
            [
                path("", CreateSeasonApi.as_view(), name='create new season')
            ]
        )
    )
]
