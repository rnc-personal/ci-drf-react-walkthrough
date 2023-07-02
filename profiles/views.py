from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer
from drf_api.permissions import isOwnerOrReadOnly

"""
In the given Django view class, the `context` variable is being used when initializing the `ProfileSerializer` object.
The `context` argument allows you to pass additional context information to the serializer.

In this case, the `context` dictionary is being used to provide the `request` object to the serializer.
The `request` object represents the current HTTP request being handled by the view.
By passing the `request` object in the `context`, the serializer gains access to information about the request,
such as the user making the request or any additional metadata.

The `ProfileSerializer` might use this `request` object in various ways.
For example, it can access the user making the request to apply certain permissions or to customize the serialization process based on the authenticated user.
In summary, the `context` argument in the `ProfileSerializer` initialization allows you to pass additional context information,
such as the `request` object, to the serializer. This can be useful for performing various operations or customizations
based on the request data within the serializer.
"""


class ProfileList(APIView):
    def get(self, request):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True, context={'request': request})
        return Response(serializer.data)

class ProfileDetail(APIView):
    # This is a reserved variable that will show a form in the JSON response for editing a profile
    serializer_class = ProfileSerializer
    permission_classes = [isOwnerOrReadOnly]
    def get_object(self, pk):
        try:
            profile = Profile.objects.get(pk=pk)
            self.check_object_permissions(self.request, profile)
            return profile
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile, context={'request': request})
        return Response(serializer.data)
    
    def put (self, request, pk):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)