from rest_framework import serializers as rest_serializers
from app.models.user import User, RoleEnum
from app.core.tokens import VersionOneRefreshToken
from app.utils.utilities import F

class UserSerializer(rest_serializers.ModelSerializer):

    role = rest_serializers.ChoiceField(
        choices=RoleEnum,
    )
    token = rest_serializers.SerializerMethodField(F.GET_TOKEN)

    class Meta:
        model = User
        fields = [
            F.UUID,
            F.FIRST_NAME,
            F.LAST_NAME,
            F.EMAIL,
            F.ROLE,
            F.TOKEN,
        ]

    def get_token(self, instance):
        refresh = VersionOneRefreshToken.for_user(instance)
        return {
            F.REFRESH: str(refresh),
            F.ACCESS: str(refresh.access_token),
        }


class ForgotSerializer(rest_serializers.ModelSerializer):

    token = rest_serializers.SerializerMethodField(F.GET_TOKEN)

    class Meta:
        model = User
        fields = [
            F.TOKEN,
        ]

    def get_token(self, instance):
        refresh = VersionOneRefreshToken.for_user(instance)
        return {
            F.REFRESH: str(refresh),
            F.ACCESS: str(refresh.access_token),
        }
