from django.shortcuts import render,redirect, HttpResponseRedirect
from django.contrib.auth import(
	authenticate, 
	get_user_model,
	login,
	logout)
from .forms import UserLoginForm, UserRegistrationForm


# Create your views here.
def landing_view(request):
	return render(request, 'vote/landing_page.html', {})

def login_view(request):
	title='Login'
	form = UserLoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get('username')
		password = form.cleaned_data.get('password')
		user = authenticate(username=username, password=password)
		if (user.is_staff):
			login(request, user)
			return render(request, 'vote/welcome_staff.html', {'username':username})


		#print(request.user.is_authenticated())
		return render(request,'vote/welcome.html', {'username':username})



	return render(request,'vote/login.html', {'form':form, 'title': title})

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
		return render(request,'vote/welcome.html', {'username':user.username})
	


	context={
		'form': form, 
		'title': title,
	}

	return render(request, 'vote/registration_form.html', context)

def logout_view(request):
	title='Login'
	form = UserLoginForm(request.POST or None)
	logout(request)
	return redirect('/')




	








	
