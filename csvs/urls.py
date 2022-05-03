from . import views
from django.urls import URLPattern, path, include

app_name='csvs'

urlpatterns = [
    path('file_upload',views.FileUploadApiView.as_view())
]