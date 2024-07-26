from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_migrate


class Contacts(models.Model):
    full_name = models.CharField(max_length=100)
    neighborhood = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name
    
    @receiver(post_migrate)
    def create_register(sender, **kwargs):
        if not Contacts.objects.exists():
            Contacts.objects.create(
                full_name = 'Rogério Cerqueira da Silva',
                neighborhood = "Coroa",
                phone = "71986881943",
                city = "Vera Cruz"
            )


class Message(models.Model):
    text = models.TextField()
    image = models.ImageField(upload_to='messages/', null=True, blank=True)
    video = models.FileField(upload_to='messages/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)