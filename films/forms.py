from django import forms
from . import models

class CreateFilm(forms.ModelForm):
	#title = forms.TextInput()
	#slug = forms.TextInput()
	#synopsis = forms.TextInput()
	#genre = forms.TextInput()
	#date_out = forms.TextInput()
	#format_type = forms.TextInput()
	#thumb = forms.ImageField()
	class Meta:
		model = models.Film
		fields = ['title','slug','synopsis','genre','date_out','format_type','thumb']
