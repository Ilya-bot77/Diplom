"""
URL configuration for social_network project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter

from posts.views import PostViewSet, CommentViewSet, LikeViewSet

# маршруты для работы с постами

r = DefaultRouter()
r.register('post', PostViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),

# маршруты для работы с комментариями

    path('post/<int:post_id>/comment/', CommentViewSet.as_view({'post': 'create'})),
    path('post/<int:post_id>/comment/<int:comment_id>/', CommentViewSet.as_view({'put': 'update', 'delete': 'destroy'})),

# маршруты для установки/снятия like

    path('post/<int:post_id>/like/', LikeViewSet.as_view({'post': 'create', 'patch': 'patch'}))
] + r.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)