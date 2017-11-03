from django import forms
from .models import Timer, DucksInjury
from django_project.secret import TIMERBOARD_KEY


class TimerForm(forms.ModelForm):

    TYPE_CHOICES = ['EC - Sotiyo', 'EC - Azbel', 'EC - Raitaru', 'Cit - Keepstar',
                    'Cit - Fortizar', 'Cit - Astrahus']
    timer_key = forms.CharField(widget=forms.PasswordInput, max_length=20)
    type = forms.ChoiceField(choices=((x, x) for x in TYPE_CHOICES))

    class Meta:
        model = Timer
        fields = ('type', 'system', 'end_at')
        widgets = {
            'system': forms.TextInput(attrs={'list': 'json-datalist'}),
            'end_at': forms.TextInput(attrs={'placeholder': 'Ex. 1d13h45m', 'class': 'timer'}),
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

    def clean_timer_key(self):
        timer_key = self.cleaned_data.get('timer_key')
        print(timer_key)
        print(TIMERBOARD_KEY)
        if timer_key != TIMERBOARD_KEY:
            raise forms.ValidationError('Please enter the correct key.')
        return timer_key


class PasteComparisonForm(forms.Form):
    paste_one = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Initial scan...',
                                                             'rows': 5,
                                                             'cols': 50,
                                                             'class': 'text-compare'}))
    paste_two = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Secondary scan...',
                                                             'rows': 5,
                                                             'cols': 50,
                                                             'class': 'text-compare'}))


# class DucksInjuryForm(forms.ModelForm):
#
#     class Meta:
#         model = DucksInjury

