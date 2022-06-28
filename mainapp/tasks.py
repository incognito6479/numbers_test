import requests
from datetime import datetime
from celery import shared_task

from get_sheet_data import main_function


"""

Calls the function to get data from Google API and add to DB

TZ Part 3

"""
@shared_task()
def test_celery():
    main_function()
    return

