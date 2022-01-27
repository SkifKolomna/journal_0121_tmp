from django.contrib import admin

from .models import Task, Address, Resource, Act, Subdivision, Category, Profile

''' 
https://russianblogs.com/article/32121447496/
'''


# Register your models here.
# admin.site.register(Task)
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__', 'created_on', 'created_by')


# admin.site.site_header = '123'
# admin.site.site_title = '123'
# admin.site.index_title = '123'


admin.site.register(Category)

# admin.site.register(Subdivision)


# admin.site.register(Address)

admin.site.register(Resource)

admin.site.register(Act)


# admin.site.register(Chart)

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'string_address', 'string_subdivision', 'is_active')
    search_fields = ('id', 'string_address')
    # list_filter = ('id', 'string_address')@admin.register(Address)


@admin.register(Subdivision)
class SubdivisionAdmin(admin.ModelAdmin):
    list_display = ('id', 'string_subdivision', 'is_active')
    search_fields = ('id', 'string_address')
    # list_filter = ('id', 'string_address')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'patronymic', 'full_name', 'short_name', 'subdivision', 'is_operator')
    search_fields = ('id', 'patronymic', 'string_address')
    # list_filter = ('id', 'string_address')
