from django.urls import path

from address.views import AddressCreateView


urlpatterns = [
    path("profile/address/", AddressCreateView.as_view(), name="create_address"),
    # path("profile/address/", AddressRetrieveView.as_view(), name="address_details"),
]
