from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render


def index(request):
    return HttpResponse("This is the Homepage, have fun!")


