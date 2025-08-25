import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_admin = models.BooleanField(default=False)
    email = models.EmailField()
    contact_no = models.CharField(max_length=10)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.FileField(upload_to="uploads/", blank=True, null=True)


def __str__(self):
    return self.name


class FormFieldChoices:
    CHOICES = (
        ('text', 'Text'),
        ('textarea', 'Textarea'),
        ('number', 'Number'),
        ('email', 'Email'),
        ('select', 'Select'),
        ('radio', 'Radio'),
        ('checkbox', 'Checkbox'),
        ('date', 'Date'),
    )

class Form(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class FormField(models.Model):
    form = models.ForeignKey(Form, related_name='fields', on_delete=models.CASCADE)
    label = models.CharField(max_length=255)
    field_type = models.CharField(max_length=50, choices=FormFieldChoices.CHOICES)
    required = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.form.name} - {self.label}"


class FormSubmission(models.Model):
    form = models.ForeignKey(Form, related_name='submissions', on_delete=models.CASCADE)
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)


class FormSubmissionData(models.Model):
    submission = models.ForeignKey(FormSubmission, related_name='data', on_delete=models.CASCADE)
    field = models.ForeignKey(FormField, on_delete=models.CASCADE)
    value = models.TextField(blank=True, null=True)
