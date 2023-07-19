from django.urls import path
from users.views import UserCreateView, UserDetailView, ListUsersView

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="register"),
    path("users/<int:user_id>/", UserDetailView.as_view(), name="user_details"),
    path("users/", ListUsersView.as_view(), name="users"),
]
