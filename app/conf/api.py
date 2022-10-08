from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from marketplace.api.views import ListCreateProductApi, RetireUpdateDestroyProductApi
from users.api.views import ListCreateUserApi, CreateSeasonApi
from users.api.views import (
    ListCreateUserApi,
    RetireUpdateDeleteUserApi,
    ListCreateDepartmentApi,
    RetireUpdateDeleteDepartmentApi,
    ListCreateStreamApi,
    RetireUpdateDeleteStreamApi,
    ListCreateCommandApi,
    RetireUpdateDeleteCommandApi,
)

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
        "events/",
        include(
            [
                path("", ListCreateEventApi.as_view(), name="list_create_event"),
                path(
                    "<str:slug>",
                    RetireUpdateDeleteEventApi.as_view(),
                    name="get_update_delete_event",
                ),
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
                path("", ListCreateUserApi.as_view(), name="list_create_user"),
                path(
                    "<str:username>",
                    RetireUpdateDeleteUserApi.as_view(),
                    name="get_update_delete_user",
                ),
                path(
                    "department/",
                    ListCreateDepartmentApi.as_view(),
                    name="list_create_department",
                ),
                path(
                    "department/",
                    ListCreateDepartmentApi.as_view(),
                    name="list_create_department",
                ),
                path(
                    "department/<int:pk>",
                    RetireUpdateDeleteDepartmentApi.as_view(),
                    name="get_update_delete_department",
                ),
                path(
                    "stream/",
                    ListCreateStreamApi.as_view(),
                    name="list_create_stream",
                ),
                path(
                    "stream/<int:pk>",
                    RetireUpdateDeleteStreamApi.as_view(),
                    name="get_update_delete_stream",
                ),
                path(
                    "command/",
                    ListCreateCommandApi.as_view(),
                    name="list_create_command",
                ),
                path(
                    "command/<int:pk>",
                    RetireUpdateDeleteCommandApi.as_view(),
                    name="get_update_delete_command",
                ),
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
