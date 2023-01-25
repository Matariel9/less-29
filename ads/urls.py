from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import include
from rest_framework.routers import SimpleRouter
from ads import views

router = SimpleRouter()
router.register(r'locations', views.LocationViewSet)

urlpatterns = [
    path('ads/', views.AdListView.as_view()),
    path('ads/create/', views.AdCreateView.as_view()),
    path('ads/<int:pk>/', views.AdDetailView.as_view()),
    path('ads/update/<int:pk>/', views.AdUpdateView.as_view()),
    path('ads/delete/<int:pk>/', views.AdDeleteView.as_view()),
    path('ads/<int:pk>/upload_image/', views.ImageView.as_view()),
    ########################################################
    path('categories/', views.CategoryListView.as_view()),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view()),
    path('categories/update/<int:pk>/', views.CategoryUpdateView.as_view()),
    path('categories/delete/<int:pk>/', views.CategoryDeleteView.as_view()),
    ########################################################
    path('users/', views.UserListView.as_view()),
    path('users/<int:pk>/', views.UserDetailView.as_view()),
    path('users/create/', views.UserCreateView.as_view()),
    path('users/<int:pk>/update/', views.UserUpdateView.as_view()),
    path('users/delete/<int:pk>/', views.UserDeleteView.as_view()),
    ########################################################
]

urlpatterns+=router.urls