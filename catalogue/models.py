from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=10, default='')
    def __str__(self):
        return self.name

class Box(models.Model):
    name = models.CharField(max_length = 50)
    def __str__(self):
        return self.name


class Item(models.Model):

    # category = models.CharField(max_length = 20, null = True)
    category = models.ManyToManyField(Category, null=True)
    contents = models.CharField(max_length = 3000)
    folder = models.CharField(max_length = 20, null = True)
    box = models.ForeignKey('Box', on_delete = models.SET_NULL, null = True)
    start_year = models.PositiveSmallIntegerField(null = True, default = None)
    end_year = models.PositiveSmallIntegerField(null = True, default = None)
    last_moved = models.DateField(null = True, default = None)





# class Category(models.Model):
#
#
#
#     name = models.CharField(max_length = 50, choices = CATEGORY)
#     items = models.ManyToManyField('Item', through = 'ItemCat')
#
#     def __str__(self):
#         return self.name
#
# class ItemCat(models.Model):
#     item = models.ForeignKey(Item, on_delete = models.CASCADE)
#     category = models.ForeignKey(Category, on_delete = models.CASCADE)
