from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

router_v1 = DefaultRouter()
router_v1.register("posts", views.PostViewSet, basename="posts")
router_v1.register(
    r"^posts/(?P<post_id>\d+)/comments",
    views.CommentViewSet,
    basename="comments",
)
router_v1.register("group", views.GroupViewSet, basename="groups")
router_v1.register("follow", views.FollowViewSet, basename="follow")


urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", include(router_v1.urls)),
]
