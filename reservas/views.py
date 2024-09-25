from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission, IsAuthenticated, IsAdminUser
from rest_framework import viewsets, permissions, generics
from .models import Cliente, Quarto, Reserva
from .serializers import ClienteSerializer, QuartoSerializer, ReservaSerializer, UserSerializer
from django.contrib.auth.models import User


# Classes de Permissão
class IsClient(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and not(request.user.is_staff) and not(request.user.is_staff)
class IsHotelEmployee(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser

# ViewSets
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all() 
    serializer_class = ClienteSerializer

    def get_queryset(self):
        user = self.request.user
        return Cliente.objects.filter(user=user)

    def get_permissions(self):
        if self.request.method in ['GET']:
            self.permission_classes = [IsClient | IsAdmin]  # Cliente pode visualizar, administrador também
        elif self.request.method in ['POST', 'PUT', 'PATCH']:
            self.permission_classes = [IsClient]  # cliente pode criar ou atualizar seu perfil
        elif self.request.method in ['DELETE']:
            self.permission_classes = [IsAdmin]  # Somente administrador pode deletar clientes
        return super(ClienteViewSet, self).get_permissions()

class QuartoViewSet(viewsets.ModelViewSet):
    queryset = Quarto.objects.all()
    serializer_class = QuartoSerializer

    def get_permissions(self):
        if self.request.method in ['GET']:
            self.permission_classes = [IsAuthenticated]  # Todos autenticados podem visualizar quartos
        elif self.request.method in ['POST', 'PUT', 'PATCH']:
            self.permission_classes = [IsHotelEmployee | IsAdmin]  # Funcionários e administradores podem criar e atualizar
        elif self.request.method in ['DELETE']:
            self.permission_classes = [IsAdmin]  # Somente administrador pode deletar quartos
        return super(QuartoViewSet, self).get_permissions()

class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer

    def perform_create(self, serializer):
        cliente = self.request.user.cliente
        serializer.save(cliente=cliente)  # Associar a reserva ao cliente autenticado

    def get_permissions(self):
        if self.request.method in ['GET']:
            self.permission_classes = [IsAuthenticated]  # Todos podem visualizar reservas
        elif self.request.method in ['POST']:
            self.permission_classes = [IsClient | IsAdmin]  # Somente cliente e admin podem criar reservas
        elif self.request.method in ['PUT', 'PATCH']:
            self.permission_classes = [IsHotelEmployee | IsAdmin]  # Funcionários e administradores podem atualizar reservas
        elif self.request.method in ['DELETE']:
            self.permission_classes = [IsAdmin]  # Somente administrador pode deletar reservas
        return super(ReservaViewSet, self).get_permissions()

