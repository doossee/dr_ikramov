from django.contrib.auth import views


class LogoutView(views.LogoutView):
    """ """
    http_method_names = ["get", "post", "options"]

    def get(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)