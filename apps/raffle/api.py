# Third Party Stuff
# Standard Library
from random import randint

from django.db.models import Count
from django.utils.translation import gettext_lazy as _
from rest_framework.views import APIView

# Talana Stuff
from apps.base import response
from apps.users.models import User
from apps.users.serializers import UserSerializer


class GetWinner(APIView):
    def get(self, request):
        if not request.user.is_superuser:
            return response.Unauthorized()

        users = User.objects.filter(is_verified=True)
        if users:
            count = users.aggregate(count=Count("id"))["count"]
            random_index = randint(0, count - 1)
            serializer = UserSerializer(users[random_index])
            return response.Ok(serializer.data)
        return response.NotFound(_("There are not users with an email confirmed"))
