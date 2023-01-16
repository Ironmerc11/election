from .models import Candidate, Location, Position


def get_filter_data(filter, state, senatorial_district, federal_constituency,
                    state_constituency, lga, ward, polling_unit):
    if filter.lower() == 'year':
        return list(set(Location.objects.all().values_list('year', flat=True))).sort()
    if filter.lower() == 'position':
        return list(set(Position.objects.all().values_list('name', flat=True))).sort()
    if filter.lower() == 'party':
        return list(set(Candidate.objects.all().values_list('party', flat=True))).sort()
    if filter.lower() == 'qualification':
        return list(set(Candidate.objects.all().values_list('qualifications', flat=True))).sort()
    if filter.lower() == 'state':
        return list(set(Location.objects.all().values_list('state', flat=True))).sort()
    if filter.lower() == 'senatorial_district':
        return list(set(Location.objects.filter(state=state).values_list('senatorial_district', flat=True))).sort()
    if filter.lower() == 'federal_constituency':
        if state:
            return list(set(Location.objects.filter(state=state).values_list('federal_constituency', flat=True))).sort()

        return list(set(
            Location.objects.filter(senatorial_district=senatorial_district).values_list('federal_constituency',
                                                                                         flat=True))).sort()
    if filter.lower() == 'state_constituency':
        if state:
            return list(set(Location.objects.filter(state=state).values_list('state_constituency', flat=True))).sort()
        return list(set(
            Location.objects.filter(federal_constituency=federal_constituency).values_list('state_constituency',
                                                                                           flat=True))).sort()
    if filter.lower() == 'lga':
        if state:
            return list(set(Location.objects.filter(state=state).values_list('lga', flat=True))).sort()
        return list(
            set(Location.objects.filter(state_constituency=state_constituency).values_list('lga', flat=True))).sort()
    if filter.lower() == 'ward':
        if state:
            return list(set(Location.objects.filter(state=state).values_list('ward', flat=True))).sort()
        return list(set(Location.objects.filter(lga=lga).values_list('ward', flat=True))).sort()
    if filter.lower() == 'polling_unit':
        if state:
            return list(set(Location.objects.filter(state=state).values_list('polling_unit', flat=True))).sort()
        return list(set(Location.objects.filter(ward=ward).values_list('polling_unit', flat=True))).sort()
