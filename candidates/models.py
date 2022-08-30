from django.db import models
from django.contrib.postgres.fields import ArrayField

class Candidate(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ]
    # QUALIFICATION_CHOICES = [
    #     ('Doctorate Degree','Doctorate Degree'),
    #     ('')
    # ]
    year = models.CharField(max_length=4)
    state = models.CharField(max_length=30)
    state_code = models.CharField(max_length=20)
    senatorial_district = models.CharField(max_length=200)
    senatorial_district_code = models.CharField(max_length=100)
    federal_constituency =  models.CharField(max_length=200)
    federal_constituency_code = models.CharField(max_length=100)
    state_constituency =  models.CharField(max_length=200)
    state_constituency_code = models.CharField(max_length=100)
    lga = models.CharField(max_length=200)
    lga_code = models.CharField(max_length=100)
    ward = models.CharField(max_length=200)
    ward_code = models.CharField(max_length=100)
    polling_unit = models.CharField(max_length=100)
    polling_unit_code = models.CharField(max_length=50)
    position = models.CharField(max_length=150)
    name = models.CharField(max_length=250)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    qualifications = ArrayField(models.CharField(max_length=50, blank=True))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.name