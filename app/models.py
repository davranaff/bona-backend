from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User


# Create your models here.


class BaseModel(models.Model):
    created_at = models.DateTimeField(verbose_name="created date/time", auto_created=True, auto_now_add=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    name = models.CharField(max_length=100, verbose_name="category name", blank=True, null=True)
    image = models.ImageField(verbose_name="category image", upload_to="category/", blank=True, null=True)

    def __str__(self):
        return f"#{self.pk} {self.name}"

    class Meta:
        ordering = ['id']


class SubCategory(BaseModel):
    name = models.CharField(max_length=100, verbose_name="subcategory name", blank=True, null=True)
    image = models.ImageField(verbose_name="subcategory image", upload_to="subcategory/", blank=False, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategory_category",
                                 related_query_name="category_subcategory", blank=True,
                                 null=True)

    def __str__(self):
        return f'#{self.id} {self.name}'

    class Meta:
        ordering = ['id']


class ProductCountry(BaseModel):
    name = models.CharField(max_length=100, verbose_name='The name of the country', blank=True, null=True, unique=True)

    def __str__(self):
        return f'#{self.pk} {self.name}'

    class Meta:
        ordering = ['id']


class ProductType(BaseModel):
    TYPES = (
        ("kg", "kilogram"),
        ("pcs", "pieces"),
    )
    type = models.CharField(max_length=20, choices=TYPES, verbose_name="product type", unique=True, blank=True, null=True)

    def __str__(self):
        return self.type

    class Meta:
        ordering = ['id']


class Product(BaseModel):
    name = models.CharField(max_length=100, verbose_name="product name", unique=True, blank=True, null=True)
    image = models.ImageField(verbose_name="product image", upload_to="products/", blank=True, null=True)
    product_code = models.CharField(verbose_name="product code", max_length=50, unique=True, blank=True, null=False)
    price = models.DecimalField(verbose_name="product price", max_digits=30, decimal_places=2, blank=True, null=False)
    description = models.TextField(verbose_name="product description", blank=True, null=False)
    quantity = models.FloatField(verbose_name='Quantity in stock (kg or pieces)', blank=True, null=False)

    discount = models.BooleanField(verbose_name="product discount", default=False, blank=False, null=True)
    discount_percent = models.IntegerField(verbose_name="product discount percent exm: (5, 10, 100)", default=0,
                                           blank=True, null=False,
                                           validators=[MaxValueValidator(100), MinValueValidator(0)])

    subcategory = models.ForeignKey(SubCategory, on_delete=models.PROTECT, related_name="product_subcategory",
                                    blank=True, null=False)
    product_type = models.ForeignKey(ProductType, on_delete=models.PROTECT, related_name="product_type", blank=True,
                                     null=False)
    country = models.ForeignKey(ProductCountry, on_delete=models.PROTECT, related_name="product_type", blank=True,
                                null=False)

    def __str__(self):
        return f'#{self.pk} {self.name}'

    class Meta:
        ordering = ['id']


class DeliveryCountries(BaseModel):
    city = models.CharField(max_length=100, verbose_name="delivery cities", unique=True, blank=True, null=False)
    delivery_price = models.FloatField(verbose_name="deliver price", blank=True, null=True)

    def __str__(self):
        return f'#{self.city}'

    class Meta:
        ordering = ['id']


class Basket(BaseModel):
    total = models.DecimalField(verbose_name="total price", max_digits=30, decimal_places=2, blank=True, null=False)
    quantity = models.FloatField(verbose_name="total quantity", blank=True, null=False)

    user = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=False)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, blank=True, null=False)
    buy = models.BooleanField(verbose_name="buyed", default=False, blank=False, null=False)

    def __str__(self):
        return f'#{self.pk} {self.user}'

    class Meta:
        ordering = ['id']


class Order(BaseModel):
    total = models.DecimalField(verbose_name="total price", max_digits=30, decimal_places=2, blank=True, null=True)
    quantity = models.FloatField(verbose_name="total quantity", blank=True, null=True)
    street = models.TextField(verbose_name="street", blank=True, null=False)
    home = models.TextField(verbose_name="home", blank=True, null=False)
    telephone = models.CharField(max_length=100, verbose_name="telephone number", blank=True, null=False)

    buy = models.BooleanField(verbose_name="buyed", blank=False, null=True)
    order_id = models.BigIntegerField(verbose_name="order id", blank=False, null=True)

    delivery_city = models.ForeignKey(DeliveryCountries, models.PROTECT, related_name="order_country", blank=True,
                                      null=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=False)

    def __str__(self):
        return f'#{self.order_id}'

    class Meta:
        ordering = ['id']


class OrderProduct(BaseModel):
    basket = models.ForeignKey(Basket, on_delete=models.PROTECT, related_name="order_product_basket", blank=True,
                               null=False)
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name="order_product_order", blank=True,
                              null=False)

    def __str__(self):
        return f'{self.basket.product.name} {self.order}'

    class Meta:
        ordering = ['id']


class Banner(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="banner_product", blank=True, null=True)
    image = models.ImageField(verbose_name="banner image", upload_to="banner/", blank=True, null=True)

    def __str__(self):
        return self.product.name


class Wishlist(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="wishlist_product", blank=True,
                                null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlist_user", blank=True, null=True)

    class Meta:
        unique_together = ("product", "user")
