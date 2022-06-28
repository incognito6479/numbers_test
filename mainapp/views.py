from django.views.generic import TemplateView
from django.http.response import HttpResponse
from mainapp.models import OrderDetail
import json


class HomeView(TemplateView):
    template_name = 'home.html'


def get_data_from_db_react(request):
    objs = OrderDetail.objects.all().values('id' ,'id_from_sheet', 'order_number', 'price_usd', 'price_rub', 'delivery_date')
    context = {
        'data': list(objs)
    }
    return HttpResponse(json.dumps(context, sort_keys=True, default=str))
