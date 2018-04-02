from django.http import Http404
from django.shortcuts import render, redirect
from random import randint


# D&D Tolls homepage
def index(request):
    return render(request, 'dnd/index.html')


# View for dice-roller tool
def dice(request):
    return render(request, 'dnd/dice.html')

# View for Shops
def shops(request):
    return render(request, 'dnd/shops.html')