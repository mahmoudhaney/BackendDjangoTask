from django.urls import path, include
from . import views
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'blog'

urlpatterns = [
    path('publish/', views.PublishPost.as_view(), name='publish-post'),
    path('posts/', views.ListPosts.as_view(), name='list-posts'),
    path('posts/<int:pk>/', views.RetrieveUpdateDestroyPost.as_view(), name='retrieve-update-delete-post'),
]
