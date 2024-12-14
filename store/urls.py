from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.store, name='store'),
    path('cloth/<int:id>/', views.store_details, name='store_details'),
    path('cart/', views.cart, name='cart'),
    path('product/<int:id>/', views.view, name='product/<product_id>/'),
    path('process_order/', views.processOrder, name='process_order'),
    path('update_item/', views.updateItem, name='update_item'),
    path('contact-us/', views.contact, name='contact-us'),
    path('checkout/', views.checkout, name='checkout'),
    path('register/', views.register, name='register'),
    path('orders/', views.order_list_view, name='orders'),
    path('deliveries/', views.all_deliveries, name='all_deliveries'),
    path('my-deliveries/', views.user_delivery_status, name='user_delivery_status'),
    path('orders/confirm/<int:order_id>/', views.confirm_order_completion, name='confirm-order'),
    path('reset_password/',
    auth_views.PasswordResetView.as_view(template_name='store/reset_password.html', html_email_template_name = 'store/email_template.html'),
    name ='reset_password'),
    path('reset_password_sent/',
    auth_views.PasswordResetDoneView.as_view(template_name='store/reset_password_sent.html'), 
    name ='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
    auth_views.PasswordResetConfirmView.as_view(template_name='store/reset_password_confirm.html'),
    name ='password_reset_confirm'),
    path('reset_password_complete/',
    auth_views.PasswordResetCompleteView.as_view(template_name='store/reset_password_complete.html'),
    name ='password_reset_complete'),
    path('login/', auth_views.LoginView.as_view(template_name='store/login.html'), name ='login' ),
    path('logout/', views.logout_view, name ='logout'),

    path('driver-signup/', views.driver_signup, name='driver_signup'),
    path('driver-login/', views.driver_login, name='driver_login'),
    path('add-product/', views.add_product, name='add_product'),
]
