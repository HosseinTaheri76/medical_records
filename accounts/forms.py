from django import forms
from .models import Patient
from django.contrib.auth.models import User


class PatientCreationForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(),
        label='نام بیمار'
    )

    def clean_name(self):
        name = self.cleaned_data['name']
        if not Patient.objects.filter(name=name):
            return name
        raise forms.ValidationError('ین نام تکراری است')


class UserRegisterForm(forms.ModelForm):
    password_2 = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput,
        label='تکرار کلمه ی عبور'
    )

    class Meta:
        model = User
        fields = ('username', 'password')
        labels = {
            'username': 'نام کاربری',
            'password': 'کلمه ی عبور'
        }

    def clean(self):
        cleaned_data = self.cleaned_data
        username = cleaned_data['username']
        password = cleaned_data['password']
        password_2 = cleaned_data['password_2']
        if User.objects.filter(username=username):
            raise forms.ValidationError('کاربری با این نام کاربری از قبل موجود است')
        if password_2 != password:
            raise forms.ValidationError('کلمه ی عبور و تکرار کلمه ی عبور مطابقت ندارند')
        return cleaned_data

    def save(self, commit=True):
        data = self.cleaned_data
        data.pop('password_2')
        user = User.objects.create_user(**data)
        return user


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput,
        label='نام کاربری'
    )
    password = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput,
        label='کلمه ی عبور'
    )


