from django import forms

class ContactForm(forms.Form):

    TOPIC_CHOICES = (
        ('', ''),
        ('HLP', 'Get Help'),
        ('BUG', 'Report A Bug'),
        ('OTR', 'Other'),
    )

    topic = forms.CharField(label='Topics', max_length=3, widget=forms.Select(choices=TOPIC_CHOICES))
    message = forms.CharField(label='Your Message', widget=forms.Textarea, error_messages={'required': 'Please enter a message.'})
    email = forms.CharField(label='Your Email Address', widget=forms.TextInput, error_messages={'required': 'Please enter an email address where you can be reached.'})

