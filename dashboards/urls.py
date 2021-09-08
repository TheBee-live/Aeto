# Django
from django.urls import path
from django.views.generic.base import View

# Views
from dashboards import views

urlpatterns = [

    path(
        route="",
        view=views.PulpoView.as_view(),
        name="pulpo"
    ),
    path(
        route="v2/",
        view=views.PulpoV2View.as_view(),
        name="pulpov2"
    ),
        path(
        route="configv2/",
        view=views.ConfigV2View.as_view(),
        name="configv2"
    ),
    path(
        route="vehiculos/",
        view=views.VehiculosV2View.as_view(),
        name="vehiculosv2"
    ),
    path(
        route="detail2/",
        view=views.DetailV2View.as_view(),
        name="detailv2"
    ),
    path(
        route="api/",
        view=views.VehiculoAPI.as_view(),
        name="api"
    ),
    path(
        route="buscar/",
        view=views.buscar,
        name="buscar"
    ),
    path(
        route="config/",
        view=views.ConfigView.as_view(),
        name="config"
    ),
    path(
        route="search/",
        view=views.SearchView.as_view(),
        name="search"
    ),
    path(
        route="search_id/",
        view=views.search,
        name="search_id"
    ),
    path(
        route="<int:pk>/",
        view=views.DetailView.as_view(),
        name="detail"
    ),
    path(
        route="login/",
        view=views.LoginView.as_view(),
        name="login"
    ),
    path(
        route="logout/",
        view=views.LogoutView.as_view(),
        name="logout"
    )
]