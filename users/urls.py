from django.urls import path
from users.views import UserCreateView, UserDetailView, ListUsersView,ProfileView

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="register"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("users/", ListUsersView.as_view(), name="users"),
    path("users/<int:user_id>/", UserDetailView.as_view(), name="user_details"),
]
