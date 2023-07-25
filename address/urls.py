from django.urls import path

from address.views import AddressCreateView, AddressDetailsView

urlpatterns = [
    path("profile/address/create/", AddressCreateView.as_view(), name="address_create"),
    path("profile/address/", AddressDetailsView.as_view(), name="address_details"),
]
