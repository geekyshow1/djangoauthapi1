from rest_framework import serializers
from .models import Menu_Object, Categories, Cart, Add_item_to_cart

class Menu_ObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu_Object
        fields = [ 'food_name', 'food_image', 'price', 'description', 'is_avilable']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'

class AddToCartSerializer(serializers.ModelSerializer):
    sub_total = serializers.ReadOnlyField()
    food = Menu_ObjectSerializer(many =True)
 
    class Meta:
        model = Add_item_to_cart
        fields = ['food', 'quantity', 'sub_total']

    def get_sub_total(self, obj):
        return obj.quantity * obj.food.price

class CartItemSerializer(serializers.ModelSerializer):
    food = Menu_ObjectSerializer()
    
    class Meta:
        model = Add_item_to_cart
        fields = [ 'food', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['cart_id', 'created_at', 'items']

    def create(self, validated_data):
        cart_items_data = validated_data.pop('items')
        cart = Cart.objects.create(user=self.context['request'].user, **validated_data)
        cart_items = []
        for item_data in cart_items_data:
            item = Add_item_to_cart.objects.create(cart=cart, **item_data)
            cart_items.append(item)
        cart.items.set(cart_items)
        return cart
