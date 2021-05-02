from rest_framework import permissions


class IsStaffUser(permissions.BasePermission):
    "Allow the requests which has temporary token for registration purpose"

    def has_permission(self, request, view):
        byebug
        if request.user.is_superuser:
            return True
        return False
        
    
