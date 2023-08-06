from django.contrib import admin
from .models import CarMake, CarModel, CarDealer, DealerReview


# Register your models here.

# CarModelInline class

# CarModelAdmin class

# CarMakeAdmin class with CarModelInline

# Register models here
# Register CarMake model with the admin site
# CarModelInline class
class CarModelInline(admin.StackedInline):  # You can also use admin.StackedInline for a different display style
    model = CarModel
    extra = 1  # Number of empty forms to display for adding related CarModel instances

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    inlines = [CarModelInline]  # Include the CarModelInline to display related CarModel instances

# Register CarModel model with the admin site
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'year', 'make', 'dealer_id')
    list_filter = ('type', 'year', 'make')
    search_fields = ('name', 'type', 'year', 'make__name')


admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(CarDealer)
admin.site.register(DealerReview)