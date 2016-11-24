from django.db import models
from django.core.urlresolvers import reverse

class Candidates(models.Model):
	c_id = models.AutoField(primary_key=True)
	first_name = models.CharField(max_length=30)
	middle_name = models.CharField(max_length=30, blank=True, null=True)
	last_name = models.CharField(max_length=30)
	dob = models.DateField()
	c_image = models.ImageField()
	PARTY_AFFILIATE = (
		('Democratic', 'Democratic'),
		('Republican', 'Republican'),
		('Third Party', 'Third Party'),
		)
	party_affiliate = models.CharField(max_length=11, choices=PARTY_AFFILIATE)
	description = models.TextField();

	def get_absolute_url(self):
		return reverse('vote.views.candidates_detail', args=[str(self.c_id)])


	def __int__(self):
		return self.c_id


	class Meta:
		#preventing duplicates entry of candidates
		unique_together = ['first_name', 'middle_name', 'last_name','dob']


	
		
	
	

