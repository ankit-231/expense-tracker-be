from django.shortcuts import render
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import exceptions
from rest_framework_simplejwt.views import TokenObtainPairView
from utilities.model_utilities.users import UserUtil
from utilities.base_api_views import AuthenticatedAPIView, PublicAPIView
from utilities.response_wrappers import OKResponse
from users.models import Budget, User
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework import serializers


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # note: you can only access self.user after calling super().validate(attrs)
        # print(self.user)
        if self.user.is_deleted:
            raise exceptions.AuthenticationFailed(
                self.error_messages["no_active_account"],
                "no_active_account",
            )

        # Add your extra responses here
        data["username"] = self.user.username
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class GetUserMeDetail(AuthenticatedAPIView):

    class OutputSerializer(serializers.ModelSerializer):
        currency = serializers.SerializerMethodField()

        class Meta:
            model = User
            fields = (
                "id",
                "username",
                "currency",
            )

        def get_currency(self, user):
            return user.currency.symbol

    def get(self, request):
        user = request.user
        user_data = self.OutputSerializer(user)
        data_ = user_data.data
        message = "success"
        status_code = status.HTTP_200_OK
        res = {"data": data_, "message": message, "status": status_code}
        return Response(res, status=status_code)


class CreateUserAPI(PublicAPIView):

    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ("username", "email", "password", "currency")

    def post(self, request):
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        input_serializer.save()
        return OKResponse(message="User created successfully")


class ChangePasswordAPI(AuthenticatedAPIView):

    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ("password",)

    def post(self, request):
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        user = request.user
        user.set_password(input_serializer.data["password"])
        user.save()
        return OKResponse(message="Password changed successfully")


class EditUserAPI(AuthenticatedAPIView):

    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ("email", "currency")

    def post(self, request):
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        input_serializer.save()
        return OKResponse(message="User updated successfully")


class DeleteUserAPI(AuthenticatedAPIView):

    def post(self, request):
        user = request.user
        user.is_deleted = True
        user.save()
        return OKResponse(message="User deleted successfully")


class GetUserDetailAPI(AuthenticatedAPIView):

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ["id", "username", "email", "currency"]

    def get(self, request):
        user = request.user
        output_serializer = self.OutputSerializer(user)
        return OKResponse(data=output_serializer.data)


class CreateBudgetAPI(AuthenticatedAPIView):

    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Budget
            fields = ["name", "amount", "is_enabled", "time_frame", "user"]

    def post(self, request):
        user = request.user
        data = request.data
        data.update({"user": user.id})
        input_serializer = self.InputSerializer(data=data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)
        input_serializer.save()


class GetFinancialDetailAPI(AuthenticatedAPIView):

    class OutputSerializer(serializers.Serializer):
        balance = serializers.FloatField()

    def get(self, request):
        user = request.user
        user_ = UserUtil(user)
        balance = user_.get_remaining_balance()
        data = {"balance": balance}
        output_serializer = self.OutputSerializer(data)
        return OKResponse(data=output_serializer.data)
