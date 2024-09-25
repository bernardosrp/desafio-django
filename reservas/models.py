from django.db import models
from django.contrib.auth.models import User

# Cliente
class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cliente')
    telefone = models.CharField(max_length=15)
    endereco = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username

# Quarto
class Quarto(models.Model):
    TIPO_QUARTO_CHOICES = [
        ('simples', 'Simples'),
        ('duplo', 'Duplo'),
        ('luxo', 'Luxo'),
    ]
    numero = models.CharField(max_length=5, unique=True)
    tipo = models.CharField(max_length=10, choices=TIPO_QUARTO_CHOICES)
    preco_diaria = models.DecimalField(max_digits=8, decimal_places=2)
    disponivel = models.BooleanField(default=True)

    def __str__(self):
        return f"Quarto {self.numero} - {self.get_tipo_display()}"

# Reserva
class Reserva(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='reservas')
    quarto = models.ForeignKey(Quarto, on_delete=models.CASCADE, related_name='reservas')
    data_entrada = models.DateField()
    data_saida = models.DateField()

    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pendente')

    def __str__(self):
        return f"Reserva de {self.cliente} no quarto {self.quarto.numero} de {self.data_entrada} a {self.data_saida}"

    # Validação para garantir que a data de saída seja após a data de entrada
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.data_saida <= self.data_entrada:
            raise ValidationError('A data de saída deve ser posterior à data de entrada.')

    # Método para verificar se o quarto está disponível no intervalo de datas
    def quarto_disponivel(self):
        reservas = Reserva.objects.filter(quarto=self.quarto)
        for reserva in reservas:
            if (self.data_entrada <= reserva.data_saida and self.data_saida >= reserva.data_entrada):
                return False
        return True

    

