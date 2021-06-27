from django.urls import path, include
from django.views.generic.base import View
from . import views
from django.views.generic import RedirectView


urlpatterns = [
    path('home/', views.index, name='index'),
    path('', RedirectView.as_view(url='home/')),
    path('profile/', views.profile, name='profile'),
    path('write-post/', views.write_post_view, name='write-post'),
    path('add-tag/', views.add_tag_view, name='add-tag'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('search-user/', views.follow_view, name='follow' ),
    path('discover/', views.discover, name='discover' ),
    path('discover/<str:name>/', views.discover_tag, name='discover-with-tag' ),
    path('like/<int:pk>/', views.like_post, name='like-post' ),
    
]

#Add Django site authentication urls (for login, logout, password management)

# urlpatterns += [
#     path('accounts/', include('django.contrib.auth.urls')),
# ]