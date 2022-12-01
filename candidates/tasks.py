
import pandas as pd
from celery import shared_task
from django.conf import settings

from .models import (Candidate, CandidateFile, Location, Position,
                     RunningPosition, Party)


@shared_task
def add_candidates_to_db(saved_file_id, parties, year):
  
    file = CandidateFile.objects.get(id=saved_file_id)
    try:
        candidates_locations = pd.read_excel(file.file.url)
        # candidates_informations = pd.read_excel(file.file.url, 'Sheet2')
        
        
        # if file_extension == '.xlsx':   
        #     reader = pd.read_excel(file)
        # elif file_extension == '.csv':
        #     reader = pd.read_csv(file)
        location_ids = []
        
        # reader = json.loads(reader_)
        for _, row in candidates_locations.iterrows():
            
            try:
                location_id = Location.objects.get(polling_unit_code=row['PUCODE'])
                location_ids.append(location_id)

            except Location.DoesNotExist:
                location_id = Location.objects.create(
                    year=year,
                    state=row["STATE"],
                    # state_code=row["STATECODE"],
                    # senatorial_district=row["SENATORIAL DISTRICT"],
                    # federal_constituency= row["FEDERAL CONSTITUENCY"],
                    # state_constituency=row["STATE CONSTITUENCY"],
                    lga=row["LGA"],
                    # lga_code=row["LGACODE"],
                    ward=row["WARD"],
                    polling_unit=row["POLLING UNIT"],
                    polling_unit_code=row["PUCODE"]      
                )
                location_ids.append(location_id)
            for party_name in parties:
                party_name_capitalize = party_name.capitalize()
                party, created = Party.objects.get_or_create(name=party_name_capitalize)
                if row[party_name]:
                    try:
                        single_candidate =  Candidate.objects.get(name=row[party_name])
                        single_candidate.party=party
                    except Candidate.DoesNotExist:
                        single_candidate = Candidate.objects.create(
                            name=row[party_name],
                            party=party,
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
        print(e)
        file.message = 'Failed to upload names: '+ str(e)
        file.status = 'Failed'
        file.save()



@shared_task
def add_candidates_data_to_db(saved_file_id):
    file = CandidateFile.objects.get(id=saved_file_id)
    try:
        candidates_details = pd.read_excel(file.file.url)
        
        for _,row in candidates_details.iterrows():
            try:
                candidate, created = Candidate.objects.get_or_create(name=row['NAME'])
                age = row['AGE']
                
                if type(age) == int:
                    candidate.age = age
                else:
                    candidate.age = 0
                
                if row['GENDER'] == 'M':
                    candidate.gender = 'Male'
                candidate.gender = 'Female'
                candidate.qualifications = row['QUALIFICATION']
                candidate.save() 
            except Exception as error:
                file.message = 'Failed to upload details: '+ str(error)
                file.status =  'Failed'
                file.save()
                raise Exception('Failed to upload details: '+ str(error))  
        file.message = 'Data upload Successful'
        file.status =  'Success'
        file.save()         
    except Exception as error:
        file.message = 'Failed to upload details: '+ str(error)
        file.status =  'Failed'
        file.save()
        raise Exception('Failed to upload details: '+ str(error))
    