from django.urls import path, includeurlpatterns = [    path('shop/', include("api.v1.shop.urls"))]