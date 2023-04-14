from django.contrib import admin
from .models import Brand, Vehicles, Enterprise, Driver, Managers
    

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('brand_name', 'car_type', 'load_capacity', 'places')

@admin.register(Vehicles)
class VehiclesAdmin(admin.ModelAdmin):
    list_display = ('reg_number', 'vin_number', 'enterprise', 'brand')
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        enterprises = request.user.managers.enterprise.all()
        if enterprises.exists():
            qs = qs.filter(enterprise__in=enterprises)
        return qs



@admin.register(Enterprise)
class EnterpriseAdmin(admin.ModelAdmin):
    list_display = ('title', 'city', 'email')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            # Если пользователь является администратором, показать все предприятия
            return qs
        # Иначе, показать только предприятия, связанные с текущим менеджером
        return qs.filter(manager_enterprise=request.user)


            
@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_active', 'vehicle', 'enterprise')
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        enterprises = request.user.managers.enterprise.all()
        if enterprises.exists():
            qs = qs.filter(enterprise__in=enterprises)
        return qs

    

@admin.register(Managers)
class ManagersAdmin(admin.ModelAdmin):
    list_display = ('username', 'enterprises_titles',)
    def get_enterprises(self, request):
        return request.user.enterprises.all()


#admin.site.register(Brand)
#admin.site.register(Vehicles)
#admin.site.register(Enterprise)
#admin.site.register(Driver)

# Register your models here.
