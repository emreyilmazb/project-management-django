from django.shortcuts import render
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

# Create your views here.

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    
    def destroy(self, request, pk=None):
        project = self.get_object()
        user = request.user
        if(user != project.project_manager):
            return Response(
                {"detail": "You can delete the project only if you are the project manager."},
                status=status.HTTP_403_FORBIDDEN
            )
        self.perform_destroy(project)
        return Response({"detail":'Project successfully deleted' }, status=status.HTTP_204_NO_CONTENT)
    
    def update(self, request, pk=None):
        project = self.get_object()
        user = request.user
    
        # Serializer ile verileri doğrula
        if(user != project.project_manager):
            return Response(
                {"detail": "You can update the project only if you are the project manager."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = self.get_serializer(project, data=request.data)
        serializer.is_valid(raise_exception=True)
        # Nesneyi güncelle ve kaydet
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        # Güncellenen nesneyi kaydet
        serializer.save()

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
    def destroy(self, request, pk=None):
        thetask = self.get_object()
        user = request.user
        if(user != thetask.project.project_manager):
            return Response(
                {"detail": "You can delete the task only if you are the project manager."},
                status=status.HTTP_403_FORBIDDEN
            )
        self.perform_destroy(thetask)
        return Response({"detail":'Task successfully deleted' }, status=status.HTTP_204_NO_CONTENT)

    def create(self, request, *args, **kwargs):
        thetask = self.get_object()
        user = request.user
        if(user != thetask.project.project_manager):
            return Response(
                {"detail": "You can create tasks only if you are the project manager."},
                status=status.HTTP_403_FORBIDDEN
            )
        self.create(thetask)
        return Response({"detail":'Task successfully created' }, status=status.HTTP_204_NO_CONTENT)
    
    def perform_create(self, serializer):
        serializer.save()

class UserProjectsAndTasksView(viewsets.ViewSet):
    def list(self, request):
        user = request.user
        if(user.user_type == 'team_lead'): # Yönetici
            projects = Project.objects.filter(project_manager=user)
            serializer = ProjectSerializer(projects, many=True)
            return Response({"managed_projects": serializer.data}, status=status.HTTP_200_OK)
        else: # Normal Kullanıcı
            assigned_projects = Project.objects.filter(team_members=user)
            assigned_tasks = Task.objects.filter(assigned_to=user)
            
            project_serializer = ProjectSerializer(assigned_projects, many=True)
            task_serializer = TaskSerializer(assigned_tasks, many=True)
            return Response({
                "assigned_projects": project_serializer.data,
                "assigned_tasks": task_serializer.data
            }, status=status.HTTP_200_OK)

class ProjectsAndTasksView(viewsets.ViewSet):
    def list(self, request):
        all_projects = Project.objects.all()
        all_tasks = Task.objects.all()
        
        serializeProjects = ProjectSerializer(all_projects, many=True)
        return Response({
            "all_projects": list(all_projects),  # Proje ID ve isimlerini döndürüyoruz
            "all_tasks": list(all_tasks)  # Görev ID ve başlıklarını döndürüyoruz
        }, status=status.HTTP_200_OK)