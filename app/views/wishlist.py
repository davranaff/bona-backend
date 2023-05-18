from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from app.models import Wishlist as WishlistModel
from app.serializers.wishlist import WishlistSerializer
from app.views import templateForResponse


class Wishlist(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wishlist = WishlistModel.objects.filter(user=request.user)
        serializer = WishlistSerializer(wishlist, many=True)
        return Response(data=templateForResponse(serializer.data, True))

    def post(self, request):
        if request.user:
            if request.user.confirmed:
                data = request.data
                if not data.get("product_id"):
                    return Response(data=templateForResponse(None, False, "product_id is required"), status=400)
                WishlistModel.objects.create(user=request.user, product_id=data.get("product_id"))
                return Response(data=templateForResponse("product has been added to the wishlist", True))
            return Response(data=templateForResponse(None, False, "Confirm your email first"), status=400)
        return Response(data=templateForResponse(None, False, "register first"), status=400)

    def put(self, request):
        if request.user.confirmed:
            data = request.data
            if not data.get("product_id"):
                return Response(data=templateForResponse(None, False, "product_id is required"), status=400)
            try:
                WishlistModel.objects.get(user=request.user, product_id=data.get("product_id")).delete()
                return Response(data=templateForResponse("product removed from wishlist", True))
            except:
                return Response(data=templateForResponse("this product was not found", True), status=400)
        return Response(data=templateForResponse(None, False, "Confirm your email first"), status=400)
