from django.contrib import admin
from . models import Movie, Theater, ShowTime, Booking, Seat

# Register your models here.

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')

@admin.register(Theater)
class TheaterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(ShowTime)
class ShowTimeAdmin(admin.ModelAdmin):
    list_display = ('id', 'movie', 'theater', 'show_time')

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('id', 'show_time', 'row', 'number', 'is_booked')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'show_time', 'seat_list', 'booking_date', 'total_price')

    def seat_list(self, obj):
        return ", ".join([f"{seat.row}{seat.number}" for seat in obj.seats.all()])
    
    seat_list.short_description = 'Seats'   
