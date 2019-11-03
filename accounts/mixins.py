from django.http import HttpResponse


class AnonymousRequiredMixin:
    """Verify that the current user is anonymous."""
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponse('You are already logged in')
        return super().dispatch(request, *args, **kwargs)

