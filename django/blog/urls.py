from django.urls import path
from blog.views import UserViewSet, PostViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register(r'users', UserViewSet, basename='user')
router.register(r'posts', PostViewSet)

app_name = 'blog'

urlpatterns = router.urls
