from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from .forms import DoctorCreationForm, VisitCreationForm, VisitSearchForm, TestSearchForm, TestCreateForm, \
    DocSearchForm, DocCreateForm

from .models import Doctor, Visit, Test, OtherDocs
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView


# Create your views here.

class DoctorListView(ListView):
    template_name = 'documents/doctors.html'
    context_object_name = 'doctors'

    def get_queryset(self):
        return Doctor.objects.filter(patient=self.request.patient)


class DoctorCreateView(View):
    def get(self, request):
        form = DoctorCreationForm(patient=request.patient)
        return render(request, 'documents/create_doctor.html', {'form': form})

    def post(self, request):
        form = DoctorCreationForm(request.POST, patient=request.patient)
        if form.is_valid():
            doctor = form.save(commit=False)
            doctor.patient = request.patient
            doctor.save()
            return redirect('doctors')
        return render(request, 'documents/create_doctor.html', {'form': form})


class DoctorUpdateView(View):
    def get(self, request, pk):
        doctor = get_object_or_404(Doctor, id=pk, patient=request.patient)
        form = DoctorCreationForm(instance=doctor, patient=request.patient)
        return render(request, 'documents/update_doctor.html', {'form': form})

    def post(self, request, pk):
        doctor = get_object_or_404(Doctor, id=pk, patient=request.patient)
        form = DoctorCreationForm(request.POST, patient=request.patient, instance=doctor)
        if form.is_valid():
            form.save()
            return redirect('doctors')
        return render(request, 'documents/update_doctor.html', {'form': form})


class DoctorDetailView(DetailView):
    template_name = 'documents/doctor_detail.html'
    context_object_name = 'doctor'

    def get_queryset(self):
        return Doctor.objects.filter(patient=self.request.patient)


class DoctorDeleteView(DeleteView):
    template_name = 'documents/doctor_delete_confirmation.html'
    context_object_name = 'doctor'
    success_url = reverse_lazy('doctors')

    def get_queryset(self):
        return Doctor.objects.filter(patient=self.request.patient)


class VisitCreateView(View):
    def get(self, request):
        return render(request, 'documents/create_visit.html', {'form': VisitCreationForm(patient=request.patient)})

    def post(self, request):
        print(request.POST)
        form = VisitCreationForm(request.POST, request.FILES, patient=request.patient)
        if form.is_valid():
            visit = form.save(commit=False)
            visit.patient = request.patient
            visit.save()
            return redirect('visits')
        return render(request, 'documents/create_visit.html', {'form': form})


class VisitListView(ListView):
    template_name = 'documents/visits.html'
    context_object_name = 'visits'

    def get_queryset(self):
        request = self.request
        if request.GET:
            search_q = {arg: value for arg, value in request.GET.items()}
            return Visit.objects.search(**search_q).filter(patient=request.patient)
        return Visit.objects.filter(patient=request.patient)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['form'] = VisitSearchForm()
        return context


class VisitUpdateView(View):
    def get(self, request, pk):
        visit = get_object_or_404(Visit, patient=request.patient, id=pk)
        return render(request, 'documents/update_visit.html',
                      {'form': VisitCreationForm(instance=visit, patient=request.patient)})

    def post(self, request, pk):
        visit = get_object_or_404(Visit, patient=request.patient, id=pk)
        form = VisitCreationForm(request.POST, request.FILES, patient=request.patient, instance=visit)
        if form.is_valid():
            form.save()
            return redirect('visits')
        return render(request, 'documents/update_visit.html', {'form': form})


class VisitDeleteView(DeleteView):
    template_name = 'documents/visit_delete_confirmation.html'
    context_object_name = 'visit'
    success_url = reverse_lazy('visits')

    def get_queryset(self):
        return Visit.objects.filter(patient=self.request.patient)


class TestListView(ListView):
    template_name = 'documents/tests.html'
    context_object_name = 'tests'

    def get_queryset(self):
        request = self.request
        if request.GET:
            search_q = {arg: value for arg, value in request.GET.items()}
            return Test.objects.search(**search_q).filter(patient=request.patient)
        return Test.objects.filter(patient=self.request.patient)

    def get_context_data(self, *args, **kwargs):
        context = super(TestListView, self).get_context_data(*args, **kwargs)
        context['form'] = TestSearchForm()
        return context


class TestCreateView(CreateView):
    template_name = 'documents/create_test.html'
    success_url = reverse_lazy('tests')
    form_class = TestCreateForm

    def form_valid(self, form):
        test = form.save(commit=False)
        test.patient = self.request.patient
        return super().form_valid(form)


class TestUpdateView(UpdateView):
    template_name = 'documents/update_test.html'
    success_url = reverse_lazy('tests')
    form_class = TestCreateForm

    def get_queryset(self):
        return Test.objects.filter(patient=self.request.patient)


class TestDeleteView(DeleteView):
    template_name = 'documents/test_delete_confirmation.html'
    success_url = reverse_lazy('tests')

    def get_queryset(self):
        return Test.objects.filter(patient=self.request.patient)


class SonoListViw(ListView):
    template_name = 'documents/sonos.html'
    context_object_name = 'sonos'

    def get_queryset(self):
        request = self.request
        if request.GET:
            if any(request.GET.values()):
                search_q = {arg: value for arg, value in request.GET.items()}
                search_q['doc_type'] = 'sono'
                return OtherDocs.objects.search(**search_q).filter(patient=request.patient)
        return OtherDocs.objects.filter(doc_type__exact='sono', patient=request.patient)

    def get_context_data(self, *args, **kwargs):
        context = super(SonoListViw, self).get_context_data(*args, **kwargs)
        context['form'] = DocSearchForm()
        return context


class DocCreateView(CreateView):
    template_name = 'documents/create_doc.html'
    form_class = DocCreateForm

    def form_valid(self, form):
        redirect_url_name = form.cleaned_data['doc_type'] + 's'
        doc = form.save(commit=False)
        doc.patient = self.request.patient
        doc.save()
        return redirect(redirect_url_name)


class DocDeleteView(DeleteView):
    template_name = 'documents/doc_delete_confirmation.html'
    context_object_name = 'doc'

    def get_success_url(self):
        redirect_url_name = self.get_object().doc_type + 's'
        return reverse_lazy(redirect_url_name)

    def get_queryset(self):
        return OtherDocs.objects.filter(patient=self.request.patient)


class DocUpdateView(UpdateView):
    template_name = 'documents/update_doc.html'
    form_class = DocCreateForm

    def get_success_url(self):
        redirect_url_name = self.get_object().doc_type + 's'
        return reverse_lazy(redirect_url_name)

    def get_queryset(self):
        return OtherDocs.objects.filter(patient=self.request.patient)


class ImgScanListView(ListView):
    template_name = 'documents/img_scans.html'
    context_object_name = 'img_scans'

    def get_queryset(self):
        request = self.request
        if request.GET:
            if any(request.GET.values()):
                search_q = {arg: value for arg, value in request.GET.items()}
                search_q['doc_type'] = 'img_scan'
                return OtherDocs.objects.search(**search_q).filter(patient=request.patient)
        return OtherDocs.objects.filter(doc_type__exact='img_scan', patient=request.patient)

    def get_context_data(self, *args, **kwargs):
        context = super(ImgScanListView, self).get_context_data(*args, **kwargs)
        context['form'] = DocSearchForm()
        return context


class OtherDocsListView(ListView):
    template_name = 'documents/other_docs.html'
    context_object_name = 'docs'

    def get_queryset(self):
        request = self.request
        if request.GET:
            if any(request.GET.values()):
                search_q = {arg: value for arg, value in request.GET.items()}
                search_q['doc_type'] = 'others'
                return OtherDocs.objects.search(**search_q).filter(patient=request.patient)
        return OtherDocs.objects.filter(doc_type__exact='others', patient=request.patient)

    def get_context_data(self, *args, **kwargs):
        context = super(OtherDocsListView, self).get_context_data(*args, **kwargs)
        context['form'] = DocSearchForm()
        return context
