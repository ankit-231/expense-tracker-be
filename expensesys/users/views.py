from django.shortcuts import render
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import exceptions
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import User
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
        print(data)

        # Add your extra responses here
        data["username"] = self.user.username
        data["role"] = self.user.role
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class GetUserMeDetail(APIView):
    permission_classes = (IsAuthenticated,)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = (
                "id",
                "username",
            )

    def get(self, request):
        user = request.user
        user_data = self.OutputSerializer(user)
        data_ = user_data.data
        message = "success"
        status_code = status.HTTP_200_OK
        res = {"data": data_, "message": message, "status": status_code}
        return Response(res, status=status_code)
