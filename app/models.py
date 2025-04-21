from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    release_date = models.DateField()
    duration = models.IntegerField(help_text="Duration in minutes")
    image = models.ImageField(upload_to='movies/')

    def __str__(self):
        return self.title
    
class Theater(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=1000)

    def __str__(self):
        return self.name

class ShowTime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    show_time = models.DateTimeField()
    available_seats = models.IntegerField(default=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.movie.title} at {self.theater.name} ({self.show_time})'
    
class Seat(models.Model):
    show_time = models.ForeignKey(ShowTime, on_delete=models.CASCADE)
    row = models.CharField(max_length=1)  
    number = models.IntegerField() 
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"Row {self.row}, Seat {self.number} ({'Booked' if self.is_booked else 'Available'})"
    
class Booking(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    show_time = models.ForeignKey(ShowTime,on_delete=models.CASCADE)
    seats = models.ManyToManyField(Seat)
    booking_date = models.DateField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=8,decimal_places=2)

    def __str__ (self):
        return f"Booking done by {self.user.username} for {self.show_time.movie.title}"
