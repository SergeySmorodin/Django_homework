from rest_framework import generics
from .models import Sensor, Measurement
from .serializers import SensorSerializer, SensorDetailSerializer, MeasurementSerializer

class SensorListCreateView(generics.ListCreateAPIView):
    """ GET, POST /sensors/ """
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

class SensorRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    """ GET, PUT/PATCH /sensors/{id}/ """
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

class MeasurementCreateView(generics.CreateAPIView):
    """ POST /measurements/ """
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer

class SensorDetailView(generics.RetrieveAPIView):
    """ GET /sensors/{id}/detail/ """
    queryset = Sensor.objects.all()
    serializer_class = SensorDetailSerializer


