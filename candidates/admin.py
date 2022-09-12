from django.contrib import admin
from .models import Candidate, Location, Position, RunningPosition, CandidateFile


admin.site.register(Candidate)
admin.site.register(Location)
admin.site.register(Position)
admin.site.register(RunningPosition)
admin.site.register(CandidateFile)
