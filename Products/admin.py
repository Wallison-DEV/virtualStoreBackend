from django.contrib import admin
from .models import CategoryModel, ProductModel, ProductLineModel

admin.site.register(ProductModel)
admin.site.register(CategoryModel)
admin.site.register(ProductLineModel)

