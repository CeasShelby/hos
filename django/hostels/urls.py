# hostels/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Ensure the name is 'hostel-index'
    path('list/', views.hostel_list, name='hostel-index'),
    path('add/', views.add_hostel, name='add-hostel'),
    path('<int:pk>/', views.hostel_detail, name='hostel_detail'),
    path('book/<int:pk>/', views.book_hostel, name='book-hostel'),
    path('my-bookings/', views.my_bookings, name='my-bookings'),
    path('booking/delete/<int:pk>/', views.delete_booking, name='delete-booking'),
    path('recommendations/', views.hostel_recommendations, name='recommendations'),
    path('proposals/send/<int:receiver_id>/', views.send_proposal, name='send_proposal'),
    path('inbox/', views.proposals_inbox, name='proposals_inbox'),
    path('proposals/<int:proposal_id>/<str:action>/', views.handle_proposal, name='handle_proposal'),
] 