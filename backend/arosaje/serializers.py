from django.contrib.auth.models import Group, User
from rest_framework import serializers

from arosaje.models import Plants, Species, Posts
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

class PostsSerializer(serializers.HyperlinkedModelSerializer):
    plant = PlantsSerializer(read_only=True)
    plant_id = serializers.PrimaryKeyRelatedField(
        queryset=Plants.objects.all(),
        write_only=True,
        source='plant'
    )

    class Meta:
        model = Posts
        fields = ['url','commentary', 'plant', 'plant_id', 'start_of_event', 'end_of_event']

class KeepingSerializer(serializers.HyperlinkedModelSerializer):
    post = PostsSerializer(read_only=True)
    post_id = serializers.PrimaryKeyRelatedField(
        queryset=Posts.objects.all(),
        write_only=True,
        source='post'
    )

    keeper = UserSerializer(read_only=True)
    keeper_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
        source='user'
    )

    class Meta:
        model = Posts
        fields = ['url', 'post', 'post_id', 'keeper', 'keeper_id']
