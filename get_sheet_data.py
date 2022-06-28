import os
from datetime import datetime

import requests
import json
from googleapiclient import discovery

from mainapp.models import OrderDetail
from system.settings import BASE_DIR
from environs import Env


env = Env()
env.read_env()


"""

Gets all expired orders delivery time and sends to Telegram User with given USER_ID

TZ Part 4.B

"""
def send_invoice_to_user(response):
    today = datetime.now()
    template = "\nСписок заказов с истекшим сроком доставки\n"
    for row in response:
        if datetime.fromisoformat("-".join(row[-1].split('.')[::-1])) < today:
            template += f"\n   Номер заказа :{row[1]} \n   Срок поставки :{row[-1]} \n\n"
    requests.get(f"https://api.telegram.org/bot{env('BOT_TOKEN')}/sendMessage?chat_id={env('TELEGRAM_USER_ID')}"
                 f"&text={template}")
    return


def main_function():
    """

    This is the code to get Google Sheet Data from Google API

    TZ Part 1

    """
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(BASE_DIR, 'credentials.json')
    credentials = None
    service = discovery.build('sheets', 'v4', credentials=credentials)
    spreadsheet_id = '1OKSnEclNbO2Zu7sepGVtpTVz9eC83eh5qi1Qif3GBXM'
    range_ = "A2:Z1000"
    request = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_)
    response = request.execute()  # returns list of spreadsheet values in row
    """
    
    TZ Part 4.B
    
    """
    send_invoice_to_user(response['values'])
    """
    
    Gets USD Currency from url
    
    TZ Part 2.B
    
    """
    resp = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
    resp = json.loads(resp.content)
    usd_currency = resp['Valute']['USD']['Value']
    """
    
    Main Algorithm for Creating, Updating and Deleting values from Google Spreadsheet
    
    TZ Part 2.A 2.B Part 3
    
    """
    google_ids_from_response = []
    google_ids_from_db = []
    for row in response['values']:
        google_ids_from_response.append(row[0])
    order_detail_objs = OrderDetail.objects.all().in_bulk()
    if bool(order_detail_objs):
        for order_detail_obj in order_detail_objs.values():
            google_ids_from_db.append(str(order_detail_obj.id_from_sheet))
    # deleting objects
    ids_needed_to_delete = set(google_ids_from_db) - set(google_ids_from_response)
    for id_ in list(ids_needed_to_delete):
        google_ids_from_db.remove(id_)
        OrderDetail.objects.filter(id_from_sheet=id_).delete()
    # creating and updating objects
    ids_needed_to_create = set(google_ids_from_response) - set(google_ids_from_db)
    object_bulk_create_list = []
    for row in response['values']:
        if row[0] in list(ids_needed_to_create):
            object_bulk_create_list.append(
                OrderDetail(
                    id_from_sheet=row[0],
                    order_number=row[1],
                    price_usd=row[2],
                    price_rub=int(row[2]) * usd_currency,
                    delivery_date="-".join(row[-1].split('.')[::-1])
                )
            )
        if row[0] in google_ids_from_db:
            if bool(order_detail_objs):
                for order_detail_obj in order_detail_objs.values():
                    if row[0] == str(order_detail_obj.id_from_sheet):
                        order_detail_obj.order_number = row[1]
                        order_detail_obj.price_usd = row[2]
                        order_detail_obj.price_rub = int(row[2]) * usd_currency
                        order_detail_obj.delivery_date = "-".join(row[-1].split('.')[::-1])
    OrderDetail.objects.bulk_create(object_bulk_create_list)
    if bool(order_detail_objs):
        OrderDetail.objects.bulk_update(order_detail_objs.values(), fields=('order_number', 'price_usd',
                                                                            'price_rub', 'delivery_date'))
    return
