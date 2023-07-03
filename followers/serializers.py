from rest_framework import serializers
from .models import User, Follower
from django.db import IntegrityError

class FollowerSerializer(serializers.ModelSerializer):
    # "owner" is a foreign key to the User model, the user that someone else is following
    owner = serializers.ReadOnlyField(source='owner.username')
    # "followed" is a foreign key to the User model for another user
    followed_by = serializers.ReadOnlyField(source='followed.username')

    class Meta:
        model = Follower
        fields = ['id', 'owner', 'created_at', 'followed', 'followed_name']

    
    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError('You already follow this user')