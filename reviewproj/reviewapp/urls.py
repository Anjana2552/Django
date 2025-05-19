from django.urls import path
from .views import add_product, delete_product, delete_product_list, edit_product, edit_product_list, signup_view, login_view, logout_view, user_dashboard, admin_dashboard
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/user/', user_dashboard, name='user_dashboard'),
    path('dashboard/admin/', admin_dashboard, name='admin_dashboard'),
    path('add-product/', add_product, name='add_product'),
    path('edit-products/', edit_product_list, name='edit_product_list'),
    path('delete-products/', delete_product_list, name='delete_product_list'),
    path('admin/product/edit/<int:product_id>/', edit_product, name='edit_product'),
    path('admin/product/delete/<int:product_id>/', delete_product, name='delete_product'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)