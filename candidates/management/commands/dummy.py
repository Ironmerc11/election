from django.core.management.base import BaseCommand
from random import randrange, choice
from candidates.models import Candidate
class Command(BaseCommand):
    
    def __init__(self):
        print('We got to dummy')
        
    
    
    def handle(self, *args, **options):
        self.add_missing_fields()
        
    def add_missing_fields(self):
        candidates = Candidate.objects.all()
        QUALIFICATION_CHOICES = [
        'Doctorate Degree',
        'Masters Degree',
        'Honours Degree',
        'Bachelors Degree',
        'National Diploma',
        'Higher Certificate'
    ]
        for candidate in candidates:
            candidate.party_image = 'https://res.cloudinary.com/rammy/image/upload/v1664547789/All_Progressives_Congress_logo.png'
            candidate.candidate_image = 'https://res.cloudinary.com/rammy/image/upload/v1664546426/peter-obi.jpg'
            candidate.age = randrange(40, 70)
            candidate.qualifications = choice(QUALIFICATION_CHOICES)
            candidate.save()
        
        
        
        