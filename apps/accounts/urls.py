from django.urls import path
from rest_framework import routers

from .views import RegisterUserViewSet, UsersModelView,LoginView,ExternalAPIDataView

router = routers.DefaultRouter()
router.register(r'users', UsersModelView, basename='users')

urlpatterns = [
    path('register', RegisterUserViewSet.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('external-api/', ExternalAPIDataView.as_view(), name='external-api'),

]

urlpatterns += router.urls
