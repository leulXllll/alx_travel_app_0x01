from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from .models import Listing, Booking
from .serializers import ListingSerializer, BookingSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly # Example permission

class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly] # Example: Allow read-only for unauthenticated users, full access for authenticated.

    # You can add custom logic here if needed, e.g., to filter listings by the current user
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user) # Automatically set the owner to the current user on creation

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly] # Example permission

    # You might want to filter bookings to only show those related to the current user
    def get_queryset(self):
        # Only show bookings made by or for the current user
        if self.request.user.is_authenticated:
            return Booking.objects.filter(guest=self.request.user) | Booking.objects.filter(listing__owner=self.request.user)
        return Booking.objects.none() # Or whatever makes sense for unauthenticated users

    def perform_create(self, serializer):
        serializer.save(guest=self.request.user) # Automatically set the guest to the current user on creation