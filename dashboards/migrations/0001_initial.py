# Generated by Django 3.0.4 on 2021-08-17 04:08

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Vehiculo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_economico', models.CharField(max_length=100)),
                ('modelo', models.CharField(default='Demo', max_length=200, null=True)),
                ('marca', models.CharField(default='Demo', max_length=200, null=True)),
                ('compañia', models.CharField(default='Demo', max_length=200, null=True)),
                ('ubicacion', models.CharField(default='Demo', max_length=200, null=True)),
                ('aplicacion', models.CharField(default='Demo', max_length=200, null=True)),
                ('numero_de_llantas', models.PositiveIntegerField(default=8)),
                ('clase', models.CharField(choices=[('Tractor', 'Tractor'), ('Remolque', 'Remolque')], default='Tractor', max_length=200, null=True)),
                ('fecha_de_inflado', models.DateField(default=datetime.date(2021, 6, 16), null=True)),
                ('tiempo_de_inflado', models.FloatField(blank=True, default=2, null=True)),
                ('presion_de_entrada', models.IntegerField(blank=True, default=100, null=True)),
                ('presion_de_salida', models.IntegerField(blank=True, default=100, null=True)),
                ('presion_establecida', models.IntegerField(blank=True, default=100, null=True)),
                ('fecha_de_creacion', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idioma', models.CharField(choices=[('Español', 'Español'), ('Inglés', 'Inglés')], default='Español', max_length=200)),
                ('unidades', models.IntegerField(default=0)),
                ('periodo1', models.IntegerField(default=30)),
                ('periodo2', models.IntegerField(default=60)),
                ('objetivo', models.IntegerField(default=10)),
                ('fecha_de_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_de_modificacion', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
