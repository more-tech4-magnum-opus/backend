from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

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
        "user/",
        include(
            [
            ]
        ),
    ),
]
