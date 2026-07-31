from django.contrib import admin
from django.urls import path

from menu import views

admin.site.site_header = 'إدارة مطعم Dinear'
admin.site.site_title = 'Dinear Admin'
admin.site.index_title = 'لوحة الإدارة'

urlpatterns = [
    path('', views.menu_view, name='menu'),
    path('api/place-order/', views.place_order, name='place_order'),
    path('dashboard/login/', views.dashboard_login, name='dashboard_login'),
    path('dashboard/logout/', views.dashboard_logout, name='dashboard_logout'),
    path('dashboard/orders/', views.dashboard_orders, name='dashboard_orders'),
    path(
        'dashboard/orders/<int:order_id>/status/',
        views.update_order_status,
        name='update_order_status',
    ),
    path('admin/', admin.site.urls),
]
