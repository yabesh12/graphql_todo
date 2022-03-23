import graphene
from django.core.exceptions import ValidationError
from .models import Category, Book
from .schema import CategoryType, BookType


# Mutation
# Create Category
class CreateCategory(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        # id = graphene.ID()

    category = graphene.Field(CategoryType)
    message = graphene.String()

    @classmethod
    def mutate(cls, root, info, title):
        category = Category()
        category.title = title
        category.save()
        msg = "Category successfully created!"
        return CreateCategory(category=category, message=msg)


# Update Category
class UpdateCategory(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        id = graphene.ID()

    category = graphene.Field(CategoryType)
    message = graphene.String()

    @classmethod
    def mutate(cls, root, info, title, id):
        try:
            category = Category.objects.get(pk=id)
        except Category.DoesNotExist:
            raise ValidationError(message="Category does not exists", code=404)
        if category:
            category.title = title
            category.save()
        else:
            pass
        msg = "Category updated successfully!"
        return UpdateCategory(category=category, message=msg)


# Delete Category
class DeleteCategory(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, id):
        try:
            category = Category.objects.get(pk=id)
        except Category.DoesNotExist:
            raise ValidationError(message="Category does not exists", code=404)
        if category:
            category.delete()
        else:
            pass
        return None


# Create Book
class CreateBook(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        author = graphene.String(required=True)
        description = graphene.String()
        price = graphene.Int(required=True)

    book = graphene.Field(BookType)
    message = graphene.String()

    @classmethod
    def mutate(cls, root, info, title, author, price, description=None):
        book = Book()
        book.title = title
        book.author = author
        book.description = description
        book.price = price
        book.save()
        msg = "Book created Successfully!"
        return CreateBook(book=book, message=msg)


# Update Book
class UpdateBook(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        title = graphene.String(required=True)
        author = graphene.String(required=True)
        price = graphene.Int(required=True)
        description = graphene.String(required=False)

    book = graphene.Field(BookType)
    message = graphene.String()

    @classmethod
    def mutate(cls, root, info, id, title, author, price, description=None):
        try:
            book = Book.objects.get(id=id)
        except Book.DoesNotExist:
            raise ValidationError(message="Book does not exists", code=404)
        if book:
            book.title = title
            book.author = author
            book.price = price
            book.description = description
            book.save()
        else:
            pass
        msg = "Book successfully updated!"
        return UpdateBook(book=book, message=msg)


# Delete Book
class DeleteBook(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    book = graphene.Field(BookType)

    @classmethod
    def mutate(cls, root, info, id):
        try:
            book = Book.objects.get(pk=id)
        except Book.DoesNotExist:
            raise ValidationError(message="Book does not exists", code=404)
        book.delete()
        return None


class CoreMutation(graphene.ObjectType):
    create_category = CreateCategory.Field()
    update_category = UpdateCategory.Field()
    delete_category = DeleteCategory.Field()

    create_book = CreateBook.Field()
    update_book = UpdateBook.Field()
    delete_book = DeleteBook.Field()
