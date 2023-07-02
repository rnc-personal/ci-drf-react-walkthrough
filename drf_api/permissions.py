from rest_framework import permissions

# Checks if the request user is the owner of the object
# This is imported in the views.py file to perform the actual check when the rest is made
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
            if request.method in permissions.SAFE_METHODS:
                return True
            return obj.owner == request.user
