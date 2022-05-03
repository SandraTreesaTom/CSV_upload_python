import pandas as pd
from django.shortcuts import render
from rest_framework.serializers import ValidationError
from csvs.serializers import FileUploadSerializers
from .models import FileUploadModel
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
# from django.http import HttpResponse

# Create your views here.
class FileUploadApiView(APIView):
    permission_classes = (AllowAny,)

    def get(self,request):
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        id = self.request.query_params.get('id')
        if date_from and date_to:
            file_upload_objs = FileUploadModel.objects.filter(date__range = [date_from,date_to])
            serializer = FileUploadSerializers(file_upload_objs,many = True).data
        elif id:
            file_upload_objs = FileUploadModel.objects.get(id = id)
            serializer = FileUploadSerializers(file_upload_objs).data
        
        data = {
            "data":serializer,
            "message": "File Data Returned Successfully"
        }
        return Response(data,status=status.HTTP_200_OK)

    def post(self,request):
        csv_file = request.FILES.get("file")
        if not csv_file.name.endswith('.csv'):
            raise ValidationError("Invalid file extension")

        csv_file_data = pd.read_csv(csv_file,sep=',', header=0)
        column_headers = [name.lower() for name in csv_file_data.columns]

        if not ('date' in column_headers):
            raise ValidationError("Mandatory column are missig!")

        records_to_insert = csv_file_data.to_dict('records')
        
        for record in records_to_insert:
            data_dict = dict()
            data_dict['date'] = record['Date']
            data_dict['name_of_state'] = record['Name of State / UT']
            data_dict['latitude'] = record['Latitude']
            data_dict['longitude'] = record['Longitude']
            data_dict['total_confirmed_cases'] = record['Total Confirmed cases']
            data_dict['death'] = record['Death']
            data_dict['cured'] = record['Cured/Discharged/Migrated']
            data_dict['new_cases'] = record['New cases']
            data_dict['new_deaths'] = record['New deaths']
            data_dict['new_recovered'] = record['New recovered']
      
            try:
                FileUploadModel.objects.create(**data_dict)
            except Exception as e:
                raise ValidationError("Error while Inserting Records")
        return Response(status=status.HTTP_201_CREATED)

    def patch(self,request):
        id = self.request.query_params.get('id')
        try:
            file_upload_obj = FileUploadModel.objects.get(id = id)
        except:
            raise ValidationError("File Object Not Found")
        serializer = FileUploadSerializers(file_upload_obj,data = request.data,partial = True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        data = {
            "data":serializer.data,
            "message": "File Data Updated Successfully"
        }
        return Response(data,status=status.HTTP_200_OK)
    
    def delete(self,request):
        id = self.request.query_params.get('id')
        try:
            file_upload_obj = FileUploadModel.objects.get(id = id)
        except:
            raise ValidationError("File Object Not Found")
        file_upload_obj.delete()
        file_upload_obj.save()

        data = {
            "message": "File Data Deleted Successfully"
        }
        return Response(data,status=status.HTTP_200_OK)
            
