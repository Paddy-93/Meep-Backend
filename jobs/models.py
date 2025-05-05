from django.db import models

# Create your models here.
from django.db import models

class Job(models.Model):
    pickup_location = models.CharField(max_length=100)
    dropoff_location = models.CharField(max_length=100)
    fare = models.DecimalField(max_digits=6, decimal_places=2)
    posted_at = models.DateTimeField(auto_now_add=True)
    is_claimed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.pickup_location} → {self.dropoff_location} (${self.fare})"
