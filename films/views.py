from django.shortcuts import render,redirect
from .models import Film
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from . import forms

def filmlist(request):
	films = Film.objects.all().order_by('date')
	return render(request,'films/film_list.html',{'films':films})

def film_details(request,slug):
	#return HttpResponse(slug)
	film = Film.objects.get(slug=slug)
	return render(request,'films/film_detail.html',{'film':film})

@login_required(login_url="/accounts/login")
def film_create(request):
	if request.method == 'POST':
		form = forms.CreateFilm(request.POST,request.FILES)
		if form.is_valid():
			#save in db
			instance = form.save(commit=False)
			instance.author = request.user
			instance.save()
			return redirect('films:list')
	else:
		form = forms.CreateFilm()
	return render(request,'films/film_create.html',{'form':form})
