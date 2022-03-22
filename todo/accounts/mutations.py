import random
import graphene
from django.contrib.auth import get_user_model
from django.core.cache import cache, caches
from django.core.exceptions import ValidationError
from django.http import JsonResponse

from .schema import UserType

User = get_user_model()


class CreateUser(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        username = graphene.String()
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        mobile_no = graphene.String(required=True)
        password = graphene.String(required=True)
        city = graphene.String()

    user = graphene.Field(UserType)

    @classmethod
    def mutate(cls, root, info, email, first_name, last_name, mobile_no, password, **kwargs):
        user_obj = User.objects.create(email=email, first_name=first_name, last_name=last_name,
                                       mobile_no=mobile_no)
        user_obj.set_password(password)
        if username := kwargs.get('username'):
            user_obj.username = username
        if city := kwargs.get('city'):
            user_obj.city = city
        user_obj.save()
        return CreateUser(user=user_obj)


class LoginUser(graphene.Mutation):
    class Arguments:
        mobile_no = graphene.String(required=True)

    user = graphene.Field(UserType)

    @classmethod
    def mutate(cls, root, info, mobile_no):
        try:
            user_obj = User.objects.get(mobile_no=mobile_no)
        except User.DoesNotExist:
            raise ValidationError("Invalid user")
        if user_obj:
            cache_key = mobile_no
            print(cache_key)
            cache_time = 300
            data = cache.get(cache_key)
            print(data)

            if data is None:
                otp = random.randint(1000, 9999)
                m_cache = cache.set(cache_key, otp, cache_time)
                print(m_cache)
            elif data is not None:
                result = cache.get(cache_key)
                print(str(result) + ' ' + "result")
            else:
                print("no matching")
        else:
            pass


class VerifyUser(graphene.Mutation):
    class Arguments:
        mobile_no = graphene.String(required=True)
        otp = graphene.Int(required=True)

    user = graphene.Field(UserType)

    @classmethod
    def mutate(cls, root, info, mobile_no, otp):
        try:
            user_obj = User.objects.get(mobile_no=mobile_no)
        except User.DoesNotExist:
            raise ValidationError("Invalid user")

        if user_obj:
            data_otp = cache.get(mobile_no)
            if otp == data_otp:
                print("user verified")
            else:
                print("user not verified")
        else:
            pass


class UserMutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    login_user = LoginUser.Field()
    verify_user = VerifyUser.Field()
