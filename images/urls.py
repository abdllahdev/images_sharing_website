from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.ImageCreateView.as_view(), name='image_create'),
    path('detail/<int:pk>/<str:slug>/', views.ImageDetailView.as_view(), name='image_detail'),
    path('list/', views.ImageListView.as_view(), name='image_list'),
    path('like/', views.LikeView.as_view(), name='image_like'),
]
