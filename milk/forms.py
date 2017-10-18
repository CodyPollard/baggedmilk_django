from django import forms
from django.forms import Select, TextInput

from .models import Timer


class TimerForm(forms.ModelForm):
    class Meta:
        model = Timer
        fields = ('type', 'system', 'end_at')
        widgets = {
            'end_at': forms.TextInput(attrs={'placeholder': 'Ex. 1d13h45m'})
        }

    def clean_end_at(self):
        end_at = self.cleaned_data.get('end_at')
        if '-' in end_at:
            raise forms.ValidationError('Only future timers are allowed.')
        if 'd' not in end_at:
            raise forms.ValidationError('Please add a day to your timer. Ex: 0d12h30m')
        if 'h' not in end_at:
            raise forms.ValidationError('Please add an hour to your timer. Ex: 1d0h30m')
        if 'm' not in end_at:
            raise forms.ValidationError('Please add a minute to your timer. Ex: 1d12h0m')
        return end_at