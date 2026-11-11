from django.urls import path
from .views import (
    LuxurySpecialAPIView,
    MyWishlistAPIView,
    ProductDetailAPIView,
    ProductListAPIView,
)

urlpatterns = [
    path("products/", ProductListAPIView.as_view(), name="product-list"),
    path("products/<slug:slug>/", ProductDetailAPIView.as_view(), name="product-detail"),
    path("luxury-special/", LuxurySpecialAPIView.as_view(), name="luxury-special"),
    path("me/wishlist/", MyWishlistAPIView.as_view(), name="my-wishlist"),
]
