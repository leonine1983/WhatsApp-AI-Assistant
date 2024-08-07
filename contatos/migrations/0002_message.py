# Generated by Django 5.0.7 on 2024-07-25 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contatos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='messages/')),
                ('video', models.FileField(blank=True, null=True, upload_to='messages/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
