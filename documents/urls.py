from django.urls import path
from .views import DoctorListView, DoctorCreateView, DoctorUpdateView, DoctorDetailView, DoctorDeleteView, \
    VisitCreateView, VisitListView, VisitUpdateView, VisitDeleteView, TestListView, TestCreateView, TestUpdateView, \
    TestDeleteView, SonoListViw, DocCreateView, DocDeleteView, DocUpdateView, ImgScanListView, OtherDocsListView

urlpatterns = [
    path('doctors/', DoctorListView.as_view(), name='doctors'),
    path('create-doctor/', DoctorCreateView.as_view(), name='create-doctor'),
    path('update-doctor/<int:pk>/', DoctorUpdateView.as_view(), name='update-doctor'),
    path('doctor-detail/<int:pk>/', DoctorDetailView.as_view(), name='doctor-detail'),
    path('delete-doctor/<int:pk>/', DoctorDeleteView.as_view(), name='delete-doctor'),
    path('create-visit/', VisitCreateView.as_view(), name='create-visit'),
    path('visits/', VisitListView.as_view(), name='visits'),
    path('update-visit/<int:pk>/', VisitUpdateView.as_view(), name='update-visit'),
    path('delete-visit/<int:pk>/', VisitDeleteView.as_view(), name='delete-visit'),
    path('tests/', TestListView.as_view(), name='tests'),
    path('create-test/', TestCreateView.as_view(), name='create-test'),
    path('update-test/<int:pk>/', TestUpdateView.as_view(), name='update-test'),
    path('delete-test/<int:pk>/', TestDeleteView.as_view(), name='delete-test'),
    path('sonos/', SonoListViw.as_view(), name='sonos'),
    path('create-doc/', DocCreateView.as_view(), name='create-doc'),
    path('delete-doc/<int:pk>/', DocDeleteView.as_view(), name='delete-doc'),
    path('update-doc/<int:pk>/', DocUpdateView.as_view(), name='update-doc'),
    path('img-scans/', ImgScanListView.as_view(), name='img_scans'),
    path('other-docs/', OtherDocsListView.as_view(), name='otherss'),
]
