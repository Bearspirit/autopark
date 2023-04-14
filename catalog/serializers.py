from rest_framework import serializers
from .models import Managers, Vehicles, Enterprise

class ManagerSerializer(serializers.ModelSerializer):
    #enterprise = serializers.StringRelatedField(many=True)
    available_vehicles = serializers.SerializerMethodField() #получаем ИД связанных автомобилей с помощью функции, определенной ниже
    available_enterprises = serializers.SerializerMethodField()

    def get_available_vehicles(self, manager):
        return list(manager.enterprise.all().values_list('vehicle_enterprice__id', flat=True))
    
    def get_available_enterprises(self, manager):
        return list(manager.enterprise.all().values_list('id', flat=True))

    class Meta:
        model = Managers
        fields = ('id', 'username', 'available_enterprises', 'available_vehicles')


class VehiclesSerializer(serializers.ModelSerializer):
    #brand_name = serializers.SerializerMethodField() #для вывода нименования бренда, с помощью функции get_brand_name
    available_managers = serializers.SerializerMethodField()
    available_enterprises = serializers.SerializerMethodField()
    car_type = serializers.SerializerMethodField()

    def get_car_type(self, vehicles):
        return vehicles.brand.get_car_type_display()

    #def get_brand_name(self, vehicle):
        #return vehicle.brand.brand_name

    def get_available_managers(self, vehicles):
        return list(vehicles.enterprise.manager_enterprise.values_list('id', flat=True))
    
    def get_available_enterprises(self, vehicles):
        return vehicles.enterprise_id

    class Meta:
        model = Vehicles
        fields = ('id', 'brand', 'car_type', 'vin_number', 'reg_number', 'model', 'available_enterprises', 'available_managers')


class EnterpriseSerializer(serializers.ModelSerializer):
    available_managers = serializers.SerializerMethodField()
    available_vehicles = serializers.SerializerMethodField()

    def get_available_managers(self, enterprise):
        return list(enterprise.manager_enterprise.all().values_list('id', flat=True))
    
    def get_available_vehicles(self, enterprise):
        return list(enterprise.vehicle_enterprice.all().values_list('id', flat=True))

    class Meta:
        model = Enterprise
        fields = ('id', 'title', 'city', 'email', 'available_vehicles', 'available_managers')