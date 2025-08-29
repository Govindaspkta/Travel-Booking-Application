import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from core.models import TravelOption  # adjust if your model is in another app


class Command(BaseCommand):
    help = "Seed the database with random travel options (flights, buses, trains)."

    def handle(self, *args, **kwargs):
        types = ["Flight", "Bus", "Train"]
        sources = ["Kathmandu", "Pokhara", "Biratnagar", "Butwal", "Chitwan"]
        destinations = ["Pokhara", "Kathmandu", "Birgunj", "Janakpur", "Lumbini"]

        for _ in range(20):  # generate 20 random travel options
            travel_type = random.choice(types)
            source = random.choice(sources)
            destination = random.choice([d for d in destinations if d != source])

            date_time = timezone.now() + timedelta(days=random.randint(1, 30),
                                                   hours=random.randint(0, 23))
            price = random.randint(500, 5000)
            seats = random.randint(0, 50)

            TravelOption.objects.create(
                type=travel_type,
                source=source,
                destination=destination,
                date_time=date_time,
                price=price,
                available_seats=seats,
            )

        self.stdout.write(self.style.SUCCESS("✅ Successfully seeded travel options!"))
