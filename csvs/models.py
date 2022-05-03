from django.db import models

# Create your models here.

class Csv(models.Model):
    file_name = models.FileField(upload_to='csvs')
    uploaded = models.DateTimeField(auto_now_add=True)
    activated =  models.BooleanField(default=False)


    def __str__(self) -> str:
        return f"File id: {self.id}"

class FileUploadModel(models.Model):
    date = models.DateField()
    name_of_state = models.CharField(max_length=255,blank=False,null=False)
    latitude = models.FloatField()
    longitude = models.FloatField()
    total_confirmed_cases = models.IntegerField()
    death = models.IntegerField()
    cured = models.IntegerField()
    new_cases = models.IntegerField()
    new_deaths = models.IntegerField()
    new_recovered = models.IntegerField()