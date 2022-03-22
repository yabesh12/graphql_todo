import graphene
from graphene_django import DjangoObjectType
from .models import Category, Book


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ('id', 'title')


class BookType(DjangoObjectType):
    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'price', 'description')


class CoreQuery(graphene.ObjectType):
    categories = graphene.List(CategoryType)
    books = graphene.List(BookType)
    category = graphene.Field(CategoryType, category_id=graphene.ID())
    category_title = graphene.Field(CategoryType, category_title=graphene.String())
    book = graphene.Field(BookType, book_id=graphene.ID())
    book_title = graphene.Field(BookType, book_title=graphene.String())

    def resolve_categories(root, info, **kwargs):
        return Category.objects.all()

    def resolve_books(root, info, **kwargs):
        return Book.objects.all()

    def resolve_category(self, info, category_id):
        return Category.objects.get(pk=category_id)

    def resolve_category_title(self, info, category_title):
        return Category.objects.get(title__iexact=category_title)

    def resolve_book(self, info, book_id):
        return Book.objects.get(pk=book_id)

    def resolve_book_title(self, info, book_title):
        return Book.objects.get(title__iexact=book_title)


