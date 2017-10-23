from django import forms
import floppyforms
from .models import Timer
from baggedmilk_django.secret import TIMERBOARD_KEY


class TimerForm(forms.ModelForm):

    timer_key = forms.CharField(max_length=20)

    class Meta:
        data_set = ['One', 'Two', 'Three', 'Four', 'Five', 'Ten']
        model = Timer
        fields = ('type', 'system', 'end_at')
        widgets = {
            'end_at': forms.TextInput(attrs={'placeholder': 'Ex. 1d13h45m'}),
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