from django.db.models import Q, Count
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import Product
from app.serializers.products import ProductSerializer
from app.views import templateForResponse


class AllPromo(APIView):

    def get(self, request):
        products = Product.objects.filter(discount=True)
        if request.auth:
            products = products.annotate(
                is_liked=Count("wishlist_product", filter=Q(wishlist_product__user=request.user)))
        serializer = ProductSerializer(products, many=True)
        return Response(data=templateForResponse(serializer.data, True))
