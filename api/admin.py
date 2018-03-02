from django.contrib import admin
from api import models
# Register your models here.


admin.site.register(models.ArticleSource)
admin.site.register(models.Article)
admin.site.register(models.Collection)
admin.site.register(models.Comment)
admin.site.register(models.Course)