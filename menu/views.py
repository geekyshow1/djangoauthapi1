from django.shortcuts import render

from rest_framework import status,viewsets,views,mixins
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from .serializers import Menu_ObjectSerializer, CartItemSerializer, CartSerializer, CategorySerializer,AddToCartSerializer
from .models import Menu_Object,Categories,Cart,Add_item_to_cart
from .filters import Foodfilter

from account.models import User

# Create your views here.
class MenuAPiView(viewsets.ModelViewSet):
    serializer_class = Menu_ObjectSerializer
    queryset=  Menu_Object.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = Foodfilter
    
class CategoriesAPiView(viewsets.ModelViewSet):
    serializer_class =CategorySerializer
    queryset=  Categories.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']    
    
'''class CartView(views.APIView):

    def post(self, request):
        serializer = CartSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = Add_item_to_cart.objects.all()
    serializer_class = CartItemSerializer

from rest_framework.permissions import IsAuthenticated

class CartViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated] # Add this line

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class AddToCartViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Add_item_to_cart.objects.all()
    serializer_class = AddToCartSerializer