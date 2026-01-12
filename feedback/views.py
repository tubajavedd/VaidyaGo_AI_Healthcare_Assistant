# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Feedback
# from .serializers import FeedbackSerializer

# @api_view(['POST'])
# def submit_feedback(request):
#     serializer = FeedbackSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(
#             {"message": "Feedback submitted successfully"},
#             status=status.HTTP_201_CREATED
#         )
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import FeedbackSerializer

@api_view(['GET', 'POST'])
def submit_feedback(request):
    if request.method == 'GET':
        return Response(
            {"detail": "Use POST to submit feedback"},
            status=status.HTTP_200_OK
        )

    serializer = FeedbackSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "Feedback submitted successfully"},
            status=status.HTTP_201_CREATED
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
