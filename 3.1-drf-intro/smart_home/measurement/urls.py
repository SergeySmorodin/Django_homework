from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import SensorListCreateView, SensorRetrieveUpdateView, MeasurementCreateView, SensorDetailView

urlpatterns = [
    path('sensors/', SensorListCreateView.as_view(), name='sensor-list-create'),
    path('sensors/<int:pk>/', SensorRetrieveUpdateView.as_view(), name='sensor-retrieve-update'),
    path('measurements/', MeasurementCreateView.as_view(), name='measurement-create'),
    path('sensors/<int:pk>/detail/', SensorDetailView.as_view(), name='sensor-detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

