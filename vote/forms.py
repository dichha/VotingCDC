from django import forms
from django.contrib.auth import(
	authenticate, 
	get_user_model,
	login,
	logout)
from django.contrib.auth.models import User

class UserLoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)
	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		#authenticating that the user is a real user
		if username and password:
			user = authenticate(username=username, password=password)
			if not user:
				raise forms.ValidationError("This user does not exist")
			if not user.check_password(password):
				raise forms.ValidationError("Incorrect password")
			if not user.is_active:
				raise forms.ValidationError("This user is no longer active")
		return super(UserLoginForm, self).clean(*args, **kwargs)



class UserRegistrationForm(forms.ModelForm):
	email = forms.EmailField(label="Email address")
	email2 = forms.EmailField(label="Confirm email")
	password = forms.CharField(widget=forms.PasswordInput)
	password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm password")

	class Meta:
		model = User
		fields = ['first_name',
		'last_name', 
		'username', 
		'password',
		'password2', 
		'email',
		'email2',]

	def clean_email2(self):
		#print(self.cleaned_data)
		email = self.cleaned_data.get('email')
		email2 = self.cleaned_data.get('email2')
		if not email == email2:
			raise forms.ValidationError("Emails must match")
		email_qs = User.objects.filter(email=email)
		if email_qs.exists():
			raise forms.ValidationError("This email has already been registered")
		return email


	def clean_password2(self):
		#print(self.cleaned_data)
		password = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('password2')
		if not password == password2:
			raise forms.ValidationError("Passwords must match")
		
		return password


