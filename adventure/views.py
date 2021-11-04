from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView
from rest_framework import status

from adventure import models, notifiers, repositories, serializers, usecases


class CreateVehicleAPIView(APIView):
    def post(self, request: Request) -> Response:
        payload = request.data
        vehicle_type = models.VehicleType.objects.get(name=payload["vehicle_type"])
        vehicle = models.Vehicle.objects.create(
            name=payload["name"],
            passengers=payload["passengers"],
            vehicle_type=vehicle_type,
        )
        return Response(
            {
                "id": vehicle.id,
                "name": vehicle.name,
                "passengers": vehicle.passengers,
                "vehicle_type": vehicle.vehicle_type.name,
            },
            status=201,
        )


class StartJourneyAPIView(generics.CreateAPIView):
    serializer_class = serializers.JourneySerializer

    def perform_create(self, serializer) -> None:
        repo = self.get_repository()
        notifier = notifiers.Notifier()
        usecase = usecases.StartJourney(repo, notifier).set_params(
            serializer.validated_data
        )
        try:
            usecase.execute()
        except usecases.StartJourney.CantStart as e:
            raise ValidationError({"detail": str(e)})

    def get_repository(self) -> repositories.JourneyRepository:
        return repositories.JourneyRepository()


class StopJourneyAPIView(APIView):
    def put(self, request: Request, pk: int) -> Response:
        repo = self.get_repository()
        journey = repo.get_journey_by_pk(pk=pk)
        usecase = usecases.StopJourney(repo, journey)
        try:
            usecase.execute()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except usecases.StopJourney.CantStop:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get_repository(self) -> repositories.JourneyRepository:
        return repositories.JourneyRepository()