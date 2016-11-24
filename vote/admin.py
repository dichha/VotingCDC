from django.contrib import admin
from .models import Candidates

# Register your models here.

class CandidatesAdmin(admin.ModelAdmin):
	list_display = ('first_name', 'middle_name', 'last_name', 'party_affiliate')
admin.site.register(Candidates, CandidatesAdmin)








