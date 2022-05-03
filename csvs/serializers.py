from rest_framework import serializers
from csvs.models import FileUploadModel

class FileUploadSerializers(serializers.ModelSerializer):
    class Meta:
        model = FileUploadModel
        fields = '__all__'