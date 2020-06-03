from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
	'''
	This declares the variables that Django will update in auth_user table in mysitedb. Although a sample user "ro" was created to allow
	this user to use and authenticate himself using login.html.
	Connection map is: login.html -> views.py -> forms.py.

	The database entries can be displayed using:
	(my_env) redhat@ubuntu:/media/redhat/apps/Django_Project$ sudo -i -u postgres
	postgres@ubuntu:~$ psql -h localhost -U dbadmin -d mysitedb
	mysitedb=# select * from auth_user;
	In the output: Table entry for "ro" can be seen. 
	'''
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):											# Inherit ModelForm from Django forms.
    password = forms.CharField(label='Password', widget=forms.PasswordInput)			# Takes two named parameters. 
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User 																	# Use User model in ModelForm class.
        fields = ('username', 'first_name', 'email')									# Use these 3 fields from User model.

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']



class ListVMForm(forms.Form):
	SubId = forms.SlugField(required=True)


class CreateVMForm(forms.Form):
	SubId  			= forms.SlugField(required=True)
	ResourceGroup	= forms.CharField(required=True)
	VmName			= forms.CharField(required=True)
	UserName		= forms.CharField(required=False)
	PassWord 		= forms.CharField(required=False)


class ShutDownVMForm(forms.Form):
	SubId  			= forms.SlugField(required=True)
	ResourceGroup	= forms.CharField(required=True)
	VmName			= forms.CharField(required=True)


class StartVMForm(forms.Form):
	SubId  			= forms.SlugField(required=True)
	ResourceGroup	= forms.CharField(required=True)
	VmName			= forms.CharField(required=True)

class AzureUsageForm(forms.Form):
	SubId = forms.SlugField(required=True)