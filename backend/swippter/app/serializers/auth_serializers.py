from rest_framework import serializers as rest_serializers
from app.models.user import User, RoleEnum
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(rest_serializers.ModelSerializer):

    role = rest_serializers.ChoiceField(
        choices=RoleEnum,
    )
    token = rest_serializers.SerializerMethodField("get_token")

    class Meta:
        model = User
        fields = [
            "uuid",
            "first_name",
            "last_name",
            "email",
            "role",
            "token",
        ]

    def get_token(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
