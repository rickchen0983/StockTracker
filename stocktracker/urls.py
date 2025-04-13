from django.contrib import admin
from django.urls import path
from stocks import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('stock/', views.home, name='home'),
    path('api/stock_data/', views.get_stock_data, name='get_stock_data'),  # API 路徑
]
