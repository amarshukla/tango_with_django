from django.contrib import admin
from rango.models import Page, Category
from rango.models import UserProfile


class PageInline(admin.StackedInline):
    model = Page
    extra = 3

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url','views')

class CategoryAdmin(admin.ModelAdmin):
	prepopulated_fields={'slug':('name',)}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile)