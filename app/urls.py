from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/',views.register,name='register'),
    path('login/',views.log_in, name='login'),
    path('logout/',views.log_out, name='logout'),
    path('',views.movie_list,name='list'),
    path('details/<int:movie_id>',views.movie_details,name='details'),
    path('show_list/<int:movie_id>',views.showtime_list,name='show_list'),
    path('tickets/<int:showtime_id>',views.select_tickets,name='tickets'),
    path('seats/<int:showtime_id>',views.select_seats,name='select_seats'),
    path('confirmation/<int:booking_id>',views.booking_confirmation,name='confirmation'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)