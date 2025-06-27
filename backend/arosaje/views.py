from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import django_filters.rest_framework

from arosaje.serializers import (GroupSerializer, UserSerializer, PostsSerializer, 
                                KeepingSerializer, SpeciesSerializer, PlantsSerializer, ConsentmentsSerializer)
from arosaje.models import Plants, Posts, Keeping, Species, Consentments, ConsentmentAcceptances
from arosaje.filters import PlantsFilterSet, ConsentmentsFilterSet


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
    filterset_class = PlantsFilterSet

    @action(detail=False, methods=['get'])
    def count(self, request):
        filtered_queryset = self.filter_queryset(self.get_queryset())
        return Response(filtered_queryset.count(), status=200)

class PostsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Posts to be viewed or edited.
    """
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['plant']

    ordering_fields = ['start_of_event', 'end_of_event', 'id']
    ordering = ['start_of_event']

    def create(self, request):        
        if (Plants.objects.get(id=request.data["plant_id"]).owner_id != request.user.id):
            raise PermissionError("You can't create a post for somebody else")
        return super().create(request)

class KeepingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Keeping to be viewed or edited.
    """
    queryset = Keeping.objects.all()
    serializer_class = KeepingSerializer
    permission_classes = [permissions.IsAuthenticated]

class SpeciesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Species to be viewed or edited.
    """
    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer
    permission_classes = [permissions.IsAuthenticated]

class ConsentmentsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Consentments to be viewed or edited.
    """
    queryset = Consentments.objects.all()

    serializer_class = ConsentmentsSerializer
    filterset_class = ConsentmentsFilterSet
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'])
    def accept(self, request):
        consentment_id = request.data.get('consentment_id')
        if not consentment_id:
            return Response({'error': 'Consentment ID is required'}, status=400)

        if (ConsentmentAcceptances.objects.filter(
                user_id=request.user.id,
                consentment_id=consentment_id,
                accepted=True
            ).count() > 0):
            return Response({'error': 'This consentment is already accepted'}, status=400)

        ConsentmentAcceptances.objects.create(
            user_id=request.user.id,
            consentment_id=consentment_id,
            accepted=True
        )
        return Response({}, status=201)

    @action(detail=False, methods=['get'])
    def count(self, request):
        filtered_queryset = self.filter_queryset(self.get_queryset())
        return Response(filtered_queryset.count(), status=200)


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'id': user.id,
            'username': user.username,
        })
