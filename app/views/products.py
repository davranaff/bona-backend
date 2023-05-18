from django.db.models import Q, F, Count
from django.shortcuts import render, get_object_or_404
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import Product, Wishlist
from app.serializers.products import ProductSerializer
from app.views import templateForResponse


# Create your views here.


class OneProduct(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        try:
            products = Product.objects.get(pk=pk)
            related_products = Product.objects.filter(subcategory_id=products.subcategory)
            if request.auth:
                related_products = related_products.annotate(
                    is_liked=Count("wishlist_product", filter=Q(wishlist_product__user=request.user)))
            serializer = ProductSerializer(products, many=False)
            rel_serializer = ProductSerializer(related_products, many=True)
            return Response(data=templateForResponse({
                "product": serializer.data,
                "related": rel_serializer.data,
            }, True))
        except:
            return Response(data=templateForResponse(None, False, "product not found"))


class GetAllProducts(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        if request.GET.get("search"):
            products = Product.objects.filter(
                Q(name__icontains=request.GET.get("search")) | Q(product_code__startswith=request.GET.get("search")))
            if request.auth:
                products = products.annotate(
                    is_liked=Count("wishlist_product", filter=Q(wishlist_product__user=request.user)))
            serializer = ProductSerializer(products, many=True)
            return Response(data=templateForResponse(serializer.data, True))
        products = Product.objects.all()[:9]
        if request.auth:
            products = products.annotate(
                is_liked=Count("wishlist_product", filter=Q(wishlist_product__user=request.user)))
        serializer = ProductSerializer(products, many=True)
        return Response(data=templateForResponse(serializer.data, True))
