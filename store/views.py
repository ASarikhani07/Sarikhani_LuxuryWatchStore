from django.db.models import Avg, F
from django.db.models import DecimalField
from django.db.models.functions import Cast
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, WishList
from .serializers import (
    LuxuryProductSerializer,
    ProductDetailSerializer,
    ProductListSerializer,
    WishlistItemSerializer,
)


class ProductListAPIView(APIView):
    def get(self, request):
        products = (
            Product.objects
            .select_related("brand", "category")
            .only(
                "id", "title", "slug", "price", "is_available", "stash",
                "brand__id", "brand__name", "category__id", "category__title",
            )
        )
        return Response(ProductListSerializer(products, many=True).data)


class ProductDetailAPIView(APIView):
    def get(self, request, slug):
        product = get_object_or_404(
            Product.objects
            .select_related("brand", "category")
            .prefetch_related("images", "colors", "comments__customer__user"),
            slug=slug,
        )

        # F() performs an atomic database-side increment; it avoids a read-modify-write race.
        Product.objects.filter(pk=product.pk).update(click_count=F("click_count") + 1)
        product.refresh_from_db(fields=["click_count"])

        return Response(ProductDetailSerializer(product).data)


class LuxurySpecialAPIView(APIView):
    def get(self, request):
        luxury_products = Product.objects.filter(
            is_special=True,
            is_luxury=True,
            is_available=True,
        ).order_by("id")

        # One aggregate query calculates the average price for the entire filtered queryset.
        average_price = luxury_products.aggregate(avg_price=Avg("price"))["avg_price"]

        # Return the average once at response level, rather than repeating it per product.
        return Response({
            "average_luxury_price": average_price,
            "products": LuxuryProductSerializer(luxury_products, many=True).data,
        })


class MyWishlistAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wishlist = (
            WishList.objects
            .filter(customer__user=request.user)
            .select_related(
                "product",
                "customer",
                "customer__user",
            )
            .order_by("-created_at")
        )
        return Response(WishlistItemSerializer(wishlist, many=True).data)
