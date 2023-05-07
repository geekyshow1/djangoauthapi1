from django_filters.rest_framework import FilterSet
from .models import Menu_Object

class Foodfilter(FilterSet):
    class Meta:
        model = Menu_Object
        fields = {
            'food_name':['exact'],
            'price':['gt','lt']
        }