from django.urls import include, path
from rest_framework import routers
from .views import ProjectViewSet, TaskViewSet, UserProjectsAndTasksView, ProjectsAndTasksView

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'tasks', TaskViewSet, basename='tasks')

urlpatterns = [
    path('', include(router.urls)),
    path('all-projects-tasks/', ProjectsAndTasksView.as_view({'get': 'list'}), name='all-projects-tasks'),
    path('view-details/', UserProjectsAndTasksView.as_view({'get': 'list'}), name='view-details')
]
