from django.db.models import Count, Q
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import SubCategory, Product
from app.serializers.products import ProductSerializer
from app.serializers.subcategories import SubCategorySerializer
from app.views import templateForResponse


class GetAllSubCategories(APIView):

    def get(self, request):
        subCategories = SubCategory.objects.all()
        serializer = SubCategorySerializer(subCategories, many=True)
        return Response(data=templateForResponse(serializer.data, True))


class OneSubCategories(APIView):

    def get(self, request, pk):
        try:
            subCategory = SubCategory.objects.get(pk=pk)
            products = Product.objects.filter(subcategory=subCategory)
            if request.auth:
                products = products.annotate(
                    is_liked=Count("wishlist_product", filter=Q(wishlist_product__user=request.user)))
            serializer = SubCategorySerializer(subCategory, many=False)
            productSerializer = ProductSerializer(products, many=True)
            return Response(data=templateForResponse({
                "subcategory": serializer.data,
                "products": productSerializer.data
            }, True))
        except:
            return Response(data=templateForResponse(None, False, "Not Found"), status=400)
