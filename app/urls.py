from django.urls import path

from app.views.basket import *
from app.views.categories import GetAllCategories, OneCategory
from app.views.home import Home
from app.views.order import Order, DeliveryCountries
from app.views.products import *
from app.views.promo import AllPromo
from app.views.subcategories import GetAllSubCategories, OneSubCategories
from app.views.wishlist import Wishlist

urlpatterns = [
    path("/home/", Home.as_view(), name="home"),

    path("/products", GetAllProducts.as_view(), name="all-products"),
    path("/products/<pk>", OneProduct.as_view(), name="one-product"),

    path("/categories", GetAllCategories.as_view(), name="all-categories"),
    path("/categories/<pk>", OneCategory.as_view(), name="one-category"),

    path("/subcategories", GetAllSubCategories.as_view(), name="all-subCategories"),
    path("/subcategories/<pk>", OneSubCategories.as_view(), name="one-subCategories"),

    path("/promo", AllPromo.as_view(), name="all-promo"),

    path("/basket", Basket.as_view(), name="basket"),
    path("/basket-total", TotalPrice.as_view(), name="basket-total"),

    path("/order", Order.as_view(), name="order"),

    path("/delivery-countries", DeliveryCountries.as_view(), name="delivery-countries"),

    path("/wishlist", Wishlist.as_view(), name="wishlist")
]
