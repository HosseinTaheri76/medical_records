from django import forms
from django.forms import ModelChoiceField
from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget
from .models import Doctor, Visit, Test, OtherDocs


class DoctorCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.patient = kwargs.pop('patient')
        super().__init__(*args, **kwargs)

    class Meta:
        model = Doctor
        fields = ('name', 'file_no', 'clinic_phone')

    def clean(self):
        cleaned_data = self.cleaned_data
        name = cleaned_data['name']
        qs = Doctor.objects.filter(name=name, patient=self.patient)
        if qs:
            if self.instance:
                if self.instance == qs.get():
                    return cleaned_data
            raise forms.ValidationError('این پزشک از قبل موجود است')
        return cleaned_data


class VisitCreationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.patient = kwargs.pop('patient')
        super().__init__(*args, **kwargs)
        self.fields['doctor'] = ModelChoiceField(
            queryset=Doctor.objects.filter(patient=self.patient),
            label='پزشک'
        )
        self.fields['visit_date'] = JalaliDateField(
            widget=AdminJalaliDateWidget,
            label='تاریخ ویزیت'
        )
        self.fields['next_visit'] = JalaliDateField(
            widget=AdminJalaliDateWidget,
            label='تاریخ ویزیت بعدی',
            required=False
        )

    class Meta:
        model = Visit
        fields = ('doctor', 'reason', 'visit_date', 'next_visit', 'file')


class VisitSearchForm(forms.Form):
    doctor_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput,
        label='نام پزشک',
        required=False
    )
    reason = forms.CharField(
        max_length=150,
        widget=forms.TextInput,
        required=False,
        label='دلیل مراجعه'
    )
    visit_date_from = JalaliDateField(
        required=False,
        widget=AdminJalaliDateWidget,
        label='تاریخ ویزیت از'
    )
    visit_date_to = JalaliDateField(
        required=False,
        widget=AdminJalaliDateWidget,
        label='تاریخ ویزیت تا'
    )
    future = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput,
        label='فقط ویریت های آینده'
    )


class TestSearchForm(forms.Form):
    test_date_from = JalaliDateField(
        required=False,
        widget=AdminJalaliDateWidget,
        label='تاریخ آزمایش از'
    )
    test_date_to = JalaliDateField(
        required=False,
        widget=AdminJalaliDateWidget,
        label='تاریخ آزمایش تا'
    )


class TestCreateForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ('test_date', 'file')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['test_date'] = JalaliDateField(
            widget=AdminJalaliDateWidget,
            label='تاریخ آزمایش'
        )


class DocSearchForm(forms.Form):
    title = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput,
        label='عنوان'
    )
    doc_date_from = JalaliDateField(
        required=False,
        widget=AdminJalaliDateWidget,
        label='تاریخ سند از'
    )
    doc_date_to = JalaliDateField(
        required=False,
        widget=AdminJalaliDateWidget,
        label='تاریخ سند تا'
    )


class DocCreateForm(forms.ModelForm):
    class Meta:
        model = OtherDocs
        fields = ('doc_type', 'title', 'doc_date', 'file')

    def __init__(self, *args, **kwargs):
        super(DocCreateForm, self).__init__(*args, **kwargs)
        self.fields['doc_date'] = JalaliDateField(
            widget=AdminJalaliDateWidget,
            label='تاریخ سند'
        )
