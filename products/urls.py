from django.urls import path
from products.views import ProductCreateListView,ProductDetailView

urlpatterns = [
    path("product/create/", ProductCreateListView.as_view(), name="product_create"),
    path("product/<str:slug>/",ProductDetailView.as_view(),name="product_details"),
    path("products/catalog/", ProductCreateListView.as_view(), name="products_catalog"),
]
