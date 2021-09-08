# Django
from django.contrib.auth.models import User
from django.db import models

# Utilities
from datetime import date, datetime, timedelta

class Vehiculo(models.Model):
    # Modelo del Vehiculo

    numero_economico = models.CharField(max_length=100)
    modelo = models.CharField(max_length=200, null=True, default="Demo")
    marca = models.CharField(max_length=200, null=True, default="Demo")
    compañia = models.CharField(max_length=200, null=True, default="Demo")
    ubicacion = models.CharField(max_length=200, null=True, default="Demo")
    aplicacion = models.CharField(max_length=200, null=True, default="Demo")
    numero_de_llantas = models.PositiveIntegerField(default=8)

    opciones_clase = (("AUTOTANQUE ALIMENTICIO", "Autotanque Alimenticio"),
                    ("AUTOTANQUE COMBUSTIBLE", "Autotanque Combustible"),
                    ("AUTOTANQUE QUIMICOS", "Autotanque Químicos"),
                    ("CAJA REFRIGERADO 48", "Caja Refrigerado 48"),
                    ("CAJA SECA 40", "Caja Seca 40"),
                    ("CAJA SECA 48", "Caja Seca 48"),
                    ("CAJA SECA 53", "Caja Seca 53"),
                    ("CAJA SECA 53 (3 EJES)", "Caja Seca 53 (3 Ejes)"),
                    ("CAMIONETA", "Camioneta"),
                    ("CORTINA", "Cortina"),
                    ("CORTINA 38", "Cortina 38"),
                    ("DOLLY", "Dolly"),
                    ("PLATAFORMA 35", "Plataforma 35"),
                    ("PLATAFORMA 40", "Plataforma 40"),
                    ("PLATAFORMA 53", "Plataforma 53"),
                    ("PLATAFORMA 53 (3 EJES)", "Plataforma 53 (3 Ejes)"),
                    ("PORTACONTENEDOR", "Portacontenedor"),
                    ("RABON", "Rabon"),
                    ("THERMOKING THORTON CAJA 25", "Thermoking Thorton Caja 25"),
                    ("TOLVA", "Tolva"),
                    ("TORTHON REFRIGERADO", "Torthon Refrigerado"),
                    ("TORTHON SECO", "Torthon Seco"),
                    ("TRACTOCAMION", "Tractocamion"),
                    ("UTILITARIO TALLER", "Utilitario Taller"),
                    ("UTILITARIO ADMINISTRATIVO", "Utilitario Administrativo"),
                    ("YARD TRUCK", "Yard Truck")
                )
    clase = models.CharField(max_length=200, choices=opciones_clase, null=True, default="Tractor")
    fecha_de_inflado = models.DateField(null=True, blank=True)
    tiempo_de_inflado = models.FloatField(blank=True, null=True, default=2)
    presion_de_entrada = models.IntegerField(blank=True, null=True, default=100)
    presion_de_salida = models.IntegerField(blank=True, null=True, default=100)
    presion_establecida = models.IntegerField(blank=True, null=True, default=100)

    fecha_de_creacion = models.DateField(auto_now_add=True)

    def __str__(self):
        # Retorna el título y el nombre de usuario
        return f"{self.numero_economico}"

class Bitacora(models.Model):
    # Modelo de la Bitácora

    numero_economico = models.CharField(max_length=100)
    compañia = models.CharField(max_length=200, null=True)
    fecha_de_inflado = models.DateField(null=True, blank=True)
    tiempo_de_inflado = models.FloatField(blank=True, null=True, default=2)
    presion_de_entrada = models.IntegerField(blank=True, null=True, default=100)
    presion_de_salida = models.IntegerField(blank=True, null=True, default=100)
    presion_establecida = models.IntegerField(blank=True, null=True, default=100)


class Excel(models.Model):
    # Modelo del Excel
    compañia = models.CharField(max_length=200, null=True, default="Demo")
    file = models.FileField(upload_to="files/", null=False)


class Perfil(models.Model):
    # Modelo del Perfil de Usuario

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    compañia = models.CharField(max_length=200, null=True, default="Demo")
    opciones_idioma = (("Español", "Español"), ("Inglés", "Inglés"))
    idioma = models.CharField(max_length=200, choices=opciones_idioma, default="Español")
    unidades = models.IntegerField(default=0)
    periodo1 = models.IntegerField(default=30)
    periodo2 = models.IntegerField(default=60)
    objetivo = models.IntegerField(default=10)

    fecha_de_creacion = models.DateTimeField(auto_now_add=True)
    fecha_de_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        # Retorna el username
        return self.user.username