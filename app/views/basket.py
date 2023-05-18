from django.db.models import Sum
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from app.models import Basket as BasketModel, Product
from app.serializers.basket import BasketSerializer
from app.views import templateForResponse
from decimal import Decimal


class Basket(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        baskets = BasketModel.objects.filter(user=request.user, buy=False)
        serializer = BasketSerializer(baskets, many=True)
        return Response(data=templateForResponse(serializer.data, True))

    def post(self, request):
        if request.user.confirmed:
            data = request.data
            if not data.get("product_id"):
                return Response(data=templateForResponse(None, False, "product_id is required"), status=400)
            if not data.get("quantity"):
                return Response(data=templateForResponse(None, False, "quantity is required"), status=400)
            product = Product.objects.get(pk=data.get("product_id"))
            total = 0
            if product.discount:
                total += float(product.price - (product.price * product.discount_percent / 100)) * float(
                    data.get("quantity"))
            else:
                total += float(product.price) * float(data.get("quantity"))
            try:
                basket = BasketModel.objects.get(user=request.user, product=product)
                basket.quantity = data.get("quantity")
                basket.total = total
                basket.save()
                serializer = BasketSerializer(basket, many=False)
                return Response(data=templateForResponse(serializer.data, True))
            except:
                basket = BasketModel.objects.create(
                    user=request.user,
                    total=Decimal(total),
                    quantity=data.get("quantity"),
                    product=product
                )
                serializer = BasketSerializer(basket, many=False)
                return Response(data=templateForResponse(serializer.data, True))
        return Response(data=templateForResponse(None, False, "Confirm your email first"), status=400)

    def put(self, request):
        data = request.data
        try:
            if not data.get("basket_id"):
                return Response(data=templateForResponse(None, False, "basket_id is required"), status=400)
            BasketModel.objects.get(pk=data.get("basket_id")).delete()
            return Response(data=templateForResponse("basket deleted", True))
        except:
            return Response(data=templateForResponse(None, False, "basket is not found"), status=404)


class TotalPrice(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total_price = BasketModel.objects.filter(user=request.user, buy=False).aggregate(total_price=Sum("total"))
        return Response(data=templateForResponse(total_price.get("total_price"), True))
