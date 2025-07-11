from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='Home'),
    path('blog/create/', views.blog_post_create, name='BlogPostCreate'),
    path('blog/', views.blog_post_list, name='BlogPostList'),
    path('blog/<int:pk>/', views.blog_post_detail, name='BlogPostDetail'),
    path('blog/update/<int:pk>/', views.blog_post_update, name='BlogPostUpdate'),
    path('blog/delete/<int:pk>/', views.blog_post_delete, name='BlogPostDelete'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
]
