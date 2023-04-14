from django.db import models

class CarTypes(models.TextChoices):
    LITE = 'LITE', 'Легковой'
    TRUCK = 'TRUCK', 'Грузовой'
    BUS = 'BUS', 'Автобус'