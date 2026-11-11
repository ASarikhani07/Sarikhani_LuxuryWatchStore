from django.contrib import admin
from .models import Brand, Category, Comment, Customer, Product, ProductColor, ProductImage, WishList


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductColorInline(admin.TabularInline):
    model = ProductColor
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "brand", "category", "price", "is_available", "is_special", "is_luxury", "stash")
    list_filter = ("brand", "category", "is_available", "is_special", "is_luxury", "gender", "engine")
    search_fields = ("title", "brand__name", "description")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ProductImageInline, ProductColorInline]


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register([Customer, Comment, WishList])
