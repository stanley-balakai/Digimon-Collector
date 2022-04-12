from dataclasses import fields
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Digimon, Toy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import FeedingForm
from django.views.generic import ListView, DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

# class Digimon:
#     def __init__(self, name, type, pforms, number):
#         self.name = name
#         self.type = type 
#         self.pforms = pforms
#         self.number = number

# digimon = [
#     Digimon('Koromon', 'Lesser', 'Botamon', 1),
#     Digimon('Pumpkinmon', 'Puppet', 'Bakemon', 76),
#     Digimon('WereGarurumon', 'Beastman', 'Garurumon', 56),
#     Digimon('MetalGreymon', 'Cyborg', 'Greymon', 54)
# ]

class DigimonCreate(LoginRequiredMixin, CreateView):
    model = Digimon
    fields = ['name','type', 'pforms', 'number', 'picture']
   
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


def home(request):
    return render(request, 'home.html')
    
def about(request):
    return render(request, 'about.html')

@login_required
def digimon_index(request):
    digimon = Digimon.objects.filter(user = request.user)
    return render(request, 'digimon/index.html', { 'digimon': digimon})

@login_required
def digimon_detail(request, digimon_id):
    digimon = Digimon.objects.get(id=digimon_id)
    toys_digimon_doesnt_have = Toy.objects.exclude(id__in = digimon.toys.all().values_list('id'))
    feeding_form = FeedingForm()
    return render(request, 'digimon/detail.html', {'digimon': digimon, 'feeding_form': feeding_form, 'toys': toys_digimon_doesnt_have})

@login_required
def add_feeding(request, digimon_id):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.digimon_id = digimon_id
        new_feeding.save()
    return redirect('detail', digimon_id =digimon_id)    

class DigimonUpdate(LoginRequiredMixin, UpdateView):
    model = Digimon 
    fields = ['name', 'type', 'number', 'picture']

class DigimonDelete(LoginRequiredMixin, DeleteView):
    model = Digimon
    success_url = '/digimon/'

class ToyList(LoginRequiredMixin, ListView):
    model = Toy

class ToyDetail(LoginRequiredMixin, DetailView):
    model =Toy

class ToyCreate(LoginRequiredMixin, CreateView):
    model = Toy
    fields = '__all__'

class ToyUpdate(LoginRequiredMixin, UpdateView):
    model = Toy
    fields = '__all__'

class ToyDelete(LoginRequiredMixin, DeleteView):
    model = Toy
    success_url = '/toys/'

@login_required
def assoc_toy(request, digimon_id, toy_id):
    Digimon.objects.get(id=digimon_id).toys.add(toy_id)
    return redirect('detail', digimon_id=digimon_id)

@login_required
def unassoc_toy(request, digimon_id, toy_id):
    Digimon.objects.get(id=digimon_id).toys.remove(toy_id)
    return redirect('detail', digimon_id=digimon_id)


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Save the user to the database
            user = form.save()
            # Login the user
            login(request, user)
            return redirect('index')
        else:
            error_message ="Invalid signup - try again"
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)