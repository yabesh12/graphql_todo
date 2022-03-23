from django.contrib.auth import get_user_model
from graphene import String

from .models import CustomUser
import graphene
from graphene_django import DjangoObjectType


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        fields = ('id', 'first_name', 'last_name', 'email', 'mobile_no', 'username', 'city')


class UserQuery(graphene.ObjectType):
    users = graphene.List(UserType)
    # me = graphene.Field(UserType)

    def resolve_users(root, info, **kwargs):
        return CustomUser.objects.all()

    # def resolve_me(self,info):
    #     user = info.context.user
    #     if user.is_anonymous:
    #         raise Exception("Authentication Failure!")
    #     return user
