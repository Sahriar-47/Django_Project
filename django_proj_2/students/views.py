from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Problem, Solution
from .serializers import ProblemSerializer, SolutionSerializer
from rest_framework.permissions import IsAuthenticated


class ProblemViewSet(viewsets.ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    permission_classes = [IsAuthenticated]


class SolutionViewSet(viewsets.ModelViewSet):
    queryset = Solution.objects.all()
    serializer_class = SolutionSerializer
    permission_classes = [IsAuthenticated]
