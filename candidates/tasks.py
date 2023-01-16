from io import StringIO

import pandas as pd
from celery import shared_task

from celery import Celery
from celery.schedules import crontab


from .models import (Candidate, CandidateFile, Location, Position,
                     RunningPosition, Party, ExcelFileData)


# import json
# import dramatiq


def read_excel(path, sheet_name):
    buffer = StringIO()
    read_file = pd.read_excel(path, sheet_name=sheet_name)
    read_file.to_csv(buffer, index=None, header=True)
    # Xlsx2csv(path, outputencoding="utf-8", sheet_name=sheet_name).convert(buffer)
    buffer.seek(0)
    df = pd.read_csv(buffer)
    return df

# @shared_task(name='excel_to_db')
# def add_candidate_data_to_excel_file_db():
#     unread_info = ExcelFileData.objects.filter(read=False)
#
#     for _ in unread_info:
#         for row in _.data:






@shared_task(name='excel_to_db')
# @dramatiq.actor
def add_candidates_to_db():
    # file = CandidateFile.objects.get(id=saved_file_id)
    files = ExcelFileData.objects.filter(read=False)
    count = 0

        # df = pd.read_excel(file.file.url)
        # df = read_excel(path=file.file.url, sheet_name='Sheet1')
        # candidates_informations = pd.read_excel(file.file.url, 'Sheet2')

        # if file_extension == '.xlsx':
        #     reader = pd.read_excel(file)
        # elif file_extension == '.csv':
        #     reader = pd.read_csv(file)
    location_ids = []
    candidates = []
    for file in files:
        try:
            for row in file.data:

                try:

                    # Location.objects.get_or_create(poll)
                    location_id = Location.objects.get(polling_unit_code=row['PUCODE'])
                    # location_ids.append(location_id)

                except Location.DoesNotExist:
                    location_id = Location.objects.create(
                        year=file.year,
                        state=row["STATE"],
                        lga=row["LGA"],
                        ward=row["WARD"],
                        polling_unit=row["POLLING UNIT"],
                        polling_unit_code=row["PUCODE"]
                    )
                location_ids.append(location_id)
                if count <= 0:
                    for party_name in file.parties:
                        party_name_capitalize = party_name.capitalize()
                        party, created = Party.objects.get_or_create(name=party_name_capitalize)
                        if row[party_name]:
                            try:
                                single_candidate = Candidate.objects.get(name=row[party_name])
                                single_candidate.party = party
                                single_candidate.save()
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
                                running_position = RunningPosition.objects.get(position=position, year=file.year)
                            except RunningPosition.DoesNotExist:
                                running_position = RunningPosition.objects.create(position=position, year=file.year)

                            single_candidate.position.add(running_position)
                            candidates.append(single_candidate)

                        count += 1
                        # for location in location_ids:
                        # print(location_ids)

            for candidate in candidates:
                candidate.location.add(*location_ids)
            file.message = 'Data upload Successful'
            file.status = 'Success'
            file.read = True
            file.save()
        except Exception as e:
            print(e)
            file.message = 'Failed to upload names: ' + str(e)
            file.status = 'Failed'
            file.read = True
            file.save()


@shared_task
# @dramatiq.actor
def add_candidates_data_to_db(saved_file_id, df):
    file = CandidateFile.objects.get(id=saved_file_id)
    try:
        # candidates_details = pd.read_excel(file.file.url)

        for _, row in df:
            try:
                candidate, created = Candidate.objects.get_or_create(name=row['NAME'])
                age = row['AGE']

                if type(age) == int:
                    candidate.age = age
                else:
                    candidate.age = 0

                if row['GENDER'] == 'M':
                    candidate.gender = 'Male'
                else:
                    candidate.gender = 'Female'
                candidate.qualifications = row['QUALIFICATION']
                candidate.save()
            except Exception as error:
                file.message = 'Failed to upload details: ' + str(error)
                file.status = 'Failed'
                file.save()
                raise Exception('Failed to upload details: ' + str(error))
        file.message = 'Data upload Successful'
        file.status = 'Success'
        file.save()
    except Exception as error:
        file.message = 'Failed to upload details: ' + str(error)
        file.status = 'Failed'
        file.save()
        raise Exception('Failed to upload details: ' + str(error))



