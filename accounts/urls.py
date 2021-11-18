from django.urls import path
from .views import PatientListView, PatientCreateView, ManagePatientView, PatientDeleteView, PatientUpdateView, \
    UserLoginView, UserCreationView, LogoutView

urlpatterns = [
    path('select-patient/', PatientListView.as_view(), name='select-patient'),
    path('create-patient/', PatientCreateView.as_view(), name='create-patient'),
    path('delete-patient/<int:pk>/', PatientDeleteView.as_view(), name='delete-patient'),
    path('update-patient/<int:pk>/', PatientUpdateView.as_view(), name='update-patient'),
    path('', ManagePatientView.as_view()),
    path('register/', UserCreationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout')
]
