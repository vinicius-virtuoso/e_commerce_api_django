from django.urls import path

from address.views import AddressCreateView

urlpatterns = [
    path("profile/address/", AddressCreateView.as_view(), name="address"),
]
