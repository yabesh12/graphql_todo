import random
import graphene
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.exceptions import ValidationError
from graphql_jwt.shortcuts import get_token
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

    message = graphene.String()
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
        message = "User created Successfully!"
        return CreateUser(user=user_obj, message=message)


class LoginUser(graphene.Mutation):
    class Arguments:
        mobile_no = graphene.String(required=True)

    user = graphene.Field(UserType)

    @classmethod
    def mutate(cls, root, info, mobile_no):
        try:
            user_obj = User.objects.filter(mobile_no=mobile_no).first()
        except User.DoesNotExist:
            raise ValidationError("Invalid user")
        if user_obj:
            token = get_token(user_obj)
            print(token)
            cache_key = mobile_no
            cache_time = 300  # 5 minutes
            data = cache.get(cache_key)

            if data is None:
                otp = random.randint(1000, 9999)
                cache.set(cache_key, otp, cache_time)
                cache_data = cache.get(cache_key)
                print(cache_data)

            elif data is not None:
                cache.get(cache_key)
            else:
                raise ValidationError("Otp not found!")
        else:
            pass
        return LoginUser(user=user_obj)


class VerifyUser(graphene.Mutation):
    class Arguments:
        mobile_no = graphene.String(required=True)
        otp = graphene.Int(required=True)
        token = graphene.String(required=True)

    user = graphene.Field(UserType)
    message = graphene.String()

    @classmethod
    def mutate(cls, root, info, mobile_no, otp, token):
        try:
            user_obj = User.objects.filter(mobile_no=mobile_no).first()
        except User.DoesNotExist:
            raise ValidationError("Invalid user")

        if user_obj:
            data_otp = cache.get(mobile_no)
            token = token
            if otp == data_otp and token == token:
                msg = "user verified"
                return VerifyUser(user=user_obj, message=msg)
            elif otp == data_otp and token != token:
                raise ValidationError("Token is not matching")
            else:
                raise ValidationError("Otp is not matching")
        else:
            pass
        return VerifyUser(user=user_obj)


class UserMutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    login_user = LoginUser.Field()
    verify_user = VerifyUser.Field()
