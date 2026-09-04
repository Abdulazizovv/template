from rest_framework import generics, permissions

from .serializers import UserSerializer


class MeView(generics.RetrieveUpdateAPIView):
    """Example authenticated resource: the logged-in user's own profile."""

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
