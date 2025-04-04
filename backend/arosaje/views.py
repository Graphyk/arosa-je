from django.shortcuts import render

from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets

from arosaje.serializers import GroupSerializer, UserSerializer, PostsSerializer
from arosaje.models import Plants, Posts
from arosaje.serializers import PlantsSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class PlantsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Plants to be viewed or edited.
    """
    queryset = Plants.objects.all()
    serializer_class = PlantsSerializer
    permission_classes = [permissions.IsAuthenticated]

class PostsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Posts to be viewed or edited.
    """
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer
    permission_classes = [permissions.IsAuthenticated]
