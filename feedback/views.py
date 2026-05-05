import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from feedback.models import Feedback  # your model

@csrf_exempt  # Only if you want Postman/API to work without CSRF
def submit_feedback(request):
    # ---------- POST from JSON / API ----------
    if request.method == "POST" and request.content_type and request.content_type.startswith("application/json"):
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

