from django.urls import path
from mainapp.views import HomeView, get_data_from_db_react


urlpatterns = [
    path('', HomeView.as_view(), name="home_view"),
    path('get_data_from_db_react/', get_data_from_db_react, name="get_data_from_db_react"),
]
