from django.db import models
import uuid
from account.models import User
# Create your models here.

FOOD_CATEGORY =(
    ('Break_fast','break_fast'),
    ('Lunch','lunch'),
    ('Super','super')
)


       
class Menu_Object(models.Model):
    food_id = models.UUIDField(default=uuid.uuid4, primary_key= True , auto_created=True, editable=True)
    food_name = models.CharField(max_length=244)
    food_image = models.ImageField( upload_to="img",blank=True,null=True)
    price = models.FloatField(default= 100.00)
    description = models.TextField()
    is_avilable = models.BooleanField(default=True)

    def __str__(self):
        return self.food_name
    
    
class Categories(models.Model):
    cartegory_id = models.UUIDField(default=uuid.uuid4 ,primary_key=True,editable=False,auto_created=True)
    category = models.CharField(max_length=20, choices=FOOD_CATEGORY)
    food = models.ForeignKey(Menu_Object, verbose_name=("food"), on_delete=models.CASCADE) 
    
    def __str__(self):
        return self.category   
    
    
class Cart(models.Model):
    cart_id =models.UUIDField(default=uuid.uuid4, primary_key= True , auto_created=True, editable=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.food_name
    
class Add_item_to_cart(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items", null=True, blank=True)
    food = models.ForeignKey(Menu_Object, on_delete=models.CASCADE, blank=True, null=True, related_name='cartitems')
    quantity = models.PositiveSmallIntegerField(default=0)
    
    def __str__(self):
        return self.food_name
   