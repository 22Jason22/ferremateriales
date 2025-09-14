from rest_framework import generics
from .serializers import UserSerializer

class UserRegistrationView(generics.CreateAPIView):
    queryset = UserSerializer.Meta.model.objects.all()
    serializer_class = UserSerializer