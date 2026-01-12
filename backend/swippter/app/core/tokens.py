from rest_framework_simplejwt.tokens import RefreshToken
from app.utils.utilities import F

class VersionOneRefreshToken(RefreshToken):

    @classmethod
    def for_user(cls, user):
        token = super().for_user(user)
        token[F.V1] = F.V1
        return token