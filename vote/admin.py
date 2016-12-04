from django.contrib import admin
from .models import Candidates, Election_Info

# Register your models here.

class CandidatesAdmin(admin.ModelAdmin):
	list_display = ('first_name', 'last_name', 'party_affiliate')
admin.site.register(Candidates, CandidatesAdmin)

class Election_InfoAdmin(admin.ModelAdmin):
	list_display=('e_id', 'e_name','position','start_date', 'end_date')
admin.site.register(Election_Info, Election_InfoAdmin)










