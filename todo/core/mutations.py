import graphene

from .models import Category, Book
from .schema import CategoryType, BookType, CoreQuery


# Mutation
# Create Category
class CreateCategory(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        # id = graphene.ID()

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, title):
        category = Category()
        category.title = title
        category.save()
        return CreateCategory(category=category)


# Update Category
class UpdateCategory(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        id = graphene.ID()

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, title, id):
        category = Category.objects.get(pk=id)
        category.title = title
        category.save()
        return UpdateCategory(category=category)


# Delete Category
class DeleteCategory(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, id):
        category = Category.objects.get(pk=id)
        category.delete()
        return None


# Create Book
class CreateBook(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        author = graphene.String(required=True)
        description = graphene.String()
        price = graphene.Int(required=True)

    book = graphene.Field(BookType)

    @classmethod
    def mutate(cls, root, info, title, author, price, description=None):
        book = Book()
        book.title = title
        book.author = author
        book.description = description
        book.price = price
        book.save()

        return CreateBook(book=book)


# Update Book
class UpdateBook(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        title = graphene.String(required=True)
        author = graphene.String(required=True)
        price = graphene.Int(required=True)
        description = graphene.String(required=False)

    book = graphene.Field(BookType)

    @classmethod
    def mutate(cls, root, info, id, title, author, price, description=None):
        book = Book.objects.get(id=id)
        book.title = title
        book.author = author
        book.price = price
        book.description = description
        book.save()

        return UpdateBook(book=book)


# Delete Book
class DeleteBook(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    book = graphene.Field(BookType)

    @classmethod
    def mutate(cls, root, info, id):
        book = Book.objects.get(pk=id)
        book.delete()
        return None


class CoreMutation(graphene.ObjectType):
    create_category = CreateCategory.Field()
    update_category = UpdateCategory.Field()
    delete_category = DeleteCategory.Field()

    create_book = CreateBook.Field()
    update_book = UpdateBook.Field()
    delete_book = DeleteBook.Field()
