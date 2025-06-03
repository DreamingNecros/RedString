#permet de gerer la protection des pages car on utilise les token
from django.shortcuts import redirect
import requests

def jwt_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        token = request.session.get("access_token")

        if not token:
            return redirect("login")

        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get("http://localhost:8000/api/verify-token/", headers=headers)

        if response.status_code == 200:
            return view_func(request, *args, **kwargs)
        else:
            return redirect("login")
    return _wrapped_view
