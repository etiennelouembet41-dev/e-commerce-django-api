from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    
    def has_permission(self, request, view):
        
        if request.method in SAFE_METHODS: #SAFE_METHODS = GET, HEAD, OPTIONS.
            return True
        
        return(
            request.user.is_authenticated
            and request.user.role=="admin" #Pour POST, PUT, PATCH, DELETE, il faut être connecté et avoir le rôle admin.
        )