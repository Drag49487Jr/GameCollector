from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

import uuid
import boto3

from .models import Game, Console, Photo
from .forms import RatingForm

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'catcollector-aas'
# Create your views here.

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def games_index(request):
    games=Game.objects.filter(user=request.user)
    return render(request, 'games/index.html', {'games': games })

@login_required
def games_detail(request, game_id):
    game=Game.objects.get(id=game_id)
    consoles_game_doesnt_play_on = Console.objects.exclude(id__in=game.consoles.all().values_list('id'))
    rating_form = RatingForm()
    return render(request, 'games/detail.html', {
        'game': game,
        'rating_form': rating_form,
        'consoles': consoles_game_doesnt_play_on, 
        })

@login_required
def add_rating(request, game_id):
    form = RatingForm(request.POST)
    if form.is_valid():
        new_rating = form.save(commit=False)
        new_rating.game_id = game_id
        new_rating.save()
    return redirect('detail', game_id=game_id)

@login_required
def assoc_console(request, game_id, console_id):
    game = Game.objects.get(id=game_id)
    game.consoles.add(console_id)
    return redirect('detail', game_id=game_id)

@login_required
def add_photo(request, game_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f'{S3_BASE_URL}{BUCKET}/{key}'
            photo = Photo(url=url, game_id=game_id)
            photo.save()
        except:
            print('An error has occured when uploading a file')
    return redirect('detail', game_id=game_id)

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up!'
    form = UserCreationForm()
    context = {'form':form, 'error_message':error_message}
    return render(request, 'registration/signup.html', context)

class GameCreate(LoginRequiredMixin, CreateView):
    model = Game
    fields = ['name', 'genre', 'review', 'character']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class GameUpdate(LoginRequiredMixin, UpdateView):
    model = Game
    fields = ['genre','review','character']

class GameDelete(LoginRequiredMixin, DeleteView):
    model = Game
    success_url = '/games/'

class ConsoleList(LoginRequiredMixin, ListView):
    model = Console

class ConsoleDetail(LoginRequiredMixin, DetailView):
    model = Console

class ConsoleCreate(LoginRequiredMixin, CreateView):
    model = Console
    fields = '__all__'

class ConsoleUpdate(LoginRequiredMixin, UpdateView):
    model = Console
    fields = ['name']

class ConsoleDelete(LoginRequiredMixin, DeleteView):
    model = Console
    success_url='/games/'
