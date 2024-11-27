from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from .models import Booking
import json
from datetime import datetime

@csrf_exempt
def bookings(request):
    if request.method == "POST":
        data = json.load(request)
        exists = Booking.objects.filter(
            reservation_date=data["reservation_date"],
            reservation_slot=data["reservation_slot"]
        ).exists()
        
        if not exists:
            booking = Booking(
                first_name=data["first_name"],
                reservation_date=data["reservation_date"],
                reservation_slot=data["reservation_slot"]
            )
            booking.save()
            return HttpResponse(
                json.dumps({"success": True}),
                content_type="application/json"
            )
        else:
            return HttpResponse(
                json.dumps({"error": 1}),
                content_type="application/json"
            )

    date = request.GET.get("date", datetime.today().date())
    bookings = Booking.objects.filter(reservation_date=date)
    bookings_json = serializers.serialize("json", bookings)
    return HttpResponse(bookings_json, content_type="application/json")
