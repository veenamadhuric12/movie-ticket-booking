from django.shortcuts import render,redirect,get_object_or_404
from .forms import RegisterForm
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate,login,logout
from . models import Movie,ShowTime,Booking,Theater,Seat
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

def register(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            print("successful")
            return redirect('login')
    return render(request,'register.html',{'form':form})

def log_in(request):
    if request.method == "POST":
        a = request.POST.get('un')
        b = request.POST.get('pwd')
        print(a,b)

        try:
            u = User.objects.get(username = a)
            print("user found" ,u)
        except Exception as e:
            print(e)
        
        u = authenticate(request,username = a,password = b)
        print(u)

        if u is not None:
            print("credentials are correct")
            login(request,u)
            print("login successful")
            return redirect('list')
        else:
            print("Enter valid username and password")
    return render(request,'login.html')

        
def log_out(request):
    logout(request)
    return redirect('login')
    
def movie_list(request):
    movies = Movie.objects.all()
    if request.method == "POST":
        search = request.POST.get("search")
        print(search)
        movies = Movie.objects.filter(title__icontains = search)
        print(movies)
    context = {
        'movies':movies
    }
    return render(request,'movie_list.html',context)

def movie_details(request,movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    context = {
        'movie':movie
    }
    return render(request,'movie_details.html',context)


def showtime_list(request,movie_id):
    theater = Theater.objects.all()
    showtime = ShowTime.objects.filter(movie = movie_id)
    movie = get_object_or_404(Movie, pk=movie_id)
    context = {
        'movie': movie,
        'theater':theater,
        'showtime': showtime
    }
    return render(request,'showtime_list.html',context)

@login_required(login_url='login')
def select_tickets(request, showtime_id):
    showtime = get_object_or_404(ShowTime, pk=showtime_id)

    if request.method == 'POST':
        tickets = int(request.POST.get('tickets'))
        request.session['tickets'] = tickets
        request.session['showtime_id'] = showtime_id
        return redirect('select_seats', showtime_id=showtime_id)

    return render(request, 'select_tickets.html', {'showtime': showtime})

@login_required(login_url='login')
def select_seats(request, showtime_id):
    showtime = get_object_or_404(ShowTime, pk=showtime_id)
    seats = Seat.objects.filter(show_time=showtime).order_by('row', 'number')
    ticket_count = int(request.session.get('tickets', 1))
    error = None

    if request.method == "POST":
        selected_seats = request.POST.getlist('selected_seats')
        if len(selected_seats) == ticket_count:
            # Create booking
            total_price = showtime.price * ticket_count
            booking = Booking.objects.create(
                user=request.user,
                show_time=showtime,
                total_price=total_price
            )

            # Mark seats booked
            booked_seats = []
            for seat_id in selected_seats:
                seat = Seat.objects.get(id=seat_id)
                seat.is_booked = True
                seat.save()
                booking.seats.add(seat)
                booked_seats.append(seat)

            messages.success(request, "Seats booked successfully!")

            return redirect('confirmation', booking_id=booking.id)
        else:
            error = f"You must select exactly {ticket_count} seat(s)."

    context = {
        'showtime_id': showtime_id,
        'seats': seats,
        'error': error,
        'ticket_count': ticket_count
    }
    
    return render(request, 'select_seats.html', context)

def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    seats = booking.seats.all()
    context = {
        'booking':booking,
        'seats':seats
    }
    return render(request, 'booking_confirmation.html', context)

def add_seats():
    showtimes = ShowTime.objects.all()
    for showtime in showtimes:
        if not Seat.objects.filter(show_time=showtime).exists():
            for row in range(1, 6):  # Rows A to E
                for num in range(1, 11):  # 10 seats per row    
                    Seat.objects.create(
                        show_time=showtime,
                        row=chr(64 + row),
                        number=num,
                        is_booked=False
                    )
            print(f"Added 50 seats for {showtime}")

add_seats()