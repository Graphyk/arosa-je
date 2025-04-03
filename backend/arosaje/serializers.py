from django.contrib.auth.models import Group, User
from rest_framework import serializers

from arosaje.models import Plants, Species
from address.models import Address

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class ShortAdressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'raw']

class SpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Species
        fields = ['id', 'water_dependency', 'light_dependency']

class PlantsSerializer(serializers.HyperlinkedModelSerializer):
    address = ShortAdressSerializer()
    species = SpeciesSerializer()
    class Meta:
        model = Plants
        fields = ['owner', 'url', 'address', 'species', 'creation_time']
