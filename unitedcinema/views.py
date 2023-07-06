from django.http import HttpResponse
from django.shortcuts import render

def homepage(request):
	#return HttpResponse('homepage')
	return render(request,'index.html')

def about(request):
	#return HttpResponse('aboutpage')
	return render(request,'about.html')