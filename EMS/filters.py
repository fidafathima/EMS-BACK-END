from django_filters import rest_framework as filters

from .models import FormSubmission


class FormFilter(filters.FilterSet):
    class Meta:
        model = FormSubmission
        fields = {
            "form__name": ["icontains"],
        }
