from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
def telemetry_receive(request):
    """
    API endpoint to receive client telemetry events.
    For the MVP stub, it logs the payload to console and returns a 201 Created response.
    """
    data = request.data
    # Print to console for verification during development
    print("LOG: Received Telemetry Event Payload ->", data)
    return Response(
        {"status": "success", "message": "Telemetry event received successfully"},
        status=status.HTTP_201_CREATED
    )

