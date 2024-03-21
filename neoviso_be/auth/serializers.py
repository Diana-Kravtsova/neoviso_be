from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        groups = user.groups.all()
        group_names = [group.name for group in groups]
        token['roles'] = group_names
        token['username'] = user.username

        return token