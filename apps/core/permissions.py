from rest_framework.permissions import IsAuthenticated

class AllowOptionsAuthentication(IsAuthenticated):
    def has_permission(self, request, view):
        # print(f"request.method ========> {request.method}")
        if request.method == 'OPTIONS':
            return True
        return request.user and request.user.is_authenticated
