from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from app.models import Order as OrderModel, Basket, OrderProduct, DeliveryCountries as DeliveryCountriesModel
from app.serializers.order import OrderSerializer, DeliveryCountrySerializer
from app.utils.randomId import randomId
from app.views import templateForResponse


class Order(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        order = OrderModel.objects.filter(user=request.user, buy=True)
        serializer = OrderSerializer(order, many=True)
        return Response(data=templateForResponse(serializer.data, True))

    def post(self, request):
        if request.user.confirmed:
            data = request.data

            if not data.get("street"):
                return Response(data=templateForResponse(None, False, "street is required"), status=400)
            if not data.get("home"):
                return Response(data=templateForResponse(None, False, "home is required"), status=400)
            if not data.get("telephone"):
                return Response(data=templateForResponse(None, False, "telephone is required"), status=400)
            if not data.get("delivery_city"):
                return Response(data=templateForResponse(None, False, "delivery_city is required"), status=400)

            basket = Basket.objects.filter(user=request.user, buy=False)
            if not len(basket):
                return Response(data=templateForResponse(None, False, "your basket is empty"), status=400)

            order = OrderModel.objects.create(
                street=data.get("street"),
                home=data.get("home"),
                telephone=data.get("telephone"),
                delivery_city_id=data.get("delivery_city"),
                order_id=randomId(),
                user=request.user,
                buy=True
            )

            total_quantity = 0
            total_price = 0

            for item in basket:
                total_quantity += float(item.quantity)
                total_price += float(item.total)
                item.product.quantity -= float(item.quantity)
                OrderProduct.objects.create(order=order, basket=item)
                item.save()

            delivery = DeliveryCountriesModel.objects.get(pk=data.get("delivery_city"))
            order.quantity = total_quantity
            order.total = float(total_price) + float(delivery.delivery_price)
            order.buy = True
            order.save()

            for item in basket:
                item.buy = True
                item.save()

            products = OrderProduct.objects.filter(basket__user=request.user, order=order)
            text = ""
            for item in products:
                text += f"------------ PRODUCTS ------------\n" \
                        f"product: {item.basket.product.name}\n" \
                        f"total price: {item.basket.total} AED\n" \
                        f"quantity: {item.basket.quantity} {item.basket.product.product_type}\n\n"

            send_mail(
                f"Your items are framed",
                f"Soon your products will be delivered, the delivery price depends on the city of delivery.\n"
                f"(If your products are still not delivered, then get in touch with us)\n\n"
                f"created time: {products.last().order.created_at}\n"
                f"order id: #{products.last().order.order_id}\n"
                f"total price: {products.last().order.total} AED\n"
                f"total quantity: {products.last().order.quantity} kg/pcs\n"
                f"my telephone: {products.last().order.telephone} kg/pcs\n"
                f"------------ DELIVERY ------------\n"
                f"delivery price: {products.last().order.delivery_city.delivery_price} AED\n"
                f"city: {products.last().order.delivery_city.city}\n"
                f"street: {products.last().order.street}\n"
                f"home: {products.last().order.home}\n"
                f"{text}",
                "bonafresco@gmail.com",
                ["bonafresco@gmail.com", request.user.custom_email.email]
            )

            return Response(data=templateForResponse("your order has been placed", True))
        return Response(data=templateForResponse(None, False, "Confirm your email first"), status=400)


class DeliveryCountries(APIView):

    def get(self, request):
        countries = DeliveryCountriesModel.objects.all()
        serializer = DeliveryCountrySerializer(countries, many=True)
        return Response(data=templateForResponse(serializer.data, True))
