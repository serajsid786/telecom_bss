from django.shortcuts import render, redirect
from .models import Service, UDR, Invoice
from django.utils import timezone
from .rating_engine import rate_udr
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UDRSerializer

# Minimal UI: ingest form
def ingest_page(request):
    services = Service.objects.all()
    if request.method == 'POST':
        service_id = request.POST.get('service_id')
        usage_class = request.POST.get('usage_class')
        usage_amount = request.POST.get('usage_amount')
        try:
            service = Service.objects.get(service_id=service_id)
        except Service.DoesNotExist:
            return render(request, 'rating/ingest.html', {'services': services, 'error': 'Service not found.'})

        udr = UDR.objects.create(
            raw={'source': 'ui'},
            timestamp=timezone.now(), 
            service=service, 
            usage_class=usage_class, 
            usage_amount=usage_amount,
        )
        
        rate_udr(udr)
        return redirect('result-page')
    return render(request, 'rating/ingest.html', {'services': services})

def result_page(request):
    udrs = UDR.objects.all()
    return render(request, 'rating/result.html', {'udrs': udrs})

def invoices_page(request):
    invoices = Invoice.objects.order_by('-created_at')[:50]
    return render(request, 'rating/invoices.html', {'invoices': invoices})


# API endpoint to ingest UDRs (POST JSON)
class IngestUDR(APIView):
    def post(self, request):
        payload = request.data
        service_id = payload.get('service_id')
        if not service_id:
            return Response({'error':'service_id required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            service = Service.objects.get(service_id=service_id)
        except Service.DoesNotExist:
            return Response({'error':'service not found'}, status=status.HTTP_400_BAD_REQUEST)

        data = {
            'raw': payload.get('raw', payload),
            'timestamp': payload.get('timestamp', timezone.now()),
            'service': service.id,                 # serializer expects FK id
            'usage_class': payload.get('usage_class'),
            'usage_amount': payload.get('usage_amount'),
        }
        
        serializer = UDRSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        udr = serializer.save()
        rate_udr(udr)
        return Response(UDRSerializer(udr).data, status=status.HTTP_201_CREATED)
    
    def get(self, request, pk=None):
        if pk is not None:
            try:
                udr = UDR.objects.get(id=pk)
            except UDR.DoesNotExist:
                return Response({'error': 'UDR not found'}, status=404)
            return Response(UDRSerializer(udr).data, status=200)

        udrs = UDR.objects.order_by('-created_at')[:100]
        return Response(UDRSerializer(udrs, many=True).data, status=200)
    
    def put(self, request, pk):
        try:
            udr = UDR.objects.get(id=pk)
        except UDR.DoesNotExist:
            return Response({'error': 'UDR not found'}, status=404)

        # Data coming from client
        payload = request.data

        # Update allowed fields (you can choose what to update)
        udr.usage_class = payload.get('usage_class', udr.usage_class)
        udr.usage_amount = payload.get('usage_amount', udr.usage_amount)
        udr.raw = payload.get('raw', udr.raw)

        # Re-rate the UDR after update
        udr.save()
        rate_udr(udr)

        return Response(UDRSerializer(udr).data, status=200)
    
    def delete(self, request, pk):
        try:
            udr = UDR.objects.get(id=pk)
        except UDR.DoesNotExist:
            return Response({'error': 'UDR not found'}, status=404)

        udr.delete()
        return Response({'message': 'UDR deleted successfully'}, status=200)
