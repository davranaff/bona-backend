from django.db.models import Count, Q
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import Category, SubCategory, Product
from app.serializers.categories import CategorySerializer
from app.serializers.products import ProductSerializer
from app.serializers.subcategories import SubCategorySerializer
from app.views import templateForResponse


class GetAllCategories(APIView):

    def get(self, request):
        if request.GET.get("limit"):
            categories = Category.objects.all()[:int(request.GET.get("limit"))]
            serializer = CategorySerializer(categories, many=True)
            return Response(data=templateForResponse(serializer.data, True))
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(data=templateForResponse(serializer.data, True))


class OneCategory(APIView):

    def get(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
            subcategory = SubCategory.objects.filter(category_id=category.pk)
            products = Product.objects.filter(subcategory__category_id=category.pk)
            if request.auth:
                products = products.annotate(
                    is_liked=Count("wishlist_product", filter=Q(wishlist_product__user=request.user)))
            serializerCategory = CategorySerializer(category, many=False)
            serializerSubCategory = SubCategorySerializer(subcategory, many=True)
            serializerProduct = ProductSerializer(products, many=True)
            return Response(data=templateForResponse({
                "category": serializerCategory.data,
                "subcategory": serializerSubCategory.data,
                "products": serializerProduct.data
            }, True))
        except:
            return Response(data=templateForResponse(None, False, "Not Found"), status=400)
