from django.db import models
from django.core.urlresolvers import reverse
import datetime
from multiselectfield import MultiSelectField
from django.utils import timezone


class Candidates(models.Model):
	c_id = models.AutoField(primary_key=True)
	first_name = models.CharField(max_length=30)
	#middle_name = models.CharField(max_length=30, blank=True, null=True)
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

	def __str__(self):
		return ("%s %s %s"%(self.first_name, self.middle_name, self.last_name))


	class Meta:
		#preventing duplicates entry of candidates
		unique_together = ['first_name', 'last_name','dob']




	
class Election_Info(models.Model):
	e_id = models.AutoField(primary_key=True)
	#candidates_choice = models.ForeignKey(Candidates)
	CANDIDATES_CHOICE = (('Sakura Haruna', 'Sakura Haruna'),
		('Sasuke Uchiha','Sasuke Uchiha'),
		('Uzumaki Naruto','Uzumaki Naruto'),
		('Buttercup Oie', 'Buttercup Oie'),
		)
	candidates_choice = MultiSelectField(choices=CANDIDATES_CHOICE, max_length=50)
	e_name = models.CharField(max_length=100)
	e_description = models.TextField()
	YEAR_DROPDOWN =[]
	for y in range(2006, (datetime.datetime.now().year +5)):
		YEAR_DROPDOWN.append((y,y))
	year = models.IntegerField(choices=YEAR_DROPDOWN, default=datetime.datetime.now().year)

	POSITION_CHOICE = (('Precinct committeewoman, committeeman','Precinct committeewoman, committeeman'),
		('School Board Member/School Board President','School Board Member/School Board President'),
		('Township/Village Trustee/Town Council', 'Township/Village Trustee/Town Council'),
		('At-Large Councilwoman/man', 'At-Large Councilwoman/man'),
		('City Ward Councilwoman/man','City Ward Councilwoman/man'),
		('President of City Council', 'President of City Council'),
		('City Law Director', 'City Law DIrector'),
		('City Auditor', 'City Auditor'),
		('City Treasurer', 'City Treasurer'),
		('City Manager','City Manager'),
		('Clerk of Court', 'Clerk of Court'),
		('Common Pleas Court Judge','Common Pleas Court'),
		('County Recorder', 'County Recorder'),
		('County Coroner', 'County Coroner'),
		('County Prosecuting Attorney', 'County Prosecuting Attorney'),
		('County Treasurer', 'County Treasurer'),
		('County Engineer', 'County Engineer'),
		('County Auditor', 'County Auditor'),
		('County Executives', 'County Execitives'),
		('Board of County Commissioners', 'Board of County Comissioner'),
		('Democrat/Republican State Central Committee', 'Democrat/Republican State Central Committee'),
		('State Representative', 'State Representative'),
		('State Senator', 'State Senator'),
		)
	position = models.CharField(max_length=50, choices=POSITION_CHOICE)
	PRECINCT_CHOICE = []

	for x in range(50000,52809,101):
		code_x = x+1;
		code_y = code_x+100;
		pre_range = str(code_x) + " - " + str(code_y)

		PRECINCT_CHOICE.append((pre_range,pre_range))

	precincts_range = MultiSelectField(choices=PRECINCT_CHOICE)
	start_date = models.DateField()
	end_date = models.DateField()

	def __int__(self):
		return self.e_id


class Question(models.Model):
	question_text = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')

	def __str__(self):
		return self.question_text

	def was_published_recently(self):
		return self.pub_date >= timezone.now() - datetime.timedelta(days=1)



class Choice(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	choice_text = models.CharField(max_length=200)
	votes = models.IntegerField(default=0)

	def __str__(self):
		return self.choice_text






	
	

