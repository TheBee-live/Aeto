# Django
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin

# Models
from django.contrib.auth.models import User
from dashboards.models import Excel, Vehiculo, Perfil, Bitacora

@admin.register(Bitacora)
class BitacorasAdmin(admin.ModelAdmin):
    # Admin de las Bitácoras
    list_display = ('numero_economico', 'compañia', 'fecha_de_inflado')
    search_fields= ('numero_economico',)
    list_filter = ('fecha_de_inflado',)

@admin.register(Vehiculo)
class VehiculosAdmin(admin.ModelAdmin):
    # Admin de los Vehículos
    list_display = ('numero_economico', 'numero_de_llantas', 'clase', 'fecha_de_inflado', 'fecha_de_creacion')
    search_fields= ('numero_economico',)
    list_filter = ('fecha_de_creacion', 'clase')


@admin.register(Excel)
class ExcelAdmin(admin.ModelAdmin):
    # Admin del Excel
    list_display = ('id', 'file')

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    # Admin del Perfil
    list_display = ('unidades', 'fecha_de_creacion')
    list_filter = ('fecha_de_creacion',)

class ProfileInline(admin.StackedInline):
    # Alinear el admin del perfil con el de User de Django
    model = Perfil
    can_delete = False
    verbose_name_plural = "perfiles"

class UserAdmin(BaseUserAdmin):
    # Agregar el admin del perfil al admin del User de Django
    inlines = (ProfileInline,)
    list_display = ("username", "email", "is_active")

admin.site.unregister(User)
admin.site.register(User, UserAdmin)