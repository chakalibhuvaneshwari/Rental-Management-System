from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/toggle/<int:property_id>/', views.toggle_wishlist, name='toggle_wishlist'),
    path('messages/', views.messages_view, name='messages'),
    path('messages/send/<int:property_id>/', views.send_message, name='send_message'),
    path('messages/thread/<int:user_id>/', views.message_thread, name='message_thread'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
