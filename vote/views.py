from django.shortcuts import render,redirect, HttpResponseRedirect, get_object_or_404
from django.contrib.auth import(
	authenticate, 
	get_user_model,
	login,
	logout)
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.sessions.models import Session
from .forms import UserLoginForm, UserRegistrationForm, CandidatesForm, Election_InfoForm
from .models import Candidates, Election_Info


# Create your views here.
def landing_view(request):
	user_name = get_username(request)
	u_id = get_uid(request)
	context = {
	'username': user_name,
	'u_id': u_id,
	}
	return render(request, 'vote/landing_page.html', context)

def login_view(request):
	title='Login'
	username=""
	form = UserLoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get('username')
		password = form.cleaned_data.get('password')
		user = authenticate(username=username, password=password)
		request.session['user_name'] = user.username
		request.session['u_id'] = user.pk
		u_id = user.pk
		#print("primary key :" + str(u_id))
		if (user.is_staff):
			login(request, user)
			#return render(request, 'vote/welcome_staff.html', {'username':username})
			return redirect('/admin/staff/%s'% user.username)
		#print(request.user.is_authenticated())
		#return render(request,'vote/welcome.html', {'username':username})
		return redirect('/user/%s'% u_id)
	return render(request,'vote/login.html', {'form':form, 'title': title, 'username': username})

def candidates(request):
	if 'user_name' in request.session:
		user_name = request.session['user_name']
	else: 
		user_name = ""
	candidates = Candidates.objects.all()
	context = {
	'candidates': candidates,
	'title': 'Candidates list',
	'username': user_name
	}
	return render(request, 'vote/candidates_list.html', context)


def elections(request):
	user_name = get_username(request)
	elections = Election_Info.objects.all()
	context  = {
		'username': user_name,
		'elections': elections,
		'title': 'Election Forms'
	}
	return render(request, 'vote/election_list.html', context)


def staff_view(request, username):
	form = CandidatesForm()
	context = {
	'username':username,
	'form': form,
	}
	return render(request, 'vote/welcome_staff.html', context)

def user_view(request, u_id):
	user = get_object_or_404(User, pk=u_id)
	username = user.username
	u_id = user.pk
	context = {
	'username':username,
	'u_id': u_id
	}
	return render(request, 'vote/welcome_users.html', context)

def register_view(request):
	#print(request.user.is_authenticated())
	title = "Register"
	form = UserRegistrationForm(request.POST or None)
	if form.is_valid():
		user = form.save(commit=False)
		password = form.cleaned_data.get('password')
		user.set_password(password)
		new_user = authenticate(username=user.username, password=password)
		user.save()
		login(request, user)
		u_id=user.pk
		#print("user id = " + str(u_id))
		
		return render(request,'vote/welcome_users.html', {'username':user.username, 'u_id':u_id})
	
	user_name = get_username(request)
	context={
		'form': form, 
		'title': title,
		'username': user_name
	}
	return render(request, 'vote/registration_form.html', context)

def logout_view(request):
	logout(request)
	username = ""
	return render(request, 'vote/logout.html', {'username': username})

def post_candidates(request):
	if 'user_name' in request.session:
		user_name = request.session['user_name']
	else: 
		user_name = ""
	if request.method == 'POST':
		form = CandidatesForm(request.POST or None, request.FILES)
		if form.is_valid():
			candidate = form.save(commit=False)
			candidate.save()
			messages.success(request, "Successfully created!")
			#print(candidate.get_absolute_url())
			#return HttpResponseRedirect(candidate.get_absolute_url())
			context = {
			'button_action':'Update',
			}
			return redirect("/candidates_detail/%s/" % candidate.c_id, context)
		else: 
			print("form is not valid")
	else:
		form = CandidatesForm()
		username=""
		context={
			'form':form,
			'username': user_name,
			'button_action': 'Post' 
		}
	return render(request, 'vote/post_candidates.html', context)
	
def post_election(request):
	user_name = get_username(request)
	can_objs = Candidates.objects.all()
	
	if request.method  == 'POST':
		form = Election_InfoForm(request.POST or None)
		if form.is_valid():
			election = form.save(commit=False)
			election.save()
			messages.success(request, "Successfully created!")
			context = {
				'button_action':'Update',
			}
			return redirect("/admin/election_detail/%s/"%election.e_id)
		else:
			print("form is not valid")
	else:

		form = Election_InfoForm()
		context = {
			'username':user_name,
			'form':form,
			'button_action': 'Post',
			'can_objs': can_objs

		}
	return render(request, 'vote/post_election.html', context)# {'username':user_name,'form':form,'button_action': 'Post'})
	

def user_polls_view(request):
	election_info = Election_Info.objects.all()
	user_name = get_username(request)
	context={
		'username': user_name,
		'title': 'Polls',
		'election_info':election_info

	}
	return render('vote/users_view_poll.html', context) 


def election_detail(request, e_id):
	user_name = get_username(request)
	election_info = get_object_or_404(Election_Info, pk=e_id)
	candidates = election_info.candidates_choice
	precincts_range = election_info.precincts_range
	can_objs = Candidates.objects.all()
	name_list = []
	for can in can_objs:
		name = can.first_name +" " +can.last_name
		c_id = can.c_id
		name_list.append((name,c_id))

	context = {
		'username': user_name,
		'election_info': election_info,
		'candidates': candidates,
		'precincts_range': precincts_range,
		'name_list': name_list
	}
	return render(request, 'vote/election_detail.html', context)

def candidates_detail(request, c_id):

	if 'user_name' in request.session:
		user_name = request.session['user_name']
	else: 
		user_name = ""
	candidate_info = get_object_or_404(Candidates, pk=c_id)
	context = {
	'candidate_info':candidate_info,
	'username': user_name
	}
	return render(request, 'vote/candidates_detail.html', context)

	
def candidates_update(request, c_id=None):
	candidate = get_object_or_404(Candidates, pk=c_id)
	form = CandidatesForm(request.POST or None, instance=candidate )
	if form.is_valid():
		candidate = form.save(commit=False)
		candidate.save()
		messages.success(request, "Successfully updated!")
		return redirect("/candidates_detail/%s/" % candidate.c_id)

	user_name = get_username(request)

	context = {
	'username':user_name,
	'form': form 
	}
	return render(request, 'vote/post_candidates.html', context)

def election_update(request, e_id=None):
	election = get_object_or_404(Election_Info, pk=e_id)
	form = Election_InfoForm(request.POST or None, instance=election )
	if form.is_valid():
		election = form.save(commit=False)
		election.save()
		messages.success(request, "Successfully updated!")
		return redirect("/admin/election_detail/%s/" % election.e_id)

	user_name = get_username(request)

	context = {
	'username':user_name,
	'form': form 
	}
	return render(request, 'vote/post_election.html', context)

def user_info_update(request, u_id=None):
	user = get_object_or_404(User, pk=u_id)
	form = UserRegistrationForm(request.POST or None, instance=user)
	if form.is_valid():
		user = form.save(commit=False)
		user.save()
		messages.success(request, "Successfully updated!")
		return redirect("/user_info/%s/" % u_id)
	user_name = get_username(request)
	title = "Register"
	context = {
	'username':user_name,
	'form':form,
	'title': title,
	'u_id': u_id
	}
	return render(request, 'vote/user_update_form.html', context)

def user_info(request, u_id):
	user_info = get_object_or_404(User, pk=u_id)
	context={
		'u_id': u_id,
		'user_info': user_info,
		'username': user_info.username,
	}
	return render(request, 'vote/user_profile.html', context)

def get_uid(request):
	if 'u_id' in request.session:
		u_id = request.session['u_id']
		return u_id
	else:
		return None

def get_username(request):
	if 'user_name' in request.session:
		user_name = request.session['user_name']
		return user_name
	else: 
		user_name = ""
		return user_name

def candidate_delete_confirmation(request, c_id=None):
	user_name=get_username(request)
	candidate = get_object_or_404(Candidates, pk=c_id)
	context={
	'username': user_name,
	'candidate': candidate,
	}
	return render(request, 'vote/candidate_delete_confirmation.html', context)

def candidate_deleted(request, c_id=None):
	candidate = get_object_or_404(Candidates, pk=c_id)
	first_name = candidate.first_name
	middle_name = candidate.middle_name
	last_name = candidate.last_name
	candidate.delete()
	user_name = get_username(request)
	context = {
	'first_name': first_name,
	'middle_name': middle_name,
	'last_name': last_name,
	'username': user_name,
	}
	return render(request, 'vote/candidate_delete_success.html', context)

def view_candidates(request, u_id):
	user = get_object_or_404(User, pk=u_id)
	username = user.username
	u_id = user.pk
	candidates = Candidates.objects.all()
	context = {
	'candidates': candidates,
	'title': 'Candidates list',
	'username':username,
	'u_id': u_id
	}
	return render(request, 'vote/user_candidates_list.html', context)

def view_candidates_detail(request, u_id, c_id):
	user = get_object_or_404(User, pk=u_id)
	username = user.username
	u_id = user.pk
	candidate_info = get_object_or_404(Candidates, pk=c_id)
	context = {
	'candidate_info':candidate_info,
	'username':username,
	'u_id': u_id
	}
	return render(request, 'vote/user_candidates_detail.html', context)

<<<<<<< HEAD
def user_elections(request, u_id):
	user = get_object_or_404(User, pk=u_id)
	u_id = user.pk
	elections = Election_Info.objects.all()
	context  = {
		'elections': elections,
		'u_id': u_id,
		'title': 'Elections'
	}
	return render(request, 'vote/user_election_list.html', context)
	
def	user_election_detail(request, u_id, e_id):
	user = get_object_or_404(User, pk=u_id)
	u_id = user.pk
	election_info = get_object_or_404(Election_Info, pk=e_id)
	candidates = election_info.candidates_choice
	precincts_range = election_info.precincts_range
	can_objs = Candidates.objects.all()
	name_list = []
	for can in can_objs:
		name = can.first_name +" " +can.last_name
		c_id = can.c_id
		name_list.append((name,c_id))
	context = {
		'u_id': u_id,
		'election_info': election_info,
		'candidates': candidates,
		'precincts_range': precincts_range,
		'name_list': name_list
	}
	return render(request, 'vote/user_election_detail.html', context)

def user_vote_success(request, u_id, e_id):

	return
=======


>>>>>>> 4be75841522696c0ea1d11ed0fc859a6c9bab70b
