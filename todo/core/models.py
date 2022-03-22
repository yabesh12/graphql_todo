from django.db import models


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id) + '  ' + str(self.title)


class Book(models.Model):
    # book = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    price = models.PositiveIntegerField()
    description = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)
