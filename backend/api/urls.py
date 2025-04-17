from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, get_message, predict
from . import views

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('message/<str:section>/', get_message, name='get_message'),
    path('predict/', views.predict, name='predict'),
]
