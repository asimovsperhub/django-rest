from django.contrib import admin

# Register your models here.
from index.models import Blog


class BlogAdmin(admin.ModelAdmin):
    #fields = ('title', 'tag', 'body')
    list_display = ('title', 'tag', 'body')
    #list_filter = ('author', admin.RelatedOnlyFieldListFilter)


admin.site.register(Blog, BlogAdmin)
