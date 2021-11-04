from django.urls import path

from adventure import views

urlpatterns = [
    path("create-vehicle/", views.CreateVehicleAPIView.as_view()),
    path("start/", views.StartJourneyAPIView.as_view()),
    path("stop/<int:pk>/", views.StopJourneyAPIView.as_view()),
]
