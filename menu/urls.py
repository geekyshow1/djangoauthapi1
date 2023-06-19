from rest_framework.routers import DefaultRouter
from .views import CartViewSet, MenuAPiView, CategoriesAPiView,CartItemViewSet,AddToCartViewSet
from django.urls import path

router = DefaultRouter()
router.register('food', MenuAPiView)
router.register('CartView', CartViewSet)
#router.register('CartItem', CartItemViewSet)
router.register('AddToCart', AddToCartViewSet)
router.register('category', CategoriesAPiView)
urlpatterns =router.urls 

#urlpatterns += router.urls
