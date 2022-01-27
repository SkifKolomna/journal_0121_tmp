from django.contrib import admin

from .models import Chart


# Register your models here.
# admin.site.register(Task)
# @admin.register(Task)

# admin.site.register(Category)

# admin.site.register(Subdivision)

# admin.site.register(Address)

# admin.site.register(Resource)

# admin.site.register(Act)

# admin.site.register(Chart)
@admin.register(Chart)
class ChartAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_on')

# @admin.register(Address)
# class AddressAdmin(admin.ModelAdmin):
#     list_display = ('id', 'string_address', 'string_subdivision', 'is_active')
#     search_fields = ('id', 'string_address')
#     list_filter = ('id', 'string_address')
