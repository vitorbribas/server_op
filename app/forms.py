from django.forms import forms, ModelForm

from app.models import Feature


class FeatureForm(ModelForm):
    class Meta:
        model = Feature
        fields = ['probability']