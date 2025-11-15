from django.urls import path
from .views import add_product, add_reply, add_review, admin_login_view, delete_product, delete_product_list, dislike_review, edit_product, edit_product_list, google_oauth_login, landing_page, like_review, logout_view, product_detail, signup_view, login_view, toggle_like, user_dashboard, admin_dashboard, view_reviews
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', landing_page, name='landing'),
    path('login', login_view, name='login'),
    path('admin_login/', admin_login_view, name='admin_login'),
    path('signup/', signup_view, name='signup'),
    path('dashboard/user/', user_dashboard, name='user_dashboard'),
    path('dashboard/admin/', admin_dashboard, name='admin_dashboard'),
    path('add-product/', add_product, name='add_product'),
    path('edit-products/', edit_product_list, name='edit_product_list'),
    path('delete-products/', delete_product_list, name='delete_product_list'),
    path('product/edit/<int:product_id>/', edit_product, name='edit_product'), 
    path('product/delete/<int:product_id>/', delete_product, name='delete_product'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('product/<int:product_id>/review/', add_review, name='add_review'),
    path('reviews/<int:review_id>/like/', toggle_like, name='toggle_like'),
    path('reviews/<int:review_id>/reply/', add_reply, name='add_reply'),
    path('products/<int:product_id>/reviews/',view_reviews, name='view_reviews'),
    path('review/<int:review_id>/like/',like_review, name='like_review'),
    path('review/<int:review_id>/dislike/', dislike_review, name='dislike_review'),
    path('logout/', logout_view, name='logout'),
    path('google-oauth-login/', google_oauth_login, name='google_oauth_login'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)