from django.urls import path
from .views import ingest_page, invoices_page,result_page, IngestUDR
from . import views

urlpatterns = [
    path('', ingest_page, name='ingest-page'),
    path('results', result_page, name='result-page'),
    path('invoices/', invoices_page, name='invoices-page'),
    path('api/ingest/', IngestUDR.as_view(), name='api-ingest'),
    path('api/ingest/<int:pk>/', IngestUDR.as_view(), name='api-ingest-detail'),
    # path("api",views.result_page)
]
