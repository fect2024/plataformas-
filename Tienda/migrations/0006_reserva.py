# Generated by Django 5.1.2 on 2024-10-18 15:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tienda', '0005_cart'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('producto', models.TextField(blank=True, default={'objects': []}, null=True)),
                ('total', models.CharField(blank=True, max_length=100, null=True)),
                ('estado', models.IntegerField(choices=[(1, 'Pendiente'), (2, 'Despachado'), (3, 'En camino'), (4, 'Entregado'), (5, 'Cancelado'), (6, 'Devuelto')], default=1)),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('actualizado', models.DateTimeField(auto_now=True)),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
