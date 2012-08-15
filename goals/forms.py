from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from goals.models import Goal, Goalset, Date, Dateset, Activity

class GoalForm(forms.ModelForm):
    name = forms.CharField(label='Goal Name', widget=forms.TextInput, error_messages={'required': 'Please enter a name for your goal.'}, max_length=255)
    description = forms.CharField(label='Description', widget=forms.TextInput, error_messages={'required': 'Please enter a description.'}, max_length=255)

    class Meta:
        model = Goal


class GoalsetForm(forms.ModelForm):
    class Meta:
        model = Goalset

    def __init__(self, *args, **kwargs):
        try:
            user = kwargs.pop('user')
            super(GoalsetForm, self).__init__(*args, **kwargs)
            self.fields['goal_one'].queryset = Goal.objects.filter(complete=False, user=user)
            self.fields['goal_two'].queryset = Goal.objects.filter(complete=False, user=user)
            self.fields['goal_three'].queryset = Goal.objects.filter(complete=False, user=user)
            self.fields['goal_four'].queryset = Goal.objects.filter(complete=False, user=user)
        except KeyError:
            super(GoalsetForm, self).__init__(*args, **kwargs)


class DateForm(forms.ModelForm):
    class Meta:
        model = Date

class DatesetForm(forms.ModelForm):
    class Meta:
        model = Dateset

class ActivityForm(forms.ModelForm):
    class Meta:
      model = Activity
