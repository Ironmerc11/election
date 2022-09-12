import json
from celery import shared_task
import os
from django.conf import settings
import pandas as pd
from .models import Candidate, Location, Position, RunningPosition, CandidateFile


@shared_task
def add_candidates_to_db(saved_file_id, parties, year):
  
    file = CandidateFile.objects.get(id=saved_file_id)
    try:
        reader = pd.read_excel(f'{settings.BASE_DIR}{file.file.url}')
        
        
        # if file_extension == '.xlsx':   
        #     reader = pd.read_excel(file)
        # elif file_extension == '.csv':
        #     reader = pd.read_csv(file)
        location_ids = []
        
        # reader = json.loads(reader_)
        for _, row in reader.iterrows():
            
            try:
                location_id = Location.objects.get(polling_unit_code=row['PUCODE'])
                location_ids.append(location_id)

            except Location.DoesNotExist:
                location_id = Location.objects.create(
                    year=year,
                    state=row["STATE"],
                    state_code=row["STATECODE"],
                    senatorial_district=row["SENATORIAL DISTRICT"],
                    federal_constituency= row["FEDERAL CONSTITUENCY"],
                    state_constituency=row["STATE CONSTITUENCY"],
                    lga=row["LGA"],
                    lga_code=row["LGACODE"],
                    ward=row["WARD"],
                    polling_unit=row["POLLING UNIT"],
                    polling_unit_code=row["PUCODE"]      
                )
                location_ids.append(location_id)
            for party in parties:
                if row[party]:
                    try:
                        single_candidate =  Candidate.objects.get(name=row[party])
                        
                    except Candidate.DoesNotExist:
                        single_candidate = Candidate.objects.create(
                            # position=row['POSITION'],
                            name=row[party],
                            party=party,
                            # year=year,
                        )
                    
                    
                    try:
                        position = Position.objects.get(name=row['POSITION'])
                    except Position.DoesNotExist:
                        position = Position.objects.create(name=row['POSITION'])
                    
                    try:
                        running_position = RunningPosition.objects.get(position=position, year=year)
                    except:
                        running_position = RunningPosition.objects.create(position=position, year=year)
                    # for location in location_ids:
                    single_candidate.location.set(location_ids)
                    single_candidate.position.add(running_position)
                    single_candidate.save()
        file.message = 'Data upload Successful'
        file.status =  'Success'
        file.save()             
    except Exception as e:
        print('here')
        file.message = 'Failed to upload names: '+ str(e)
        file.status = 'Failed'
        file.save()