# Django
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView, TemplateView, DetailView, DeleteView, UpdateView
from django.views.generic.base import View

# Functions
from dashboards import functions

# Forms
from dashboards.forms import ExcelForm, VehiculoForm

# Models
from django.contrib.auth.models import User
from dashboards.models import Vehiculo, Perfil

# Utilities
from datetime import date, datetime, timedelta
import json

class LoginView(auth_views.LoginView):
    # Vista de Login

    template_name = "login.html"
    redirect_authenticated_user = True

class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    # Vista de Logout
    pass

class VehiculoAPI(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        jd = json.loads(request.body)
        Vehiculo.objects.create(numero_economico=jd['numero_economico'],
                            tiempo_de_inflado=jd['tiempo_de_inflado'],
                            presion_de_entrada=jd['presion_de_entrada'],
                            presion_de_salida=jd['presion_de_salida']
                            )
        return JsonResponse(jd)

class PulpoView(LoginRequiredMixin, ListView):
    # Vista del dashboard pulpo
    template_name = "pulpo.html"
    model = Vehiculo
    
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        vehiculo = Vehiculo.objects.all()
        hoy = date.today()
        ultimo_mes = hoy - timedelta(days=31)
        vehiculo_fecha = Vehiculo.objects.filter(fecha_de_inflado__range=[ultimo_mes, hoy])
        entrada_correcta_contar = functions.contar_entrada_correcta(vehiculo_fecha)

        vehiculo_periodo = Vehiculo.objects.filter(fecha_de_inflado__lte=ultimo_mes)

        my_profile = Perfil.objects.get(user=self.request.user)

        radar_min = functions.radar_min()
        radar_max = functions.radar_max()
        radar_min_resta = functions.radar_min_resta(radar_min, radar_max)


        functions.excel()

        context["cantidad_total"] = vehiculo.count()
        context["cantidad_inflado"] = vehiculo_fecha.count()
        context["cantidad_entrada"] = entrada_correcta_contar
        context["clases_mas_frecuentes"] = functions.clases_mas_frecuentes()
        context["hoy"] = hoy
        context["porcentaje_inflado"] = functions.porcentaje(vehiculo_fecha.count(), vehiculo.count())
        context["porcentaje_entrada_correcta"] = functions.porcentaje(entrada_correcta_contar, vehiculo_fecha.count())
        context["radar_min"] = radar_min_resta
        context["radar_max"] = radar_max
        context["rango_1"] = my_profile.periodo1
        context["rango_2"] = my_profile.periodo2
        context["rango_3"] = my_profile.periodo1 + 1
        context["rango_4"] = my_profile.periodo2 + 1
        context["tiempo_promedio"] = functions.inflado_promedio(vehiculo_fecha)
        context["vehiculos"] = vehiculo_fecha
        context["vehiculos_periodo"] = vehiculo_periodo
        context["vehiculos_todos"] = vehiculo
        return context


def buscar(request):
    # Busca por fecha, localidad o clase
    
    vehiculo_todos = Vehiculo.objects.all()
    vehiculo = vehiculo_todos.count()
    hoy = date.today()
    clase = request.GET.get("clase")
    fecha = request.GET.get("fecha1")
    fecha2 = request.GET.get("fecha2")
    rango_fecha = request.GET.get("rango_fecha")

    # Buscar por fecha
    if fecha:
        # Definir si se toma en cuenta el mes, la semana o el día
        fecha_date = datetime.strptime(fecha, "%Y-%m-%d").date()
        
        if rango_fecha == "mensual":
            vehiculo_fecha = Vehiculo.objects.filter(fecha_de_inflado__year=fecha_date.year, fecha_de_inflado__month=fecha_date.month)
        elif rango_fecha == "semanal":
            ultima_semana = fecha_date - timedelta(days=7)
            vehiculo_fecha = Vehiculo.objects.filter(fecha_de_inflado__range=[ultima_semana, fecha_date])
        else:
            if fecha2:
                vehiculo_fecha = Vehiculo.objects.filter(fecha_de_inflado__range=[fecha, fecha2])
            else:
                vehiculo_fecha = Vehiculo.objects.filter(fecha_de_inflado__year=fecha_date.year, fecha_de_inflado__month=fecha_date.month, fecha_de_inflado__day=fecha_date.day)
        # Vehículos del periodo 2 y 3
        ultimo_mes = hoy - timedelta(days=31)
        vehiculo_periodo = Vehiculo.objects.filter(fecha_de_inflado__lte=ultimo_mes)

        # Convertir formato de fecha
        if fecha2:
            fecha_con_formato = functions.convertir_rango(fecha, fecha2)
        else:
            fecha_con_formato = functions.convertir_fecha(fecha)

        # Saber el tiempo de inflado promedio
        tiempo_promedio = functions.inflado_promedio(vehiculo_fecha)


        # Sacar el porcentaje de los vehículos inflados que hay dentro de los vehículos
        porcentaje_inflado = functions.porcentaje(vehiculo_fecha.count(), vehiculo)

        # Sacar cuántos vehículos tienen la entrada correcta
        entrada_correcta_contar = functions.contar_entrada_correcta(vehiculo_fecha)

        # Sacar el porcentaje de los vehículos con entrada correcta que hay dentro de los vehículos seleccionados
        porcentaje_entrada_correcta = functions.porcentaje(entrada_correcta_contar, vehiculo_fecha.count())

        return render(request, "pulpo.html", {
                                            "cantidad_total": vehiculo_todos.count(),
                                            "cantidad_inflado": vehiculo_fecha.count(),
                                            "cantidad_entrada": entrada_correcta_contar,
                                            "fecha":fecha,
                                            "fecha2":fecha2,
                                            "fecha_con_formato":fecha_con_formato,
                                            "hoy": hoy,
                                            "porcentaje_inflado":porcentaje_inflado,
                                            "porcentaje_entrada_correcta":porcentaje_entrada_correcta,
                                            "rango_fecha": rango_fecha,
                                            "tiempo_promedio": tiempo_promedio,
                                            "vehiculos": vehiculo_fecha,
                                            "vehiculos_periodo": vehiculo_periodo,
                                            "vehiculos_todos": vehiculo_todos
                                        })

    elif clase:

        vehiculo_clase = Vehiculo.objects.filter(clase=clase)

        # Vehículos del periodo 2 y 3
        ultimo_mes = hoy - timedelta(days=31)
        vehiculo_periodo = Vehiculo.objects.filter(fecha_de_inflado__lte=ultimo_mes)

        # Saber el tiempo de inflado promedio
        tiempo_promedio = functions.inflado_promedio(vehiculo_clase)

        # Sacar el porcentaje de los vehículos inflados que hay dentro de los vehículos
        porcentaje_inflado = functions.porcentaje(vehiculo_clase.count(), vehiculo)

        # Sacar cuántos vehículos tienen la entrada correcta
        entrada_correcta_contar = functions.contar_entrada_correcta(vehiculo_clase)

        # Sacar el porcentaje de los vehículos con entrada correcta que hay dentro de los vehículos seleccionados
        porcentaje_entrada_correcta = functions.porcentaje(entrada_correcta_contar, vehiculo_clase.count())

        return render(request, "pulpo.html", {
                                            "clase": clase,
                                            "hoy": hoy,
                                            "porcentaje_inflado":porcentaje_inflado,
                                            "porcentaje_entrada_correcta":porcentaje_entrada_correcta,
                                            "tiempo_promedio": tiempo_promedio,
                                            "vehiculos": vehiculo_clase,
                                            "vehiculos_periodo": vehiculo_periodo,
                                            "vehiculos_todos": vehiculo_todos
                                        })

    else:
        vehiculo = Vehiculo.objects.all()
        hoy = date.today()
        ultimo_mes = hoy - timedelta(days=31)
        vehiculo_fecha = Vehiculo.objects.filter(fecha_de_inflado__range=[ultimo_mes, hoy])
        entrada_correcta_contar = functions.contar_entrada_correcta(vehiculo_fecha)

        vehiculo_periodo = Vehiculo.objects.filter(fecha_de_inflado__lte=ultimo_mes)

        return render(request, "pulpo.html", {
                                            "hoy": hoy,
                                            "porcentaje_inflado": functions.porcentaje(vehiculo_fecha.count(), vehiculo.count()),
                                            "porcentaje_entrada_correcta": functions.porcentaje(entrada_correcta_contar, vehiculo_fecha.count()),
                                            "tiempo_promedio": functions.inflado_promedio(vehiculo_fecha),
                                            "vehiculos": vehiculo_fecha,
                                            "vehiculos_periodo": vehiculo_periodo,
                                            "vehiculos_todos": vehiculo
        })

class ConfigView(LoginRequiredMixin, CreateView):
    # Vista del dashboard configuración
    template_name = "config.html"
    form_class = ExcelForm
    success_url = reverse_lazy('dashboards:pulpo')

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        user = User.objects.get(username=self.request.user)
        context["user"] = user
        return context

class SearchView(LoginRequiredMixin, ListView):
    # Vista del dashboard buscar_vehiculos
    template_name = "buscar_vehiculos.html"
    model = Vehiculo
    ordering = ("-fecha_de_creacion")
    context_object_name = "vehiculos"
    form_class = VehiculoForm

def search(request):
    num = request.GET.get("numero_economico")
    if num:
        vehiculos = Vehiculo.objects.filter(numero_economico__icontains=num)
        return render(request, "buscar_vehiculos.html", {
                                            "vehiculos": vehiculos
        })
    return render(request, "buscar_vehiculos.html")

class DetailView(LoginRequiredMixin, DetailView):
    # Vista del dashboard detail
    template_name = "detail.html"
    slug_field = "vehiculo"
    slug_url_kwarg = "vehiculo"
    queryset = Vehiculo.objects.all()
    context_object_name = "vehiculo"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        vehiculo = self.get_object()
        fecha = functions.convertir_fecha(str(vehiculo.fecha_de_inflado))
        context["hoy"] = date.today()
        context["fecha"] = fecha
        return context

class PulpoV2View(LoginRequiredMixin, TemplateView):
    # Vista del Pulpo V2
    template_name = "pulpov2.html"

class ConfigV2View(LoginRequiredMixin, TemplateView):
    # Vista del Pulpo V2
    template_name = "config2.html"

class VehiculosV2View(LoginRequiredMixin, TemplateView):
    # Vista del Pulpo V2
    template_name = "vehiculos.html"

class DetailV2View(LoginRequiredMixin, TemplateView):
    # Vista del Pulpo V2
    template_name = "detail2.html"