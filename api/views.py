from django.http import JsonResponse
from django.views import View
from api.metar_radis.meter import get_station_report


class Ping(View):
    def get(self, request):
        res = {"data": "pong"}
        return JsonResponse(res)


class MetarApi(View):
    def get(self, request, *args, **kwargs):
        scode = self.request.GET.get('scode')
        if not scode:
            return JsonResponse({'message': 'Station code is required', 'status': 'error', 'code': 1400})
        nocache = self.request.GET.get('nocache')
        try:
            if nocache is not None:
                nocache = int(nocache)
        except ValueError:
            nocache = 0
        response = get_station_report(scode, nocache)
        print(get_station_report(scode, nocache))
        return JsonResponse(response, status=200)
