from django.db import models


class Contacts(model.Models):
    full_name = models.CharField(max_length=100)
    neighborhood = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name