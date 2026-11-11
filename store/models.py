from django.conf import settings
from django.db import models
from django.utils.text import slugify


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseModel(TimeStampedModel):
    # Common abstract base requested by the assignment.
    class Meta:
        abstract = True


class SluggedMixinModel(models.Model):
    slug = models.SlugField(max_length=220, unique=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            source = getattr(self, "title", None) or getattr(self, "name", None) or "item"
            base_slug = slugify(source) or "item"
            candidate = base_slug
            index = 1
            ModelClass = self.__class__
            while ModelClass.objects.filter(slug=candidate).exclude(pk=self.pk).exists():
                index += 1
                candidate = f"{base_slug}-{index}"
            self.slug = candidate
        super().save(*args, **kwargs)


class Brand(TimeStampedModel):
    name = models.CharField(max_length=120, unique=True)
    meta_title = models.CharField(max_length=180, blank=True)
    meta_description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Category(TimeStampedModel, SluggedMixinModel):
    title = models.CharField(max_length=120, unique=True)

    class Meta:
        ordering = ["title"]
        verbose_name_plural = "categories"

    def __str__(self):
        return self.title


class Customer(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="customer_profile")
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.username


class Product(BaseModel, SluggedMixinModel):
    class Gender(models.TextChoices):
        MEN = "men", "Men"
        WOMEN = "women", "Women"
        UNISEX = "unisex", "Unisex"

    class Origin(models.TextChoices):
        SWISS = "swiss", "Swiss"
        JAPANESE = "japanese", "Japanese"
        GERMAN = "german", "German"
        OTHER = "other", "Other"

    class StrapMaterial(models.TextChoices):
        LEATHER = "leather", "Leather"
        STEEL = "steel", "Steel"
        RUBBER = "rubber", "Rubber"
        FABRIC = "fabric", "Fabric"
        OTHER = "other", "Other"

    class Usage(models.TextChoices):
        FORMAL = "formal", "Formal"
        SPORT = "sport", "Sport"
        DAILY = "daily", "Daily"
        DRESS = "dress", "Dress"

    class Design(models.TextChoices):
        CLASSIC = "classic", "Classic"
        MODERN = "modern", "Modern"
        MINIMAL = "minimal", "Minimal"
        LUXURY = "luxury", "Luxury"

    class Engine(models.TextChoices):
        QUARTZ = "quartz", "Quartz"
        AUTOMATIC = "automatic", "Automatic"
        MECHANICAL = "mechanical", "Mechanical"
        SMART = "smart", "Smart"

    title = models.CharField(max_length=220)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name="products")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    price = models.DecimalField(max_digits=12, decimal_places=2)
    is_discount = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    is_special = models.BooleanField(default=False)
    gender = models.CharField(max_length=10, choices=Gender.choices, default=Gender.UNISEX)
    origin = models.CharField(max_length=12, choices=Origin.choices, default=Origin.OTHER)
    strap_material = models.CharField(max_length=12, choices=StrapMaterial.choices, default=StrapMaterial.OTHER)
    usage = models.CharField(max_length=12, choices=Usage.choices, default=Usage.DAILY)
    design = models.CharField(max_length=12, choices=Design.choices, default=Design.CLASSIC)
    engine = models.CharField(max_length=12, choices=Engine.choices, default=Engine.QUARTZ)
    main_image = models.ImageField(upload_to="products/main/", blank=True, null=True)
    features = models.JSONField(default=dict, blank=True)
    is_luxury = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    meta_title = models.CharField(max_length=180, blank=True)
    meta_description = models.TextField(blank=True)
    stash = models.PositiveIntegerField(default=0)
    click_count = models.PositiveBigIntegerField(default=0)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["is_special", "is_luxury", "is_available"]),
            models.Index(fields=["-created_at"]),
        ]

    def __str__(self):
        return self.title


class ProductImage(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="products/gallery/")

    def __str__(self):
        return f"Image for {self.product.title}"


class ProductColor(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="colors")
    color = models.CharField(max_length=60)
    hex_code = models.CharField(max_length=7, help_text="Example: #000000")

    def __str__(self):
        return f"{self.color} - {self.product.title}"


class Comment(TimeStampedModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="comments")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments")
    body = models.TextField()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Comment by {self.customer}"


class WishList(TimeStampedModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="wishlist_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="wishlisted_by")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["product", "customer"], name="unique_customer_product_wishlist")
        ]

    def __str__(self):
        return f"{self.customer} - {self.product}"
