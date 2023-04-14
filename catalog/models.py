from cgi import print_exception
from sys import _clear_type_cache
from unicodedata import name
from django.db import models
from django.forms import ValidationError
from django.urls import reverse_lazy
from catalog.choices import CarTypes
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group

# Create your models here.


class Brand(models.Model):
    brand_name = models.CharField(max_length=20)
    car_type = models.CharField(
        'type', max_length=20, choices=CarTypes.choices)
    tank_volume = models.PositiveSmallIntegerField()
    load_capacity = models.PositiveSmallIntegerField()
    places = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.brand_name


class Enterprise(models.Model):
    title = models.CharField(max_length=45)
    city = models.CharField(max_length=25)
    email = models.EmailField(max_length=25, null=True)

    def __str__(self):
        return self.title


class Vehicles(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    enterprise = models.ForeignKey(
        Enterprise, on_delete=models.CASCADE, default=None, null=True, blank=True, related_name='vehicle_enterprice')
    vin_number = models.CharField(max_length=20, null=True)
    reg_number = models.CharField(max_length=20, null=True)
    model = models.CharField(max_length=20, null=True)
    price = models.DecimalField(max_digits=19, decimal_places=2)
    year = models.PositiveSmallIntegerField()
    mileage = models.PositiveIntegerField()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__enterprise = self.enterprise

    def clean_fields(self, exclude) -> None:
        super().clean_fields(exclude)
        if (self.enterprise != self.__enterprise) and (self.__enterprise is not None):
            if self.has_active_driver():
                raise ValidationError("Есть активный водитель")

    def has_active_driver(self):
        return self.drivers.filter(is_active=True).exists()
    

    def __str__(self):
        return self.reg_number

    def get_absolute_url(self):
        return reverse_lazy('car-detail', args=[str(self.id)])


class Driver(models.Model):
    name = models.CharField(max_length=40, null=True)
    category = models.CharField(max_length=20)
    enterprise = models.ForeignKey(
        Enterprise, on_delete=models.CASCADE, default=None, null=True, blank=True, related_name='driver_enterprise')
    is_active = models.BooleanField(default=False)
    vehicle = models.ForeignKey(
        Vehicles, on_delete=models.CASCADE, default=None, null=True, blank=True, related_name='drivers')

    #Проверка активен ли водитель
    def check_active_car(self):
        if self.vehicle is None:
            raise ValidationError("Нет привязки к машине")
        if self.vehicle.has_active_driver():
            raise ValidationError("Есть активный водитель")

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__is_active = self.is_active
        self.__vehicle = self.vehicle

    def clean_fields(self, exclude) -> None:
        super().clean_fields(exclude)
        if self.is_active != self.__is_active and self.is_active:
            self.check_active_car()
        if self.is_active and self.vehicle != self.__vehicle:
            raise ValidationError("Активный водитель не может сменить машину")
        

    def __str__(self):
        return self.category

class Managers(User):
    enterprise = models.ManyToManyField(Enterprise, related_name='manager_enterprise')

    def enterprises_titles(self):
        return u" %s" % (u", ".join([enterprise.title for enterprise in self.enterprise.all()]))
    enterprises_titles.short_description=u'Enterprise'


    

    class Meta:
        verbose_name = 'Manager'
        verbose_name_plural = 'Managers'

