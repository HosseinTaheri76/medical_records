from .models import Patient
from django.shortcuts import redirect
from django.conf import settings


class CheckLoginMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not any(request.path.startswith(url) for url in settings.NO_AUTH_REQUIRED_URLS):
            if not request.user.is_authenticated:
                return redirect('login')
        response = self.get_response(request)
        return response


class SetOrGetPatientMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not any([request.path.startswith(pattern) for pattern in settings.NO_PATIENT_REQUIRED_URLS]):
            p_code = request.COOKIES.get('p_code')
            if not p_code:
                return redirect('select-patient')
            try:
                patient = Patient.objects.get(code=int(p_code), user=request.user)
                request.patient = patient
            except Patient.DoesNotExist:
                return redirect('select-patient')
        response = self.get_response(request)
        return response
