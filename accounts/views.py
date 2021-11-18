from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView, TemplateView, DeleteView, UpdateView
from .models import Patient
from .forms import PatientCreationForm, UserRegisterForm, LoginForm
from django.contrib.auth.models import User
from django.views import View


# Create your views here.

class PatientListView(ListView):
    model = Patient
    context_object_name = 'patients'
    template_name = 'accounts/select_patient.html'

    def get_queryset(self):
        return Patient.objects.filter(user=self.request.user)


class PatientCreateView(FormView):
    form_class = PatientCreationForm
    template_name = 'accounts/create_patient.html'

    def form_valid(self, form):
        Patient.objects.create(**form.cleaned_data, user=self.request.user)
        return redirect('select-patient')


class PatientDeleteView(DeleteView):
    model = Patient
    template_name = 'accounts/patient_delete_confirmation.html'
    context_object_name = 'patient'
    success_url = reverse_lazy('select-patient')

    def get_queryset(self):
        return Patient.objects.filter(user=self.request.user)


class ManagePatientView(TemplateView):
    template_name = 'accounts/manage_patient.html'


class PatientUpdateView(UpdateView):
    model = Patient
    fields = ('name',)
    template_name = 'accounts/update_patient.html'
    success_url = reverse_lazy('select-patient')

    def get_queryset(self):
        return Patient.objects.filter(user=self.request.user)


class UserCreationView(FormView):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('select-patient')
        return super().get(request, *args, **kwargs)

    form_class = UserRegisterForm
    success_url = reverse_lazy('select-patient')
    template_name = 'accounts/register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)


class UserLoginView(FormView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('select-patient')
        return super().get(request, *args, **kwargs)

    form_class = LoginForm
    success_url = reverse_lazy('select-patient')
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        user = authenticate(**form.cleaned_data)
        if user:
            login(self.request, user)
            return redirect('select-patient')
        else:
            form.add_error('username', 'نام کاربری یا کلمه ی عبور اشتباه است')
            return render(self.request, 'accounts/login.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        if 'p_code' in request.COOKIES:
            request.COOKIES.pop('p_code')
        logout(request)
        return redirect('login')
