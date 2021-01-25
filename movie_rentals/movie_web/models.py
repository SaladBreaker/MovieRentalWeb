import datetime
from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    phone_number = PhoneNumberField(blank=True)
    name = models.CharField(max_length=50, blank=False)
    city = models.CharField(max_length=50, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_active = models.DateTimeField()

    def update_activity_tracker(self):
        self.last_active = datetime.datetime.now()
        logger.info(
            f"Updated last_active of user: {self.user.username} to {self.last_active}"
        )
        self.save()

    def __str__(self) -> str:
        return f"{self.name}"

    @staticmethod
    def get_form_fields():
        """
        Return a list of filds that will be present in the create/update form
        """
        return [
            "name",
            "phone_number",
            "city",
        ]


class Movie(models.Model):
    owner = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
    )
    price = models.FloatField(max_length=20)
    name = models.CharField(max_length=50, blank=False)
    category = models.CharField(max_length=50, blank=False)
    description = models.TextField(max_length=3000, blank=False)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.name}"

    @staticmethod
    def get_form_fields():
        """
        Return a list of filds that will be present in the create/update form
        """
        return [
            "name",
            "category",
            "description",
            "price",
        ]
