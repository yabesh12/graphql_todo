import graphene

# Query for getting the data from the server.
import graphql_jwt
from accounts.mutations import UserMutation
from accounts.schema import UserQuery
from core.schema import CoreQuery
from core.mutations import CoreMutation


# Query receive responses from server
class Query(UserQuery, CoreQuery, graphene.ObjectType):
    pass


# Mutation for sending the data to the server.
class Mutation(CoreMutation, UserMutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


# Create schema
schema = graphene.Schema(query=Query, mutation=Mutation)
