# from django.http import JsonResponse

# def csrf_required(view_func):
#     def wrapper(request, *args, **kwargs):
#         if request.method == "POST" and not request.META.get("CSRF_COOKIE"):
#             return JsonResponse({"error": "CSRF token missing!"}, status=403)
#         return view_func(request, *args, **kwargs)
#     return wrapper
from django.http import JsonResponse
from django.middleware.csrf import CsrfViewMiddleware

def csrf_required(view_func): #main function of decorator
    def wrapper(request, *args, **kwargs):# inner function- putting logic / execuion

        # Create a dummy get_response function required by middleware
        def dummy_get_response(req):
            return None

        # Initialize middleware properly
        csrf_middleware = CsrfViewMiddleware(dummy_get_response)

        # Let Django validate CSRF safely
        reason = csrf_middleware.process_view(request, view_func, args, kwargs)

        if reason:
            return JsonResponse({"error": "CSRF Failed", "detail": str(reason)}, status=403)

        return view_func(request, *args, **kwargs)

    return wrapper
