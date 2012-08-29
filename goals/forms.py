import sys

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from goals.models import Goal, Goalset, Date, Dateset, Activity

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(GoalForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = self.cleaned_data

        # prevent goals with duplicate names
        name = cleaned_data.get('name')
        if name is None:
            raise forms.ValidationError("Please enter a name for your goal.")
        else:
            name = cleaned_data['name']
            try:
                existing_name = Goal.objects.get(name__iexact=name, user=self.user)
            except:
                existing_name = False
            if name and existing_name:
                raise forms.ValidationError("You have already created a goal with this name.")

        return cleaned_data


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
