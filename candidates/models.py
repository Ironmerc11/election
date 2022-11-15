from distutils.command.upload import upload
from pyexpat import model
from django.db import models
from django.contrib.postgres.fields import ArrayField
from cloudinary.models import CloudinaryField


class Location(models.Model):    
    year = models.CharField(max_length=4, null=True)
    state = models.CharField(max_length=30)
    state_code = models.CharField(max_length=20)
    senatorial_district = models.CharField(max_length=200)
    senatorial_district_code = models.CharField(max_length=100, null=True)
    federal_constituency =  models.CharField(max_length=200)
    federal_constituency_code = models.CharField(max_length=100, null=True)
    state_constituency =  models.CharField(max_length=200)
    state_constituency_code = models.CharField(max_length=100, null=True)
    lga = models.CharField(max_length=200)
    lga_code = models.CharField(max_length=100)
    ward = models.CharField(max_length=200)
    ward_code = models.CharField(max_length=100)
    polling_unit = models.CharField(max_length=100)
    polling_unit_code = models.CharField(max_length=50)
    
    
    def __str__(self):
        return self.polling_unit


class Position(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        self.name

class RunningPosition(models.Model):
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    year = models.CharField(max_length=4, null=True)
    
    def __str__(self):
        return self.position.name

class Party(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(null=True)
    
    def __str__(self):
        return self.name

class Candidate(models.Model):
    
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ]
    position = models.ManyToManyField(RunningPosition)
    name = models.CharField(max_length=250)
    candidate_image = models.ImageField( null=True)
    party = models.ForeignKey(Party, on_delete=models.SET_NULL, null=True)
    age = models.PositiveIntegerField(null=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default='Male',)
    qualifications = models.CharField(max_length=250, null=True)
    location = models.ManyToManyField(Location)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.name    
    

class CandidateFile(models.Model):
    UPLOAD_CHOICES = [
        ('Success','Success'),
        ('Failed', 'Failed'),
        ('Uploading','Uploading'),
    ]
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='election-csv/')
    active = models.BooleanField(default=True)
    status = models.CharField(choices=UPLOAD_CHOICES, max_length=50, null=True)
    message = models.CharField(max_length=300, null=True)
    year = models.CharField(max_length=4, null=True)

    
    
    
class SearchQuery(models.Model):
    filter_combo = models.CharField(max_length=500)
    keywords = ArrayField(models.CharField(max_length=200), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.filter_combo
    


class ImageUpload(models.Model):
    image = models.ImageField(upload_to='candidate-pictures/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    