from django.utils import timezone


class LastUserRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            request.user.last_request_at = timezone.now()
            request.user.save(update_fields=["last_request_at"])

        return response
