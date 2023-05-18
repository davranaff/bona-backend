from django.contrib.auth.hashers import make_password, check_password
from rest_framework.authtoken.views import *
from rest_framework.decorators import api_view
from rest_framework.response import Response

from app.models import Order, OrderProduct
from app.serializers.order import OrderSerializer, OrderProductSerializer
from app.views import templateForResponse
from users.models import User, Email
from users.serializers.user import UserSerializer
from users.utils.generateEmailCode import generateEmailCode
from users.utils.sendCode import sendCode


# Create your views here.


@api_view(["POST"])
def register(request):
    data = request.data
    if not data.get("email"):
        return Response(data=templateForResponse(None, False, "email is required"), status=400)
    if not data.get("password"):
        return Response(data=templateForResponse(None, False, "password is required"), status=400)
    if not data.get("name"):
        return Response(data=templateForResponse(None, False, "name is required"), status=400)
    if not data.get("telephone"):
        return Response(data=templateForResponse(None, False, "telephone is required"), status=400)
    hashed = make_password(data.get("password"))
    try:
        email = Email.objects.create(
            email=data.get("email"),
            code=generateEmailCode()
        )
        user = User.objects.create(
            username=data.get("name"),
            password=hashed,
            custom_email=email,
            telephone=data.get("telephone")
        )
        token = Token.objects.create(user_id=user.id)
        sendCode(email.email, email.code)
        serializer = UserSerializer(user, many=False)
        return Response(data=templateForResponse({ "user": serializer.data, "token": token.key }, True))
    except:
        return Response(data=templateForResponse(None, False, "email or username already exist"), status=400)


@api_view(["POST"])
def verifyCode(request):
    data = request.data
    if not data.get('code'):
        return Response(data=templateForResponse(None, False, "code required"), status=400)
    token = Token.objects.get(key=request.auth)
    user = User.objects.get(pk=token.user_id)
    if int(data.get('code')) != user.custom_email.code:
        return Response(data=templateForResponse(None, False, "invalid Code"), status=400)
    user.confirmed = True
    user.save()
    return Response(data=templateForResponse("your email confirmed", True))


@api_view(["POST"])
def login(request):
    data = request.data
    if not data.get("email") and not data.get("password"):
        return Response(data=templateForResponse(None, False, "email and password required"), status=400)
    try:
        user = User.objects.select_related("custom_email").get(custom_email__email=data.get("email"))
    except:
        return Response(data=templateForResponse(None, False, "email or password is not correct"), status=400)
    check = check_password(data.get("password"), user.password)
    if check:
        Token.objects.update(key=Token.generate_key())
        token = Token.objects.get(user_id=user.pk)
        return Response(data=templateForResponse(token.key, True))
    return Response(data=templateForResponse(None, False, "email or password is not correct"), status=400)


@api_view(["PUT", "POST"])
def reset_password(request):
    if request.method == "POST":
        data = request.data
        if not data.get("password"):
            return Response(data=templateForResponse(None, False, "password is required"), status=400)
        if not data.get("email_code"):
            return Response(data=templateForResponse(None, False, "email_code is required"), status=400)
        try:
            email = Email.objects.get(code=int(data.get("email_code")))
            user = email.user_email.get(custom_email=email)
            user.password = make_password(data.get("password"))
            user.save()
            return Response(data=templateForResponse("password updated", True))
        except:
            return Response(data=templateForResponse(None, False, "email code invalid"), status=400)
    if request.method == "PUT":
        data = request.data
        if not data.get("old_password"):
            return Response(data=templateForResponse(None, False, "old_password is required"), status=400)
        if not data.get("new_password"):
            return Response(data=templateForResponse(None, False, "new_password is required"), status=400)
        check = check_password(data.get("old_password"), request.user.password)
        if not check:
            return Response(data=templateForResponse(None, False, "Password mismatch"), status=400)
        user = User.objects.get(pk=request.user.pk)
        user.password = make_password(data.get("new_password"))
        user.save()
        return Response(data=templateForResponse("password updated", True))


@api_view(["POST"])
def reset_password_with_email(request):
    data = request.data
    if not data.get("email"):
        return Response(data=templateForResponse(None, False, "email is required"), status=400)
    try:
        email = Email.objects.get(email=data.get("email"))
        code = generateEmailCode()
        email.code = code
        email.save()
        sendCode(email.email, code)
        return Response(data=templateForResponse("code sending", True), status=200)
    except:
        return Response(data=templateForResponse(None, False, "user with this mail does not exist"), status=400)


@api_view(["GET"])
def profile(request):
    user = User.objects.get(pk=request.user.pk)
    order = Order.objects.filter(user=request.user, buy=True).prefetch_related("order_product_order")
    serializerOrder = OrderSerializer(order, many=True)
    serializer = UserSerializer(user, many=False)
    return Response(data=templateForResponse({
        "user": serializer.data,
        "order": serializerOrder.data,
    }, True))
