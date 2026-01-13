
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

import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from feedback.models import Feedback  # your model

@csrf_exempt  # Only if you want Postman/API to work without CSRF
def submit_feedback(request):
    # ---------- POST from JSON / API ----------
    if request.method == "POST" and request.headers.get("Content-Type") == "application/json":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        full_name = data.get("full_name")
        email = data.get("email")
        feedback_text = data.get("feedback")

        if not all([full_name, email, feedback_text]):
            return JsonResponse({"error": "All fields are required"}, status=400)

        Feedback.objects.create(
            full_name=full_name,
            email=email,
            feedback=feedback_text
        )
        return JsonResponse({"message": "Feedback submitted successfully"})


    # ---------- POST from Browser Form ----------
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        feedback_text = request.POST.get("feedback")

        if not all([full_name, email, feedback_text]):
            return render(request, "feedback/feedback_form.html", {"error": "All fields are required"})

        Feedback.objects.create(
            full_name=full_name,
            email=email,
            feedback=feedback_text
        )

        return render(request, "feedback/feedback_form.html", {"success": "Feedback submitted successfully"})


    # ---------- GET ----------
    return render(request, "feedback/feedback_form.html")

