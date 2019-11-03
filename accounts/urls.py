from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.AccountCreateView.as_view(), name='account_create'),
    path('update/', views.AccountUpdateView.as_view(), name='account_update'),
    path('list/', views.AccountListView.as_view(), name='account_list'),
    path('detail/<int:pk>/<str:username>/', views.AccountDetailView.as_view(), name='account_detail'),
    path('follow/', views.FollowView.as_view(), name='account_follow'),
    path('<str:username>/<str:type>/', views.FollowersFollowingView.as_view(), name='account_followers_following'),
]
