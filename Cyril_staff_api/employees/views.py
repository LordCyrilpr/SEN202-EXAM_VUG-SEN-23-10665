from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Manager, Intern
from .serializers import (
    ManagerSerializer, 
    InternSerializer, 
    ManagerDetailSerializer
)

class ManagerViewSet(viewsets.ModelViewSet):
    """
    Viewset for Manager model.
    """
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer

    def get_serializer_class(self):
        """Use detailed serializer for retrieve actions"""
        if self.action == 'retrieve':
            return ManagerDetailSerializer
        return ManagerSerializer

    @action(detail=True, methods=['get'])
    def role(self, request, pk=None):
        """
        Get the role of a specific manager using the polymorphic get_role() method.
        """
        manager = self.get_object()
        return Response({
            'id': manager.id,
            'name': manager.full_name,
            'role': manager.get_role(),
            'department': manager.department
        })

    @action(detail=False, methods=['get'])
    def by_department(self, request):
        """
        Get managers grouped by department.
        """
        department = request.query_params.get('department', None)
        if department:
            managers = Manager.objects.filter(department__icontains=department)
        else:
            managers = Manager.objects.all()
        
        serializer = self.get_serializer(managers, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def all_roles(self, request):
        """
        Get roles for all managers using the polymorphic get_role() method.
        """
        managers = self.get_queryset()
        roles = []
        
        for manager in managers:
            roles.append({
                'id': manager.id,
                'name': manager.full_name,
                'role': manager.get_role()
            })
        
        return Response(roles)


class InternViewSet(viewsets.ModelViewSet):
    """
    Viewset for Intern model.
    """
    queryset = Intern.objects.all()
    serializer_class = InternSerializer

    @action(detail=True, methods=['get'])
    def role(self, request, pk=None):
        """
        Get the role of a specific intern using the polymorphic get_role() method.
        """
        intern = self.get_object()
        return Response({
            'id': intern.id,
            'name': intern.full_name,
            'role': intern.get_role(),
            'mentor': intern.mentor.full_name if intern.mentor else None,
            'internship_end_date': intern.internship_end_date
        })

    @action(detail=False, methods=['get'])
    def by_mentor(self, request):
        """
        Get interns grouped by mentor.
        """
        mentor_id = request.query_params.get('mentor_id', None)
        if mentor_id:
            interns = Intern.objects.filter(mentor_id=mentor_id)
        else:
            interns = Intern.objects.all()
        
        serializer = self.get_serializer(interns, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def without_mentor(self, request):
        """
        Get interns without assigned mentors.
        """
        interns = Intern.objects.filter(mentor__isnull=True)
        serializer = self.get_serializer(interns, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def all_roles(self, request):
        """
        Get roles for all interns using the polymorphic get_role() method.
        """
        interns = self.get_queryset()
        roles = []
        
        for intern in interns:
            roles.append({
                'id': intern.id,
                'name': intern.full_name,
                'role': intern.get_role()
            })
        
        return Response(roles)
