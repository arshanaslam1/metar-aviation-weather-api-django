from django.urls import path
from .views import Ping, MetarApi

urlpatterns = {
    path('ping/', Ping.as_view(), name="ping"),
    path('', MetarApi.as_view(), name="metar-api"),
}