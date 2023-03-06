from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['complete']


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    complete = models.BooleanField(default=False)
    completion_date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.title


class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def clean(self):
        if self.end_date <= self.start_date:
            raise ValidationError("End date must be later than start date.")

    def get_absolute_url(self):
        return reverse('calendar', kwargs={'year': self.start_date.year,
                                           'month': self.start_date.strftime('%B')})

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['start_date']

