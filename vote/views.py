from django.shortcuts import render,redirect, HttpResponseRedirect, get_object_or_404
from django.contrib.auth import(
	authenticate, 
	get_user_model,
	login,
	logout)
from django.contrib import messages
from django.contrib.sessions.models import Session
from .forms import UserLoginForm, UserRegistrationForm, CandidatesForm
from .models import Candidates


# Create your views here.
def landing_view(request):
	if 'user_name' in request.session:
		user_name = request.session['user_name']
	else: 
		user_name = ""

	return render(request, 'vote/landing_page.html', {
		'username':user_name})

def login_view(request):
	title='Login'
	username=""
	form = UserLoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get('username')
		password = form.cleaned_data.get('password')
		user = authenticate(username=username, password=password)
		request.session['user_name'] = user.username
		if (user.is_staff):
			login(request, user)
			#return render(request, 'vote/welcome_staff.html', {'username':username})
			return redirect('/admin/staff/%s'% user.username)


		#print(request.user.is_authenticated())
		#return render(request,'vote/welcome.html', {'username':username})
		return redirect('/user/%s'% user.username)



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


def staff_view(request, username):
	form = CandidatesForm()
	context = {
	'username':username,
	'form': form,

	}
	return render(request, 'vote/welcome_staff.html', context)

def user_view(request, username):
	return render(request, 'vote/welcome_users.html', {'username':username})



def register_view(request):
	#print(request.user.is_authenticated())
	title = "Register"
	form = UserRegistrationForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		user = form.save(commit=False)
		password = form.cleaned_data.get('password')
		user.set_password(password)
		new_user = authenticate(username=user.username, password=password)
		user.save()
		login(request, user)
		return render(request,'vote/welcome_users.html', {'username':user.username})

	


	context={
		'form': form, 
		'title': title,
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
		
			return redirect("/candidates_detail/%s/" % candidate.c_id)
		else: 
			print("form is not valid")


	
	else:
		form = CandidatesForm()
		username=""
		context={
			'form':form,
			'username': user_name
		}
	return render(request, 'vote/post_candidates.html', context)


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

	








	
