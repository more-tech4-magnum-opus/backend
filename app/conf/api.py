from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from events.api.views import (
    ListCreateEventApi,
    RetrieveUpdateDeleteEventApi,
    ListPlannedEvents,
    RetrieveSubmitDeleteEventAttendance,
    ListAttendedWorkersApi,
    SubmitWorkerAttendedEvent,
)
from marketplace.api.views import ListCreateProductApi, RetrieveUpdateDestroyProductApi
from users.api.views import (
    ListCreateUserApi,
    RetrieveUpdateDeleteUserApi,
    ListCreateDepartmentApi,
    RetrieveUpdateDeleteDepartmentApi,
    ListCreateStreamApi,
    RetrieveUpdateDeleteStreamApi,
    ListCreateCommandApi,
    RetrieveUpdateDeleteCommandApi,
    CreateSeasonApi,
    ListClansApiView,
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
                    RetrieveUpdateDeleteEventApi.as_view(),
                    name="get_update_delete_event",
                ),
                path(
                    "attendance/",
                    ListPlannedEvents.as_view(),
                    name="list_event_attendance",
                ),
                path(
                    "attendance/<str:slug>/list/",
                    ListAttendedWorkersApi.as_view(),
                    name="list_event_attendance",
                ),
                path(
                    "attendance/<str:slug>/submit/",
                    SubmitWorkerAttendedEvent.as_view(),
                    name="submit_event_attendance",
                ),
                path(
                    "attendance/<str:slug>",
                    RetrieveSubmitDeleteEventAttendance.as_view(),
                    name="get_submit_delete_event_attendance",
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
                    RetrieveUpdateDestroyProductApi.as_view(),
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
                    RetrieveUpdateDeleteUserApi.as_view(),
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
                    RetrieveUpdateDeleteDepartmentApi.as_view(),
                    name="get_update_delete_department",
                ),
                path(
                    "stream/",
                    ListCreateStreamApi.as_view(),
                    name="list_create_stream",
                ),
                path(
                    "stream/<int:pk>",
                    RetrieveUpdateDeleteStreamApi.as_view(),
                    name="get_update_delete_stream",
                ),
                path(
                    "command/",
                    ListCreateCommandApi.as_view(),
                    name="list_create_command",
                ),
                path(
                    "command/<int:pk>",
                    RetrieveUpdateDeleteCommandApi.as_view(),
                    name="get_update_delete_command",
                ),
            ]
        ),
    ),
    path(
        "season/",
        include(
            [
                path("", CreateSeasonApi.as_view(), name="create new season"),
                path("clans/", ListClansApiView.as_view()),
            ]
        ),
    ),
]
