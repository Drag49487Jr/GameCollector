from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.
RATINGS = (
    ('E', 'Everyone'),
    ('T', 'Teen'),
    ('M', 'Mature'),
)
class Console(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('consoles_detail', kwargs={'pk':self.id})

class Game(models.Model):
    name = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    review = models.TextField(max_length=250)
    character = models.CharField(max_length=100)
    consoles = models.ManyToManyField(Console)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}|{self.genre}|{self.review}|{self.character}'

    def get_absolute_url(self):
        return reverse('detail', kwargs={'game_id': self.id})
    
class Rating(models.Model):
    date = models.DateField()
    rating = models.CharField(
        max_length=1,
        choices=RATINGS,
        default=RATINGS[0][0],
    )
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_rating_display()} on {self.date}"

    class Meta:
        ordering = ['-date']

class Photo(models.Model):
    url = models.CharField(max_length=200)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    def __str__(self):
            return f'Photo for game_id: {self.game_id} @{self.url}'