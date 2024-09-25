# Generated by Django 5.1.1 on 2024-09-24 20:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Quarto",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("numero", models.CharField(max_length=5, unique=True)),
                (
                    "tipo",
                    models.CharField(
                        choices=[
                            ("simples", "Simples"),
                            ("duplo", "Duplo"),
                            ("luxo", "Luxo"),
                        ],
                        max_length=10,
                    ),
                ),
                ("preco_diaria", models.DecimalField(decimal_places=2, max_digits=8)),
                ("disponivel", models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name="Cliente",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("telefone", models.CharField(max_length=15)),
                ("endereco", models.CharField(max_length=255)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cliente",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Reserva",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("data_entrada", models.DateField()),
                ("data_saida", models.DateField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pendente", "Pendente"),
                            ("confirmada", "Confirmada"),
                            ("cancelada", "Cancelada"),
                        ],
                        default="pendente",
                        max_length=10,
                    ),
                ),
                (
                    "cliente",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reservas",
                        to="reservas.cliente",
                    ),
                ),
                (
                    "quarto",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reservas",
                        to="reservas.quarto",
                    ),
                ),
            ],
        ),
    ]
