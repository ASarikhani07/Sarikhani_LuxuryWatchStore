from rest_framework import serializers
from .models import Brand, Category, Comment, Customer, Product, ProductColor, ProductImage, WishList


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "name", "meta_title", "meta_description"]


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="title", read_only=True)

    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class ProductListSerializer(serializers.ModelSerializer):
    brand = serializers.CharField(source="brand.name", read_only=True)
    category = serializers.CharField(source="category.title", read_only=True)

    class Meta:
        model = Product
        fields = ["id", "title", "slug", "price", "brand", "category", "is_available", "stash"]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image", "created_at"]


class ProductColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductColor
        fields = ["id", "color", "hex_code"]


class CommentSerializer(serializers.ModelSerializer):
    customer = serializers.CharField(source="customer.user.username", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "customer", "body", "created_at"]


class ProductDetailSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    colors = ProductColorSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = "__all__"


class LuxuryProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "title", "price", "gender", "strap_material", "engine"]


class WishlistProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["title", "slug", "price", "stash", "main_image"]


class WishlistCustomerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Customer
        fields = ["username", "email", "phone_number"]


class WishlistItemSerializer(serializers.ModelSerializer):
    product = WishlistProductSerializer(read_only=True)
    customer = WishlistCustomerSerializer(read_only=True)

    class Meta:
        model = WishList
        fields = ["id", "product", "customer", "created_at"]
