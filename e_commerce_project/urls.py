from django.contrib import admin
from django.urls import path,include
import e_commerce_app.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ecommerce/',include(e_commerce_app.urls))
]
