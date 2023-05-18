from django.db.models import Sum, Count
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import Category, Basket, Banner as BannerModel
from app.serializers.categories import CategorySerializer
from app.serializers.products import ProductSerializer
from app.views import templateForResponse


# mix ---------
class BannerSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False)

    class Meta:
        model = BannerModel
        fields = "__all__"


# end mix -----------

class Home(APIView):

    def get(self, request):
        banner = BannerModel.objects.all()
        count, total = 0, 0
        if request.auth:
            basket = Basket.objects.filter(user=request.user, buy=False).aggregate(total=Sum("total"),
                                                                                   count=Count("pk"))
            count += basket.get("count") if basket.get("count") else 0
            total += basket.get("total") if basket.get("total") else 0
        serializerBanner = BannerSerializer(banner, many=True)
        return Response(data=templateForResponse({
            "count": count,
            "total": total,
            "banner": serializerBanner.data
        }, True))
